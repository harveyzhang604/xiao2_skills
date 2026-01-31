#!/usr/bin/env python3
"""
Profit Hunter ULTIMATE V3 - 轻量运行脚本
适合一次性运行或 cron 使用
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from config import THRESHOLDS
from scorer import KeywordScorer, USER_INTENTS
from gpts_analyzer import GPTsAnalyzer

# 测试关键词
keywords = [
    'struggling with excel pivot table calculator',
    'free video converter online no watermark',
    'ai headshot generator professional',
    'temperature converter celsius to fahrenheit',
    'password strength checker online free',
    'struggling with Notion templates',
    'best ai writing assistant vs chatgpt',
    'online calculator free download',
    'json to csv converter tool',
    'instagram reel downloader online free',
    'image to text converter ocr',
    'how to fix pivot table error',
    'fast battery health checker iphone',
    'free online video editor no watermark',
    'color palette generator from image',
    'website seo checker free online',
    'youtube thumbnail maker free online',
    'instagram story viewer anonymous free',
    'pdf to word converter online free',
    'video compressor online free no watermark',
]

def main():
    start_time = datetime.now()
    
    print('=' * 80)
    print('💎 Profit Hunter ULTIMATE V3 - 轻量挖掘')
    print('=' * 80)
    print(f'\n⏰ 开始时间: {start_time.strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'📊 处理关键词: {len(keywords)} 个')
    print(f'🎯 评分阈值: BUILD NOW ≥ {THRESHOLDS["BUILD_NOW"]} 分')
    print()
    
    # 生成 GPTs 数据
    print('📊 Step 1: GPTs 热度分析...')
    gpts = GPTsAnalyzer()
    gpts_data = {}
    for kw in keywords:
        result = gpts.analyze({kw: {'keyword': kw}})
        if kw in result:
            gpts_data[kw] = result[kw]
    print(f'   ✅ 完成 {len(gpts_data)} 个关键词分析')
    
    # 评分
    print('🎯 Step 2: 关键词评分...')
    scorer = KeywordScorer({}, gpts_data, {})
    results = scorer.score(keywords)
    final_results = scorer.get_final_results(results)
    
    # 统计
    build_now = [r for r in final_results if 'BUILD NOW' in r.get('decision', '')]
    watch = [r for r in final_results if 'WATCH' in r.get('decision', '')]
    
    elapsed = (datetime.now() - start_time).total_seconds()
    
    print('\n' + '=' * 80)
    print('✅ 挖掘完成！')
    print('=' * 80)
    print(f'\n📊 统计结果:')
    print(f'   总关键词: {len(final_results)}')
    print(f'   🔴 BUILD NOW: {len(build_now)} 个')
    print(f'   🟡 WATCH: {len(watch)} 个')
    print(f'   ⏱️  耗时: {elapsed:.1f} 秒')
    
    print('\n' + '-' * 80)
    print('🔥 Top 10 BUILD NOW 机会')
    print('-' * 80)
    
    for i, kw in enumerate(build_now[:10], 1):
        avg_ratio = kw.get('avg_ratio', 0)
        ratio_str = f'{avg_ratio:.2%}' if avg_ratio > 0 else 'N/A'
        
        print(f'\n{i}. {kw["keyword"]}')
        print(f'   评分: {kw["final_score"]}分 | 决策: {kw["decision"]}')
        print(f'   GPTs热度: {ratio_str} | 意图: {kw.get("user_intent", "N/A")}')
        print(f'   目标: {kw.get("user_goal", "N/A")}')
    
    print('\n' + '=' * 80)
    print('💡 提示: 使用 generate_report.py 生成 HTML 可视化报告')
    print('=' * 80)
    
    return final_results


if __name__ == '__main__':
    main()
