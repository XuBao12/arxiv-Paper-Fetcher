import asyncio
import os
import json
from typing import Optional, AsyncGenerator
from contextlib import AsyncExitStack
import logging

from openai import OpenAI
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot.log'),
        logging.StreamHandler()
    ]
)

# 加载 .env 文件，确保 API Key 受到保护
load_dotenv()

class WebChatbot:
    def __init__(self):
        """初始化 Web Chatbot"""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")  # 读取 OpenAI API Key
        self.base_url = os.getenv("BASE_URL")  # 读取 BASE URL
        self.model = os.getenv("MODEL", "gpt-3.5-turbo")  # 读取 model，默认使用 gpt-3.5-turbo

        self.client = None
        if self.openai_api_key:
            self.client = OpenAI(api_key=self.openai_api_key, base_url=self.base_url) # 创建OpenAI client

        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.connected = False
        self.available_tools = []

    async def connect_to_server(self):
        """连接到 MCP 服务器并列出可用工具"""
        if self.connected:
            return True

        # 检查 API Key 是否设置
        if not self.openai_api_key:
            logging.warning("未找到 OpenAI API Key，请先在设置页面配置")
            return False

        # 加载项目目录下的mcp.json配置文件
        config_path = "mcp.json"
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                mcp_servers = config.get("mcpServers", {})
        except Exception as e:
            logging.error(f"读取mcp.json配置文件失败: {str(e)}")
            raise ValueError(f"读取mcp.json配置文件失败: {str(e)}")

        if not mcp_servers:
            logging.error("mcp.json中没有配置任何服务器")
            raise ValueError("mcp.json中没有配置任何服务器")

        # 连接所有服务器
        connected_servers = []
        for server_name, server_config in mcp_servers.items():
            try:
                logging.info(f"正在连接到MCP服务器: {server_name}")
                server_params = StdioServerParameters(
                    command=server_config["command"],
                    args=server_config["args"],
                    env=server_config.get("env")
                )

                # 启动 MCP 服务器并建立通信
                stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
                self.stdio, self.write = stdio_transport
                self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

                await self.session.initialize()

                # 列出 MCP 服务器上的工具
                response = await self.session.list_tools()
                tools = response.tools
                logging.info(f"已连接到服务器 '{server_name}'，支持以下工具: {[tool.name for tool in tools]}")
                connected_servers.append(server_name)

                # 保存可用工具，以便后续使用
                self.available_tools = [{
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "input_schema": tool.inputSchema
                    }
                } for tool in response.tools]

            except Exception as e:
                logging.error(f"连接服务器 '{server_name}' 失败: {str(e)}")

        if not connected_servers:
            logging.error("无法连接到任何MCP服务器")
            raise ValueError("无法连接到任何MCP服务器")

        logging.info(f"成功连接到MCP服务器: {connected_servers}")
        self.connected = True
        return True

    async def process_query(self, query: str) -> str:
        """
        使用大模型处理查询并调用可用的 MCP 工具 (Function Calling)
        """
        # 检查 API Key 是否设置
        if not self.openai_api_key:
            return "请先在设置页面配置 OpenAI API Key。点击页面上的 'API Setup' 按钮进行设置。"

        if not self.connected:
            connect_result = await self.connect_to_server()
            if not connect_result:
                return "连接服务器失败，请检查配置并重试。"

        # 为查询添加有关arxiv论文的上下文信息
        system_message = """
        你是一个专门用于回答 arXiv 论文相关问题的AI助手。你可以帮助用户查找特定领域的研究论文，
        解释论文内容，或者分析论文之间的关系。你可以调用工具来搜索和下载论文。
        当用户询问特定领域的论文时，可以使用搜索工具查询arXiv。
        当用户查询具体的论文时，可以尝试下载并阅读该论文内容来回答问题。
        请以专业、简洁的方式回答问题，并在必要时提供论文链接。
        """

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": query}
        ]

        try:
            # 调用OpenAI API进行处理
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.available_tools
            )

            # 处理返回的内容
            content = response.choices[0]
            if content.finish_reason == "tool_calls":
                # 如果需要使用工具，就解析工具
                tool_call = content.message.tool_calls[0]
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                logging.info(f"调用工具: {tool_name}，参数: {tool_args}")

                # 执行工具
                result = await self.session.call_tool(tool_name, tool_args)

                # 将模型返回的调用哪个工具数据和工具执行完成后的数据都存入messages中
                messages.append(content.message.model_dump())
                messages.append({
                    "role": "tool",
                    "content": result.content[0].text,
                    "tool_call_id": tool_call.id,
                })

                # 将上面的结果再返回给大模型用于生产最终的结果
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                )
                return response.choices[0].message.content

            return content.message.content

        except Exception as e:
            logging.error(f"处理查询时发生错误: {str(e)}")
            return f"抱歉，处理您的请求时发生错误: {str(e)}"

    async def process_query_stream(self, query: str) -> AsyncGenerator[str, None]:
        """
        流式处理查询，逐步返回响应内容
        """
        # 检查 API Key 是否设置
        if not self.openai_api_key:
            yield "请先在设置页面配置 OpenAI API Key。点击页面上的 'API Setup' 按钮进行设置。"
            return

        if not self.connected:
            connect_result = await self.connect_to_server()
            if not connect_result:
                yield "连接服务器失败，请检查配置并重试。"
                return

        # 确保OpenAI客户端已初始化
        if not self.client:
            self.client = OpenAI(api_key=self.openai_api_key, base_url=self.base_url)

        # 为查询添加有关arxiv论文的上下文信息
        system_message = """
        你是一个专门用于回答 arXiv 论文相关问题的AI助手。你可以帮助用户查找特定领域的研究论文，
        解释论文内容，或者分析论文之间的关系。你可以调用工具来搜索和下载论文。
        当用户询问特定领域的论文时，可以使用搜索工具查询arXiv。
        当用户查询具体的论文时，可以尝试下载并阅读该论文内容来回答问题。
        请以专业、简洁的方式回答问题，并在必要时提供论文链接。
        """

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": query}
        ]

        try:
            # 首先检查是否需要使用工具
            logging.info(f"处理查询: {query}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.available_tools
            )

            content = response.choices[0]

            if content.finish_reason == "tool_calls":
                # 如果需要使用工具，就解析工具
                tool_call = content.message.tool_calls[0]
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                logging.info(f"调用工具: {tool_name}，参数: {tool_args}")

                # 先告知用户正在查询
                query_term = tool_args.get('query', '')
                paper_id = tool_args.get('paper_id', '')
                if query_term:
                    yield f"正在查询关于 '{query_term}' 的论文信息..."
                elif paper_id:
                    yield f"正在获取论文 '{paper_id}' 的内容..."
                else:
                    yield "正在使用工具获取信息..."

                try:
                    # 执行工具
                    result = await self.session.call_tool(tool_name, tool_args)

                    # 如果工具调用结果很大，分块返回一部分
                    tool_result_text = result.content[0].text
                    if len(tool_result_text) > 500:
                        yield "\n\n查询结果较大，处理中..."

                    # 将模型返回的调用哪个工具数据和工具执行完成后的数据都存入messages中
                    messages.append(content.message.model_dump())
                    messages.append({
                        "role": "tool",
                        "content": tool_result_text,
                        "tool_call_id": tool_call.id,
                    })

                    yield "\n\n正在分析结果..."

                except Exception as e:
                    logging.error(f"工具调用失败: {str(e)}")
                    yield f"\n\n工具调用失败: {str(e)}"
                    return

                # 使用流式响应获取最终结果
                try:
                    stream = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        stream=True
                    )

                    yield "\n\n"  # 为新内容添加间隔

                    for chunk in stream:
                        if chunk.choices and chunk.choices[0].delta.content:
                            chunk_content = chunk.choices[0].delta.content
                            yield chunk_content

                except Exception as e:
                    logging.error(f"流式响应出错: {str(e)}")
                    yield f"\n\n生成回答时出错: {str(e)}"
            else:
                # 如果不需要工具，则直接使用流式响应
                try:
                    stream = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        stream=True
                    )

                    for chunk in stream:
                        if chunk.choices and chunk.choices[0].delta.content:
                            chunk_content = chunk.choices[0].delta.content
                            yield chunk_content

                except Exception as e:
                    logging.error(f"流式响应出错: {str(e)}")
                    yield f"生成回答时出错: {str(e)}"

        except Exception as e:
            logging.error(f"处理查询时发生错误: {str(e)}")
            yield f"抱歉，处理您的请求时发生错误: {str(e)}"

    async def cleanup(self):
        """清理资源"""
        if self.connected:
            await self.exit_stack.aclose()
            self.connected = False

# 创建一个单例实例
chatbot = None

async def get_chatbot():
    """获取或创建Chatbot实例"""
    global chatbot
    if chatbot is None:
        chatbot = WebChatbot()
        try:
            await chatbot.connect_to_server()
        except Exception as e:
            logging.error(f"初始化聊天机器人失败: {str(e)}")
    return chatbot