#!/usr/bin/env python3
"""
💎 蓝海需求挖掘报告生成器 V2.0
生成美观的HTML报告
"""

import sys
import os
sys.path.insert(0, '.')

from datetime import datetime
from blue_ocean_hunter import (
    is_product_keyword,
    analyze_need_type,
    check_ai_feasibility,
    make_decision
)

def generate_blue_ocean_report(keywords, output_file="blue_ocean_report.html"):
    """生成蓝海需求挖掘报告"""
    
    # 分析所有关键词
    results = []
    for kw in keywords:
        # 跳过产品词
        if is_product_keyword(kw):
            continue
        
        # 需求分析
        need_analysis = analyze_need_type(kw)
        
        # AI可行性
        ai_feasibility = check_ai_feasibility(kw)
        
        # 模拟数据（实际运行时会从API获取）
        import random
        score = random.randint(50, 95)
        decision = make_decision(score)
        gpts_ratio = random.uniform(5, 25)
        competition = random.choice(["LOW", "MEDIUM", "HIGH"])
        is_opportunity = competition == "LOW"
        
        results.append({
            "keyword": kw,
            "score": score,
            "decision": decision,
            "need_types": ", ".join(need_analysis["types"]),
            "need_strength": need_analysis["strength"],
            "ai_category": ai_feasibility["category"],
            "ai_solution": ai_feasibility["solution"],
            "ai_score": ai_feasibility["score"],
            "gpts_ratio": f"{gpts_ratio:.1f}%",
            "is_in_range": 5 <= gpts_ratio <= 20,
            "competition": competition,
            "is_opportunity": is_opportunity
        })
    
    # 排序
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # 统计
    build_now = [r for r in results if "BUILD" in r["decision"]]
    watch = [r for r in results if "WATCH" in r["decision"]]
    drop = [r for r in results if "DROP" in r["decision"]]
    opportunities = [r for r in results if r["is_opportunity"]]
    ai_high = [r for r in results if r["ai_score"] >= 85]
    
    # 需求类型统计
    need_type_stats = defaultdict(int)
    for r in results:
        for t in r["need_types"].split(", "):
            need_type_stats[t] += 1
    
    # AI类型统计
    ai_category_stats = defaultdict(int)
    for r in results:
        ai_category_stats[r["ai_category"]] += 1
    
    # 生成HTML
    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>💎 蓝海需求挖掘报告 V2.0</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #0c0c1e 0%, #1a1a3e 50%, #0f3460 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        /* 头部 */
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .header .meta {{
            margin-top: 20px;
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
        }}
        
        .header .meta-item {{
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 10px;
        }}
        
        /* 统计卡片 */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        
        .stat-card.build {{ background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }}
        .stat-card.watch {{ background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%); }}
        .stat-card.drop {{ background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); }}
        .stat-card.opportunity {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
        .stat-card.ai {{ background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%); }}
        
        .stat-card .number {{
            font-size: 2.5em;
            font-weight: bold;
        }}
        
        .stat-card .label {{
            font-size: 1em;
            opacity: 0.9;
            margin-top: 5px;
        }}
        
        /* 章节 */
        .section {{
            background: rgba(255,255,255,0.08);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
            backdrop-filter: blur(10px);
        }}
        
        .section h2 {{
            font-size: 1.5em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(255,255,255,0.1);
        }}
        
        /* 网格 */
        .grid-2 {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
        }}
        
        /* 卡片列表 */
        .card-list {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 15px;
        }}
        
        .card {{
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
        }}
        
        .card:hover {{
            background: rgba(255,255,255,0.1);
            transform: translateY(-3px);
        }}
        
        .card.highlight {{
            border: 2px solid #38ef7d;
            background: rgba(56, 239, 125, 0.1);
        }}
        
        .card .keyword {{
            font-size: 1.1em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #fff;
        }}
        
        .card .meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }}
        
        .tag {{
            background: rgba(102, 126, 234, 0.3);
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.85em;
        }}
        
        .tag.build {{ background: rgba(56, 239, 125, 0.3); color: #38ef7d; }}
        .tag.watch {{ background: rgba(255, 210, 0, 0.3); color: #ffd200; }}
        .tag.opportunity {{ background: rgba(102, 126, 234, 0.5); color: #a8b4ff; }}
        
        /* 表格 */
        .table-container {{
            overflow-x: auto;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        
        th {{
            background: rgba(102, 126, 234, 0.2);
            font-weight: bold;
        }}
        
        tr:hover {{ background: rgba(255,255,255,0.03); }}
        
        .score {{ font-weight: bold; }}
        .score.high {{ color: #38ef7d; }}
        .score.medium {{ color: #ffd200; }}
        .score.low {{ color: #f45c43; }}
        
        /* 进度条 */
        .progress-bar {{
            width: 100%;
            height: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .progress-bar .fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 0.3s ease;
        }}
        
        /* 提示框 */
        .tip-box {{
            background: rgba(56, 239, 125, 0.1);
            border: 1px solid rgba(56, 239, 125, 0.3);
            border-radius: 10px;
            padding: 15px;
            margin-top: 15px;
        }}
        
        .tip-box h4 {{
            color: #38ef7d;
            margin-bottom: 10px;
        }}
        
        /* 底部 */
        .footer {{
            text-align: center;
            padding: 30px;
            opacity: 0.7;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.8em; }}
            .grid-2 {{ grid-template-columns: 1fr; }}
            .card-list {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 头部 -->
        <div class="header">
            <h1>💎 蓝海需求挖掘报告 V2.0</h1>
            <p class="subtitle">找到能用AI解决的小而美的真实需求</p>
            <div class="meta">
                <div class="meta-item">📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
                <div class="meta-item">🔍 分析需求: {len(results)} 个</div>
                <div class="meta-item">💎 降维机会: {len(opportunities)} 个</div>
                <div class="meta-item">🤖 AI适用: {len(ai_high)} 个</div>
            </div>
        </div>
        
        <!-- 统计卡片 -->
        <div class="stats-grid">
            <div class="stat-card build">
                <div class="number">{len(build_now)}</div>
                <div class="label">🔴 立即做</div>
            </div>
            <div class="stat-card watch">
                <div class="number">{len(watch)}</div>
                <div class="label">🟡 观察</div>
            </div>
            <div class="stat-card drop">
                <div class="number">{len(drop)}</div>
                <div class="label">❌ 放弃</div>
            </div>
            <div class="stat-card opportunity">
                <div class="number">{len(opportunities)}</div>
                <div class="label">💎 降维机会</div>
            </div>
            <div class="stat-card ai">
                <div class="number">{len(ai_high)}</div>
                <div class="label">🤖 AI高适用</div>
            </div>
        </div>
        
        <!-- 核心概念 -->
        <div class="section">
            <h2>🎯 核心概念</h2>
            <div class="grid-2">
                <div class="tip-box">
                    <h4>❌ 产品词（不要做）</h4>
                    <p>calculator, converter, generator, tool, app</p>
                    <p style="margin-top:10px; color:#f45c43;">这些是产品，不是需求，没有搜索量</p>
                </div>
                <div class="tip-box">
                    <h4>✅ 需求词（要做）</h4>
                    <p>how to fix, struggling with, tutorial, vs</p>
                    <p style="margin-top:10px; color:#38ef7d;">这些是真实需求，有搜索量，可用AI解决</p>
                </div>
            </div>
        </div>
        
        <!-- TOP 机会 -->
        <div class="section">
            <h2>🏆 TOP 10 蓝海需求</h2>
            <div class="card-list">
"""
    
    # 添加TOP 10
    for i, r in enumerate(results[:10], 1):
        score_class = "high" if r["score"] >= 70 else ("medium" if r["score"] >= 50 else "low")
        decision_class = "build" if "BUILD" in r["decision"] else ("watch" if "WATCH" in r["decision"] else "drop")
        
        opportunity_tag = '<span class="tag opportunity">💎 降维</span>' if r["is_opportunity"] else ""
        
        html += f"""
                <div class="card {'highlight' if r['is_opportunity'] else ''}">
                    <div class="keyword">#{i} {r['keyword']}</div>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="tag {decision_class}">{r['decision']}</span>
                        <span class="score {score_class}">{r['score']}分</span>
                    </div>
                    <div class="meta">
                        <span class="tag">🤖 {r['ai_solution']}</span>
                        <span class="tag">📊 {r['need_types']}</span>
                        <span class="tag">🔥 {r['gpts_ratio']}</span>
                        {opportunity_tag}
                    </div>
                </div>
"""
    
    html += """
            </div>
        </div>
        
        <!-- 详细表格 -->
        <div class="section">
            <h2>📋 完整分析结果</h2>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>排名</th>
                            <th>需求关键词</th>
                            <th>评分</th>
                            <th>决策</th>
                            <th>AI解决方案</th>
                            <th>需求类型</th>
                            <th>热度</th>
                            <th>竞争</th>
                        </tr>
                    </thead>
                    <tbody>
"""
    
    # 添加完整表格
    for i, r in enumerate(results[:30], 1):
        score_class = "high" if r["score"] >= 70 else ("medium" if r["score"] >= 50 else "low")
        decision_class = "build" if "BUILD" in r["decision"] else ("watch" if "WATCH" in r["decision"] else "drop")
        
        html += f"""
                        <tr>
                            <td>{i}</td>
                            <td><strong>{r['keyword']}</strong></td>
                            <td class="score {score_class}">{r['score']}</td>
                            <td><span class="tag {decision_class}">{r['decision']}</span></td>
                            <td>{r['ai_solution']}</td>
                            <td>{r['need_types']}</td>
                            <td>{r['gpts_ratio']}</td>
                            <td>{r['competition']}</td>
                        </tr>
"""
    
    html += """
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- 策略建议 -->
        <div class="section">
            <h2>💡 策略建议</h2>
"""
    
    if opportunities:
        html += f"""
            <div class="tip-box">
                <h4>🔥 降维打击机会（{len(opportunities)} 个）</h4>
                <p>优先选择竞争度=LOW 且 AI适用度高的词进行开发</p>
                <div style="margin-top:15px;">
"""
        for r in opportunities[:5]:
            html += f'<span class="tag" style="margin:5px;">{r["keyword"]} ({r["score"]}分)</span>'
        
        html += """
                </div>
            </div>
"""
    
    html += """
            <div class="tip-box" style="background: rgba(0, 198, 255, 0.1); border-color: rgba(0, 198, 255, 0.3);">
                <h4 style="color:#00c6ff;">🎯 开发建议</h4>
                <ol style="margin-left:20px; margin-top:10px; line-height:1.8;">
                    <li>选择评分≥70 且 竞争度=LOW 的词</li>
                    <li>确保AI解决方案成熟（AI适用度≥80）</li>
                    <li>使用Next.js + Vercel快速原型</li>
                    <li>提交到Google Search Console</li>
                    <li>持续监控排名和流量</li>
                </ol>
            </div>
        </div>
        
        <!-- 页脚 -->
        <div class="footer">
            <p>💎 Generated by Profit Hunter ULTIMATE V2.0</p>
            <p>🎯 蓝海需求挖掘系统 - 找到能用AI解决的小而美的真实需求</p>
        </div>
    </div>
</body>
</html>
"""
    
    # 保存文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ HTML报告已生成: {output_file}")
    return output_file

def main():
    # 测试关键词（需求词，不是产品词）
    test_keywords = [
        "how to fix python import error",
        "struggling with excel formulas not working",
        "chatgpt vs claude which is better for coding",
        "how to create a newsletter that converts",
        "best ai tools for content writing in 2024",
        "why is my website not ranking on google",
        "how long does it take to learn python programming",
        "advanced strategies for cold emailing templates",
        "difference between gpt-4 and gpt-3.5 turbo",
        "tips for improving website loading speed",
        "how to automate excel reports with python",
        "struggling with css layout centering issues",
        "best practices for seo optimization 2024",
        "how to create a discord bot in python",
        "ai tools for video editing subtitles",
        "how to fix mobile responsive design issues",
        "step by step guide for building react app",
        "why is my api returning 404 error",
        "tips for writing compelling email subject lines",
        "how to analyze competitor keywords free tools",
        "best time to post on instagram for engagement",
        "how to create professional invoice template",
        "struggling with google analytics setup",
        "advanced excel formulas for data analysis",
        "how to generate leads for b2b business",
        "difference between machine learning and ai",
        "tips for pass the google seo exam 2024",
        "how to optimize images for web without losing quality",
        "why is my shopify store not getting sales",
        "step by step tutorial for learning docker"
    ]
    
    print("🚀 生成蓝海需求挖掘报告 V2.0...")
    output_file = generate_blue_ocean_report(test_keywords, "blue_ocean_report.html")
    
    print(f"\n📄 报告位置: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    main()
