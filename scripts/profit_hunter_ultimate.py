#!/usr/bin/env python3
"""
Profit Hunter ULTIMATE V3 - 终极版蓝海关键词猎取系统
整合: Google Autocomplete + Trends + GPTs + Playwright SERP + 用户意图深挖
"""

import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime

# 添加当前目录到 path
sys.path.insert(0, str(Path(__file__).parent))

from config import *
from data_utils import save_csv, load_keywords
from alphabet_soup import GoogleSuggestHarvester
from trends_analyzer import TrendsAnalyzer
from gpts_analyzer import GPTsAnalyzer
from serp_analyzer import SERPAnalyzer
from deep_search import DeepSearchAnalyzer  # 新增
from scorer import KeywordScorer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_pipeline(args):
    """执行完整的关键词挖掘流程 - V3 版"""
    
    start_time = datetime.now()
    logger.info("🚀 Profit Hunter ULTIMATE V3 启动")
    logger.info("=" * 60)
    
    all_keywords = set()
    
    # Step 0: Alphabet Soup 挖词
    logger.info("📊 Step 0: Alphabet Soup 海量挖词...")
    harvester = GoogleSuggestHarvester()
    seed_words = load_keywords()
    logger.info(f"   种子词数量: {len(seed_words)}")
    
    suggest_results = harvester.harvest(seed_words, max_per_word=args.max)
    all_keywords.update(suggest_results)
    logger.info(f"   → 获取 {len(all_keywords)} 个候选关键词")
    
    # V3: 全部关键词，不采样
    keywords = list(all_keywords)
    logger.info(f"   → 处理全部 {len(keywords)} 个关键词")
    
    # 预处理：去重和清理
    keywords = list(set(keywords))
    
    # Step 1: Google Trends 分析
    trends_data = {}
    if args.trends:
        logger.info("📈 Step 1: Google Trends 飙升词分析...")
        analyzer = TrendsAnalyzer()
        trends_data = analyzer.analyze(keywords)
        save_csv(list(trends_data.values()), "step1_trends_deep.csv")
        logger.info(f"   → 分析 {len(trends_data)} 个趋势数据")
    
    # Step 2: GPTs 对比
    logger.info("🤖 Step 2: GPTs 基准对比...")
    gpts_analyzer = GPTsAnalyzer()
    gpts_results = gpts_analyzer.analyze(keywords)
    save_csv(list(gpts_results.values()), "step2_gpts_comparison.csv")
    logger.info(f"   → 对比 {len(gpts_results)} 个关键词")
    
    # 计算 avg_ratio
    if gpts_results:
        ratios = [r.get('ratio', 0) for r in gpts_results.values() if r.get('ratio', 0) > 0]
        if ratios:
            avg_ratio = sum(ratios) / len(ratios)
            logger.info(f"   → 平均 GPTs 热度比: {avg_ratio:.2%}")
    
    # Step 3: SERP 竞争分析
    serp_data = {}
    if args.playwright:
        logger.info("🔍 Step 3: SERP 降维打击分析...")
        serp_analyzer = SERPAnalyzer()
        serp_data = serp_analyzer.analyze(keywords[:args.max])
        save_csv(list(serp_data.values()), "step3_serp_analysis.csv")
        logger.info(f"   → 分析 {len(serp_data)} 个 SERP")
        
        # 统计降维打击机会
        dimension_attacks = [k for k, v in serp_data.items() if v.get('降维打击')]
        logger.info(f"   → 发现 {len(dimension_attacks)} 个降维打击机会")
    
    # Step 3.5: 深度社区搜索（新增）
    deep_data = {}
    if args.deep_search:
        logger.info("🔎 Step 3.5: 深度社区搜索（Reddit/论坛/Google）...")
        deep_analyzer = DeepSearchAnalyzer()
        deep_data = deep_analyzer.analyze_batch(keywords[:args.max])
        save_csv(list(deep_data.values()), "step3_5_deep_search.csv")
        logger.info(f"   → 深度分析 {len(deep_data)} 个关键词")
        
        # 统计高需求关键词
        high_demand = [k for k, v in deep_data.items() if v.get('demand_strength') == 'HIGH']
        logger.info(f"   → 发现 {len(high_demand)} 个高需求机会")
    
    # Step 4: 综合评分 + 用户意图深挖
    logger.info("🎯 Step 4: 综合评分 + 用户意图深挖...")
    scorer = KeywordScorer(trends_data, gpts_results, serp_data, deep_data)
    scored_keywords = scorer.score(keywords)
    
    # Step 5: 输出决策结果
    logger.info("📋 Step 5: 生成最终报告...")
    final_results = scorer.get_final_results(scored_keywords)
    
    # 保存最终结果（V3: 全部关键词）
    save_csv(final_results, "ultimate_final_results.csv")
    
    # 统计
    build_now = [k for k in final_results if 'BUILD NOW' in k.get('decision', '')]
    watch = [k for k in final_results if 'WATCH' in k.get('decision', '')]
    
    elapsed = (datetime.now() - start_time).total_seconds()
    
    logger.info("=" * 60)
    logger.info("✅ V3 分析完成！")
    logger.info(f"   总关键词: {len(final_results)}")
    logger.info(f"   🔴 BUILD NOW: {len(build_now)} 个")
    logger.info(f"   🟡 WATCH: {len(watch)} 个")
    logger.info(f"   ⏱️ 耗时: {elapsed:.1f} 秒")
    logger.info("=" * 60)
    
    # 输出 Top 10 BUILD NOW（带用户意图）
    if build_now:
        logger.info("\n🔥 Top 10 BUILD NOW 机会（含用户意图）：")
        logger.info("-" * 80)
        for i, kw in enumerate(sorted(build_now, key=lambda x: x.get('final_score', 0), reverse=True)[:10], 1):
            降维 = "💎" if kw.get('降维打击') else ""
            avg_ratio = kw.get('avg_ratio', 0)
            user_intent = kw.get('user_intent', 'general')
            user_goal = kw.get('user_goal', '')
            
            logger.info(f"   {i}. {kw['keyword']} ({kw['final_score']}分) {降维}")
            logger.info(f"      GPTs热度比: {avg_ratio:.2%} | 意图: {user_intent}")
            logger.info(f"      目标: {user_goal}")
            logger.info("")
    
    # 显示竞争度分布
    if serp_data:
        competition_dist = {}
        for kw, data in serp_data.items():
            comp = data.get('competition', 'UNKNOWN')
            competition_dist[comp] = competition_dist.get(comp, 0) + 1
        
        logger.info("\n📊 竞争度分布：")
        for comp, count in sorted(competition_dist.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"   {comp}: {count} 个")
    
    return final_results


def main():
    parser = argparse.ArgumentParser(description='Profit Hunter ULTIMATE V3 - 蓝海关键词猎取')
    parser.add_argument('--trends', action='store_true', help='启用 Google Trends 分析')
    parser.add_argument('--playwright', action='store_true', help='启用 Playwright SERP 分析')
    parser.add_argument('--deep-search', action='store_true', help='启用深度社区搜索')
    parser.add_argument('--max', type=int, default=50, help='种子词最大建议数 (默认50)')
    parser.add_argument('--trends-only', action='store_true', help='仅运行 Trends 分析')
    parser.add_argument('--quiet', action='store_true', help='静默模式')
    
    args = parser.parse_args()
    
    # V3: 默认启用 trends
    if not args.trends and not args.trends_only:
        args.trends = True
    
    # V3: 默认提示 playwright 和 deep-search
    if not args.playwright and not args.trends_only:
        logger.info("💡 提示: 添加 --playwright 参数可启用降维打击检测")
    if not args.deep_search and not args.trends_only:
        logger.info("💡 提示: 添加 --deep-search 参数可启用深度社区搜索（Reddit/论坛）")
    
    try:
        results = run_pipeline(args)
    except KeyboardInterrupt:
        logger.info("\n⏹️ 用户中断")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
