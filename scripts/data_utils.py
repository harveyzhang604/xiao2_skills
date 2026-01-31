#!/usr/bin/env python3
"""
数据工具函数
"""

import csv
from pathlib import Path
from config import DATA_DIR


def save_csv(data, filename):
    """保存数据到 CSV"""
    if not data:
        return
    
    Path(DATA_DIR).mkdir(exist_ok=True)
    filepath = Path(DATA_DIR) / filename
    
    if isinstance(data, list) and data:
        # 列表：多条记录
        fieldnames = list(data[0].keys()) if isinstance(data[0], dict) else []
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if fieldnames:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            else:
                # 简单列表
                writer = csv.writer(f)
                writer.writerow([filename])
                for item in data:
                    writer.writerow([item])
    elif isinstance(data, dict):
        # 字典：单条记录
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)
    
    print(f"💾 保存: {filepath}")


def load_keywords():
    """加载种子词"""
    words_file = Path(DATA_DIR) / "words.md"
    if not words_file.exists():
        # 默认种子词
        return ["calculator", "generator", "converter", "tool", "tracker"]
    
    with open(words_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析 markdown 列表
    keywords = []
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('- ') or line.startswith('* '):
            keyword = line[2:].strip()
            if keyword:
                keywords.append(keyword)
    
    return keywords if keywords else ["calculator", "generator"]


def load_csv(filepath):
    """加载 CSV 数据"""
    if not Path(filepath).exists():
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)
