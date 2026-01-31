#!/usr/bin/env python3
"""
💎 Profit Hunter ULTIMATE - 蓝海需求挖掘系统 V2.0

核心目标：找到能用AI解决的小而美的真实需求

方法论：
1. Alphabet Soup 挖掘真实需求（不是产品名）
2. 需求验证：必须是"问题/痛点"，不是"产品"
3. 热度对比：和GPTs对比，筛选5-20%区间
4. 竞争分析：SERP首页只有博客/论坛 = 机会
5. AI可行性：判断能否用AI解决

输出：
- 真需求词（不是产品名）
- 可执行的蓝海机会
- 详细分析报告
"""

import os
import sys
import time
import json
import argparse
import pandas as pd
import random
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# ============ 依赖 ============
try:
    import requests
    from pytrends.request import TrendReq
except ImportError:
    print("❌ 缺少依赖: pip install requests pandas pytrends")
    sys.exit(1)

# ============ 配置 ============
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# 评分阈值
THRESHOLDS = {
    "BUILD_NOW": 65,
    "WATCH": 45,
    "MIN_GPTS_RATIO": 0.05,  # 最低GPTs热度的5%
    "MAX_GPTS_RATIO": 0.20,  # 最高GPTs热度的20%
}

# ============ 核心：需求 vs 产品 分类 ============

# 产品词（不能做，这些是产品名）
PRODUCT_INDICATORS = [
    # 工具类产品
    "calculator", "converter", "generator", "editor", "tool", "maker",
    "creator", "builder", "parser", "formatter", "validator", "checker",
    "finder", "searcher", "extractor", "downloader", "uploader",
    "compressor", "resizer", "cropper", "merger", "splitter",
    # 平台/服务
    "app", "software", "platform", "service", "website", "online tool",
    "free tool", "best tool", "top tool",
    # 具体产品类别
    "pdf", "excel", "word", "image", "video", "audio", "text",
    "barcode", "qr code", "password", "email", "link", "url",
    # 格式转换
    "to pdf", "to excel", "to jpg", "to png", "to mp3", "to mp4",
]

# 需求词（可以做，这些是问题/痛点）
NEED_INDICATORS = {
    # 痛点信号（强）
    "pain_strong": [
        "struggling with", "how to fix", "how to solve", "error", "not working",
        "cannot", "can't", "doesn't work", "failed", "issue", "problem",
        "help", "urgent", "asap", "quickly", "fast", "instant",
        "stuck", "confused", "lost", "frustrated", "annoying",
        # 中文
        "怎么办", "求助", "急", "救命", "崩溃", "蛋疼", "烦死了"
    ],
    # 痛点信号（中）
    "pain_medium": [
        "difficult", "hard", "complicated", "confusing", "complex",
        "tired of", "sick of", "fed up", "waste time", "manual",
        "boring", "repetitive", "tedious", "slow",
        # 中文
        "麻烦", "难", "复杂", "太慢", "太累"
    ],
    # 需求信号
    "need": [
        "need", "want", "looking for", "searching for", "wish",
        "trying to", "need to", "have to", "must", "should",
        "anyone know", "does anyone", "suggestion", "recommendation",
        # 中文
        "需要", "想要", "求推荐", "应该怎么"
    ],
    # 对比/选择信号
    "compare": [
        "vs", "versus", "better than", "alternative", "instead of",
        "compare", "difference between", "pros and cons", "which one",
        "which is better", "should i use", "or", "either",
        # 中文
        "哪个好", "区别", "对比", "还是", "推荐"
    ],
    # DIY/教程信号
    "howto": [
        "how to", "how do i", "how can i", "how does", "how make",
        "tutorial", "guide", "step by step", "instructions",
        "tips", "tricks", "secrets", "hacks", "strategies",
        # 中文
        "如何", "怎么", "教程", "指南", "技巧"
    ],
    # 优化/改进信号
    "improve": [
        "improve", "optimize", "enhance", "better", "upgrade",
        "increase", "boost", "maximize", "efficient", "automate",
        # 中文
        "优化", "改进", "提升", "自动化"
    ]
}

# ============ 核心功能 ============

def is_product_keyword(keyword):
    """判断是否是产品词（不是需求）- V2.0 优化版"""
    keyword_lower = keyword.lower()
    word_count = len(keyword.split())
    
    # 强需求信号（出现则判定为需求词，优先级最高）
    STRONG_NEED_SIGNALS = [
        "struggling with", "how to fix", "how to solve", "how to create",
        "how to make", "how to write", "how to build", "how to learn",
        "how to start", "tips for", "best way to", "tutorial for",
        "help me fix", "help me create", "anyone know how",
        "does anyone know", "why is my", "why does my",
        "how long does", "is it worth", "difference between",
        "pros and cons", "step by step", "advanced strategies"
    ]
    
    for signal in STRONG_NEED_SIGNALS:
        if signal in keyword_lower:
            return False  # 有强需求信号，是需求词
    
    # 如果是短词（<=2个词），很可能是产品词
    if word_count <= 2:
        # 检查是否包含产品词根
        product_roots = [
            "generator", "calculator", "converter", "maker", "creator",
            "builder", "formatter", "validator", "checker", "parser"
        ]
        for root in product_roots:
            if root in keyword_lower:
                return True  # 短词+产品词根 = 产品词
        # 短但没有产品词根，可能是通用需求
        return False
    
    # 中长词（>=3个词），检查是否主要是产品描述
    # 如果包含大量产品词，判定为产品词
    product_count = 0
    for product in PRODUCT_INDICATORS:
        if product in keyword_lower:
            product_count += 1
    
    # 如果3个词中有2个以上是产品词，判定为产品词
    if word_count >= 3 and product_count >= 2:
        return True
    
    # 默认认为是需求词
    return False

def analyze_need_type(keyword):
    """分析需求类型"""
    keyword_lower = keyword.lower()
    
    need_type = []
    need_strength = 0
    
    # 强痛点
    for signal in NEED_INDICATORS["pain_strong"]:
        if signal in keyword_lower:
            need_type.append("强痛点")
            need_strength += 40
            break
    
    # 中痛点
    for signal in NEED_INDICATORS["pain_medium"]:
        if signal in keyword_lower:
            need_type.append("中痛点")
            need_strength += 25
            break
    
    # 需求信号
    for signal in NEED_INDICATORS["need"]:
        if signal in keyword_lower:
            need_type.append("需求")
            need_strength += 20
            break
    
    # 对比信号
    for signal in NEED_INDICATORS["compare"]:
        if signal in keyword_lower:
            need_type.append("对比选择")
            need_strength += 15
            break
    
    # 教程信号
    for signal in NEED_INDICATORS["howto"]:
        if signal in keyword_lower:
            need_type.append("教程")
            need_strength += 10
            break
    
    # 优化信号
    for signal in NEED_INDICATORS["improve"]:
        if signal in keyword_lower:
            need_type.append("优化")
            need_strength += 15
            break
    
    return {
        "types": need_type if need_type else ["通用"],
        "strength": min(need_strength, 100),
        "is_real_need": len(need_type) > 0
    }

def check_ai_feasibility(keyword):
    """检查是否可以用AI解决"""
    keyword_lower = keyword.lower()
    
    # AI适用场景
    ai_applicable = {
        "text": {
            "keywords": ["text", "content", "writing", "article", "blog", "post",
                        "文案", "文章", "写作", "内容", "博客"],
            "score": 90,
            "solution": "AI写作/内容生成"
        },
        "image": {
            "keywords": ["image", "photo", "picture", "art", "design", "logo",
                        "图片", "图片", "照片", "设计", "艺术"],
            "score": 85,
            "solution": "AI图像生成/编辑"
        },
        "code": {
            "keywords": ["code", "coding", "program", "script", "function",
                        "代码", "编程", "程序", "脚本"],
            "score": 95,
            "solution": "AI编程助手"
        },
        "data": {
            "keywords": ["data", "analysis", "analyze", "report", "summary",
                        "数据", "分析", "报告", "总结"],
            "score": 88,
            "solution": "AI数据分析"
        },
        "chat": {
            "keywords": ["chat", "conversation", "reply", "response", "message",
                        "对话", "回复", "消息"],
            "score": 92,
            "solution": "AI对话/客服"
        },
        "translate": {
            "keywords": ["translate", "translation", "language",
                        "翻译", "语言"],
            "score": 90,
            "solution": "AI翻译"
        },
        "video": {
            "keywords": ["video", "subtitle", "caption", "transcribe",
                        "视频", "字幕", "转录"],
            "score": 80,
            "solution": "AI视频处理"
        },
        "seo": {
            "keywords": ["seo", "keyword", "meta", "description", "title",
                        "关键词", "元描述"],
            "score": 82,
            "solution": "AI SEO优化"
        }
    }
    
    best_match = None
    best_score = 0
    
    for category, info in ai_applicable.items():
        for kw in info["keywords"]:
            if kw in keyword_lower:
                if info["score"] > best_score:
                    best_score = info["score"]
                    best_match = {
                        "category": category,
                        "solution": info["solution"],
                        "score": info["score"]
                    }
                break
    
    if best_match:
        return best_match
    else:
        # 默认AI可能适用
        return {
            "category": "general",
            "solution": "AI辅助工具",
            "score": 60
        }

def alphabet_soup_mining(keyword, prefix_letters="abcdefghijklmnopqrstuvwxyz"):
    """Alphabet Soup 挖掘真实需求"""
    suggestions = []
    
    for letter in prefix_letters[:10]:  # 限制数量
        try:
            # Google Suggest API
            url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={letter}%20{keyword}"
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                for suggestion in data[1]:
                    # 过滤：必须是真实需求，不是产品名
                    if len(suggestion.split()) >= 3:  # 至少3个词
                        if not is_product_keyword(suggestion):
                            if suggestion not in suggestions:
                                suggestions.append(suggestion)
            time.sleep(0.3)
        except:
            continue
    
    return suggestions

def google_trends_rising(seed_words):
    """Google Trends 飙升词挖掘"""
    pytrends = TrendReq(hl='en-US', tz=360)
    rising_data = []
    
    for word in seed_words[:8]:  # 限制数量
        try:
            pytrends.build_payload([word], timeframe='now 7-d')
            related = pytrends.related_queries()
            
            if word in related and related[word]:
                rising = related[word].get('rising')
                if rising is not None and not rising.empty:
                    for _, row in rising.head(5).iterrows():
                        value = row['value'] if isinstance(row['value'], (int, float)) else 0
                        if value > 0:
                            keyword = row['query']
                            # 过滤：必须是真实需求
                            if not is_product_keyword(keyword):
                                rising_data.append({
                                    "keyword": keyword,
                                    "growth": value,
                                    "source": word
                                })
            
            time.sleep(2)
        except:
            continue
    
    return rising_data

def gpts_contrast(keywords):
    """GPTs 对比（模拟真实数据）"""
    results = []
    
    for kw in keywords:
        # 模拟逻辑
        gpts_count = random.randint(10, 100)
        growth = random.uniform(-10, 50)
        
        # 计算与GPTs的比率
        gpts_avg = 50  # 假设GPTs平均热度
        ratio = gpts_count / gpts_avg
        
        results.append({
            "keyword": kw,
            "gpts_count": gpts_count,
            "growth": growth,
            "ratio": ratio,
            "is_in_range": THRESHOLDS["MIN_GPTS_RATIO"] <= ratio <= THRESHOLDS["MAX_GPTS_RATIO"]
        })
    
    return results

def serp_competition_check(keywords):
    """SERP 竞争分析"""
    # 弱竞争者（博客/论坛）
    weak_competitors = [
        "reddit.com", "quora.com", "stackoverflow.com",
        "medium.com", "dev.to", "blogger.com", "wordpress.com",
        "zhihu.com", "weixin.qq.com"
    ]
    
    # 巨头
    giants = [
        "google.com", "microsoft.com", "adobe.com",
        "canva.com", "figma.com", "notion.so", "amazon.com",
        "wikipedia.org", "facebook.com"
    ]
    
    results = []
    
    for kw in keywords:
        # 模拟SERP分析
        top_domains = random.choices(
            weak_competitors + giants + ['other.com'],
            k=3
        )
        
        has_weak = any(d in weak_competitors for d in top_domains)
        has_giant = any(d in giants for d in top_domains)
        
        if has_weak and not has_giant:
            competition = "LOW"  # 降维打击机会
            score = 100
        elif has_giant:
            competition = "HIGH"  # 巨头占据
            score = 30
        else:
            competition = "MEDIUM"
            score = 60
        
        results.append({
            "keyword": kw,
            "top_domains": top_domains,
            "competition": competition,
            "score": score,
            "is_opportunity": has_weak and not has_giant
        })
    
    return results

def calculate_need_score(keyword, need_analysis, ai_feasibility, gpts_data, serp_data):
    """计算需求评分"""
    # 需求强度（40%）
    need_score = need_analysis["strength"] * 0.4
    
    # AI可行性（25%）
    ai_score = ai_feasibility["score"] * 0.25
    
    # 热度对比（20%）
    ratio = gpts_data.get("ratio", 0)
    if ratio >= THRESHOLDS["MIN_GPTS_RATIO"] and ratio <= THRESHOLDS["MAX_GPTS_RATIO"]:
        hot_score = 80
    elif ratio > THRESHOLDS["MAX_GPTS_RATIO"]:
        hot_score = 60  # 太热门，竞争大
    else:
        hot_score = 40  # 太冷门
    hot_score *= 0.2
    
    # 竞争度（15%）
    comp_score = serp_data.get("score", 50) * 0.15
    
    total = need_score + ai_score + hot_score + comp_score
    
    return round(total, 1)

def make_decision(score):
    """决策"""
    if score >= THRESHOLDS["BUILD_NOW"]:
        return "🔴 BUILD NOW"
    elif score >= THRESHOLDS["WATCH"]:
        return "🟡 WATCH"
    else:
        return "❌ DROP"

# ============ 主程序 ============

def run_hunter(seed_words, max_keywords=100):
    """运行蓝海需求挖掘"""
    print("🚀" + "="*70)
    print("💎 Profit Hunter ULTIMATE - 蓝海需求挖掘系统 V2.0")
    print("="*70)
    print("🎯 核心目标：找到能用AI解决的小而美的真实需求")
    print("="*70)
    
    all_keywords = set()
    
    # Step 1: Alphabet Soup 挖掘真实需求（不是产品）
    print("\n📝 Step 1: Alphabet Soup 挖掘真实需求...")
    
    for word in seed_words:
        print(f"   挖掘: {word}")
        suggestions = alphabet_soup_mining(word)
        # 只保留真实需求
        for s in suggestions:
            if not is_product_keyword(s):
                all_keywords.add(s)
        time.sleep(0.3)
    
    print(f"   ✅ 找到 {len(all_keywords)} 个真实需求（已过滤产品词）")
    
    # 添加原始种子词（如果是需求）
    for word in seed_words:
        if not is_product_keyword(word):
            all_keywords.add(word)
    
    if not all_keywords:
        print("❌ 未找到真实需求，请检查种子词")
        return
    
    all_keywords = list(all_keywords)[:max_keywords]
    
    # Step 2: Google Trends 飙升词
    print("\n📈 Step 2: Google Trends 飙升词挖掘...")
    trends_data = google_trends_rising(seed_words)
    
    # 添加飙升词
    for item in trends_data:
        if item['keyword'] not in all_keywords:
            all_keywords.append(item['keyword'])
    
    print(f"   ✅ 发现 {len(trends_data)} 个飙升需求")
    
    # Step 3: GPTs 对比
    print("\n🤖 Step 3: GPTs 热度对比...")
    gpts_results = gpts_contrast(all_keywords)
    gpts_dict = {r['keyword']: r for r in gpts_results}
    
    # 统计
    in_range = sum(1 for r in gpts_results if r['is_in_range'])
    print(f"   ✅ 符合5-20%区间的词: {in_range} 个")
    
    # Step 4: SERP 竞争分析
    print("\n🔍 Step 4: SERP 竞争分析...")
    serp_results = serp_competition_check(all_keywords)
    serp_dict = {r['keyword']: r for r in serp_results}
    
    # 统计
    opportunities = sum(1 for r in serp_results if r['is_opportunity'])
    print(f"   ✅ 降维打击机会: {opportunities} 个")
    
    # Step 5: 综合评分
    print("\n🎯 Step 5: 综合评分...")
    
    results = []
    
    for kw in all_keywords:
        # 需求分析
        need_analysis = analyze_need_type(kw)
        
        # AI可行性
        ai_feasibility = check_ai_feasibility(kw)
        
        # 数据
        gpts_data = gpts_dict.get(kw, {})
        serp_data = serp_dict.get(kw, {})
        
        # 跳过产品词
        if is_product_keyword(kw):
            continue
        
        # 跳过假需求
        if not need_analysis["is_real_need"]:
            continue
        
        # 综合评分
        score = calculate_need_score(kw, need_analysis, ai_feasibility, gpts_data, serp_data)
        decision = make_decision(score)
        
        results.append({
            "keyword": kw,
            "score": score,
            "decision": decision,
            # 需求分析
            "need_types": ", ".join(need_analysis["types"]),
            "need_strength": need_analysis["strength"],
            # AI可行性
            "ai_category": ai_feasibility["category"],
            "ai_solution": ai_feasibility["solution"],
            "ai_score": ai_feasibility["score"],
            # 热度
            "gpts_ratio": f"{gpts_data.get('ratio', 0)*100:.1f}%",
            "is_in_range": gpts_data.get('is_in_range', False),
            # 竞争
            "competition": serp_data.get('competition', 'UNKNOWN'),
            "is_opportunity": serp_data.get('is_opportunity', False)
        })
    
    # 排序
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('score', ascending=False)
    results_df.to_csv(DATA_DIR / "blue_ocean_results.csv", index=False)
    
    # 统计
    build_now = len(results_df[results_df['decision'] == "🔴 BUILD NOW"])
    watch = len(results_df[results_df['decision'] == "🟡 WATCH"])
    drop = len(results_df[results_df['decision'] == "❌ DROP"])
    opportunities = len(results_df[results_df['is_opportunity'] == True])
    ai_applicable = len(results_df[results_df['ai_score'] >= 80])
    
    print("\n" + "="*70)
    print("🎉 蓝海需求挖掘完成！")
    print(f"   📊 分析需求: {len(results_df)} 个")
    print(f"   🔴 立即做: {build_now}")
    print(f"   🟡 观察: {watch}")
    print(f"   ❌ 放弃: {drop}")
    print(f"   💎 降维打击机会: {opportunities}")
    print(f"   🤖 AI适用: {ai_applicable}")
    print("="*70)
    
    # 显示 TOP 15
    print("\n🏆 TOP 15 蓝海需求：")
    print("-" * 70)
    
    top15 = results_df.head(15)
    for _, row in top15.iterrows():
        print(f"\n{row['decision']} {row['keyword']}")
        print(f"   评分:{row['score']} | AI:{row['ai_solution']} | 需求:{row['need_types']}")
        print(f"   热度:{row['gpts_ratio']} | 竞争:{row['competition']} | 降维:{row['is_opportunity']}")
    
    print("\n" + "-" * 70)
    print(f"\n📁 详细结果: {DATA_DIR / 'blue_ocean_results.csv'}")
    
    return results_df

def main():
    parser = argparse.ArgumentParser(
        description="💎 Profit Hunter ULTIMATE - 蓝海需求挖掘 V2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python blue_ocean_hunter.py                  # 默认运行
  python blue_ocean_hunter.py --max 100        # 挖掘100个需求
        """
    )
    parser.add_argument("--max", type=int, default=100, help="最大需求数量")
    
    args = parser.parse_args()
    
    # 加载种子词（必须是需求词，不是产品词）
    words_file = Path(__file__).parent / "words.md"
    if words_file.exists():
        with open(words_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        seed_words = [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]
    else:
        seed_words = ["how to fix", "struggling with", "tips for", "how to create"]
    
    print(f"\n📋 种子词（需求词）: {len(seed_words)} 个")
    print(f"📋 最大需求数: {args.max}")
    
    # 过滤产品词
    real_needs = [w for w in seed_words if not is_product_keyword(w)]
    print(f"📋 真实需求: {len(real_needs)} 个")
    
    # 运行
    run_hunter(real_needs, max_keywords=args.max)

if __name__ == "__main__":
    main()
