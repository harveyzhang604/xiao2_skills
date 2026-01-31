#!/usr/bin/env python3
"""
测试脚本 - Profit Hunter ULTIMATE V3（快速版）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

# 直接导入模块测试
from config import THRESHOLDS
from scorer import KeywordScorer, USER_INTENTS
from gpts_analyzer import GPTsAnalyzer
from serp_analyzer import SERPAnalyzer


def test_modules():
    """测试各个模块"""
    print("=" * 60)
    print("🧪 Profit Hunter ULTIMATE V3 模块测试")
    print("=" * 60)
    
    all_passed = True
    
    # 1. 测试配置
    print("\n📋 1. 配置测试")
    print(f"   BUILD_NOW 阈值: {THRESHOLDS['BUILD_NOW']}")
    print(f"   WATCH 阈值: {THRESHOLDS['WATCH']}")
    if THRESHOLDS['BUILD_NOW'] == 65:
        print("   ✅ PASS")
    else:
        print("   ❌ FAIL")
        all_passed = False
    
    # 2. 测试评分器
    print("\n🎯 2. 评分器测试")
    scorer = KeywordScorer({}, {}, {})
    
    # 测试用户意图
    test_cases = [
        ('calculator', 'calculate'),
        ('converter', 'convert'),
        ('generator', 'generate'),
        ('checker', 'check'),
        ('planner', 'plan'),
    ]
    
    for keyword, expected_intent in test_cases:
        result = scorer._analyze_user_intent(keyword)
        if result['intent_types'] == expected_intent:
            print(f"   ✅ {keyword} → {result['intent_types']}")
        else:
            print(f"   ❌ {keyword} → {result['intent_types']} (期望 {expected_intent})")
            all_passed = False
    
    # 测试复合意图
    result = scorer._analyze_user_intent('online calculator converter')
    print(f"   🔗 复合意图测试: '{result['intent_types']}' → {result['goal']}")
    
    # 测试评分
    result = scorer._score_keyword('struggling with excel calculator')
    print(f"   📊 评分测试: '{result['keyword']}'")
    print(f"      最终评分: {result['final_score']}")
    print(f"      用户意图: {result['user_intent']}")
    print(f"      目标: {result['user_goal']}")
    print(f"      清晰度: {result['intent_clarity']}")
    
    # 3. 测试 GPTs 分析器
    print("\n🤖 3. GPTs 分析器测试")
    gpts = GPTsAnalyzer()
    volume = gpts._estimate_volume('free online calculator')
    print(f"   估算搜索量: {volume}")
    
    score = gpts._calc_score(0.15, 150)
    print(f"   热度评分: {score}")
    
    # 4. 测试 SERP 分析器
    print("\n🔍 4. SERP 分析器测试")
    serp = SERPAnalyzer()
    result = serp._analyze_competition('free online calculator')
    print(f"   竞争度: {result['level']} (Score: {result['score']})")
    print(f"   降维打击: {result['is_weak']}")
    
    # 5. 综合测试
    print("\n🏆 5. 综合评分测试")
    
    test_keywords = [
        'struggling with excel calculator',
        'free video converter online',
        'generator for content',
        'simple tracker tool',
    ]
    
    for kw in test_keywords:
        scored = scorer._score_keyword(kw)
        decision = '🔴 BUILD NOW' if scored['final_score'] >= THRESHOLDS['BUILD_NOW'] else '🟡 WATCH'
        print(f"   • {kw}")
        print(f"     评分: {scored['final_score']} | {decision}")
        print(f"     意图: {scored['user_intent']} | {scored['user_goal']}")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有测试通过！")
    else:
        print("⚠️  部分测试失败")
    print("=" * 60)
    
    return all_passed


if __name__ == "__main__":
    success = test_modules()
    sys.exit(0 if success else 1)
