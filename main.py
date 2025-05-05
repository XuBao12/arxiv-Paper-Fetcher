#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ArXiv Paper Fetcher 入口文件
使用此文件启动Web应用或运行论文抓取功能
"""

import sys
import argparse
from src.app import app
from src.arxiv_fetcher import ArxivFetcher

def parse_args():
    parser = argparse.ArgumentParser(description='ArXiv Paper Fetcher')
    parser.add_argument('--fetch', action='store_true', help='仅抓取论文，不启动web界面')
    parser.add_argument('--port', type=int, default=8080, help='Web服务器端口')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Web服务器主机')
    return parser.parse_args()

def main():
    args = parse_args()

    if args.fetch:
        print("正在从arXiv抓取论文...")
        fetcher = ArxivFetcher()
        papers = fetcher.fetch_papers()
        fetcher.save_papers(papers)
        print(f"抓取完成，共获取{len(papers)}篇论文")
    else:
        print(f"启动Web服务器，访问 http://{args.host if args.host != '0.0.0.0' else 'localhost'}:{args.port}")
        app.run(host=args.host, port=args.port, debug=True)

if __name__ == "__main__":
    main()