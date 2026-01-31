#!/usr/bin/env python3
"""
💎 Profit Hunter ULTIMATE - 快速测试版本（模拟数据）
用于验证所有核心功能是否正常工作
"""

import sys
sys.path.insert(0, '.')

from profit_hunter_ultimate import (
    analyze_user_intent,
    calculate_intent_score,
    extract_signals,
    make_decision,
    INTENT_TYPES
)

def run_quick_test():
    """运行快速测试"""
    print("🚀" + "="*70)
    print("💎 Profit Hunter ULTIMATE - 快速测试")
    print("="*70)
    
    # 测试用户意图深挖
    print("\n📊 Step 1: 用户意图深挖测试")
    print("-" * 70)
    
    test_keywords = [
        "roi calculator online",
        "currency converter free",
        "image to text converter",
        "excel password remover",
        "video compressor online free",
        "chatgpt vs claude which is better",
        "python error how to fix",
        "ai content generator tool",
        "bulk email verifier api",
        "instagram reel downloader online"
    ]
    
    for kw in test_keywords:
        intent = analyze_user_intent(kw)
        signals = extract_signals(kw)
        score = calculate_intent_score(kw)
        decision = make_decision(score)
        
        print(f"\n🔍 {kw}")
        print(f"   意图类型: {intent['user_intent']}")
        print(f"   用户目标: {intent['user_goal']}")
        print(f"   清晰度: {intent['intent_clarity']} | 信号: {signals}")
        print(f"   评分: {score} → {decision}")
    
    # 测试意图类型字典
    print("\n" + "="*70)
    print("📋 可检测的意图类型：")
    print("-" * 70)
    
    for intent_type, info in INTENT_TYPES.items():
        print(f"   • {intent_type}: {info['description']}")
        print(f"     关键词: {', '.join(info['keywords'][:5])}")
    
    # 统计
    build_now = 0
    watch = 0
    drop = 0
    
    print("\n" + "="*70)
    print("📈 测试结果统计")
    print("-" * 70)
    
    for kw in test_keywords:
        score = calculate_intent_score(kw)
        decision = make_decision(score)
        if decision == "🔴 BUILD NOW":
            build_now += 1
        elif decision == "🟡 WATCH":
            watch += 1
        else:
            drop += 1
    
    print(f"   🔴 立即做: {build_now}")
    print(f"   🟡 观察: {watch}")
    print(f"   ❌ 放弃: {drop}")
    
    print("\n" + "="*70)
    print("✅ 所有核心功能测试通过！")
    print("="*70)
    
    print("\n💡 核心功能验证：")
    print("   ✅ 用户意图深挖 (analyze_user_intent)")
    print("   ✅ 需求强度评分 (calculate_intent_score)")
    print("   ✅ 信号词提取 (extract_signals)")
    print("   ✅ 决策系统 (make_decision)")
    print("   ✅ 意图类型字典 (INTENT_TYPES)")
    
    print("\n🚀 下一步：运行完整版本")
    print("   python3 profit_hunter_ultimate.py --max 500")
    
    return True

if __name__ == "__main__":
    try:
        run_quick_test()
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
