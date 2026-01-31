#!/usr/bin/env python3
"""
Profit Hunter ULTIMATE V3.0 - 快速测试
"""

import sys
sys.path.insert(0, '.')

from profit_hunter_v3 import (
    analyze_pain_points,
    analyze_commercial_value,
    serp_dimensional_analysis,
    gpts_market_analysis,
    calculate_super_score,
    make_decision
)

def test_v3_functions():
    """测试 V3 核心功能"""
    print("🧪 测试 V3.0 核心功能...")
    
    test_keywords = [
        "ai headshot generator",
        "struggling with excel pivot table",
        "best ai writing tool 2024",
        "free video converter online",
        "python vs javascript",
        "tired of manual data entry",
        "instagram reel downloader",
        "ai calculator for business"
    ]
    
    print("\n📊 痛点强度分析：")
    for kw in test_keywords:
        pain = analyze_pain_points(kw)
        commercial = analyze_commercial_value(kw)
        serp = serp_dimensional_analysis(kw)
        gpts = gpts_market_analysis(kw)
        
        score = calculate_super_score(
            kw, ["google", "youtube"], [], serp, gpts, pain, commercial
        )
        decision = make_decision(score)
        
        print(f"\n   🔍 {kw}")
        print(f"      痛点:{pain} 商业:{commercial} 竞争:{serp['competition_level']} 降维:{serp['is_dimensional_attack']}")
        print(f"      📈 综合评分: {score:.1f} → {decision}")
    
    print("\n✅ V3 功能测试通过！")

def run_quick_demo():
    """运行快速演示"""
    print("="*70)
    print("🚀 Profit Hunter ULTIMATE V3.0 - 快速演示")
    print("="*70)
    
    test_v3_functions()
    
    print("\n" + "="*70)
    print("💡 下一步：运行完整版 V3")
    print("   python scripts/profit_hunter_v3.py --max 50")
    print("="*70)

if __name__ == "__main__":
    run_quick_demo()
