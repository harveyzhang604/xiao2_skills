#!/usr/bin/env python3
"""
Profit Hunter ULTIMATE V3 - HTML 报告生成器
"""

import sys
from pathlib import Path
from datetime import datetime
from scorer import KeywordScorer, USER_INTENTS
from gpts_analyzer import GPTsAnalyzer
from config import THRESHOLDS


def generate_report(results, output_path=None):
    """生成 HTML 报告"""
    
    # 统计
    build_now = [r for r in results if 'BUILD NOW' in r.get('decision', '')]
    watch = [r for r in results if 'WATCH' in r.get('decision', '')]
    drop = [r for r in results if 'DROP' in r.get('decision', '')]
    
    # Top 10 关键词行
    top_keywords_rows = ''
    for i, kw in enumerate(build_now[:10], 1):
        score = kw.get('final_score', 0)
        avg_ratio = kw.get('avg_ratio', 0)
        ratio_str = f'{avg_ratio:.2%}' if avg_ratio > 0 else 'N/A'
        
        if score >= 80:
            score_class = 'score-high'
            bar_color = '#10b981'
        elif score >= 60:
            score_class = 'score-medium'
            bar_color = '#f59e0b'
        else:
            score_class = 'score-low'
            bar_color = '#ef4444'
        
        user_intent = kw.get('user_intent', 'N/A')
        user_goal = kw.get('user_goal', 'N/A')
        降维 = '<span class="dim-attack">💎 降维</span>' if kw.get('降维打击') else '-'
        
        top_keywords_rows += f'''
        <tr>
            <td><strong>#{i}</strong></td>
            <td class="keyword">{kw['keyword']}</td>
            <td>
                <span class="score-badge {score_class}">{score}分</span>
                <div class="score-bar">
                    <div class="score-bar-fill" style="width: {score}%; background: {bar_color}"></div>
                </div>
            </td>
            <td><span class="decision-badge decision-build">🔴 BUILD NOW</span></td>
            <td>{ratio_str}</td>
            <td><span class="intent-tag">{user_intent}</span></td>
            <td style="font-size: 0.9rem; color: #64748b;">{user_goal}</td>
            <td>{降维}</td>
        </tr>
        '''
    
    # 完整关键词行
    all_keywords_rows = ''
    for kw in results:
        score = kw.get('final_score', 0)
        trend = kw.get('trend_score', 0)
        intent = kw.get('intent_score', 0)
        competition = kw.get('competition_score', 0)
        buildability = kw.get('buildability_score', 0)
        decision = kw.get('decision', '')
        user_intent = kw.get('user_intent', 'N/A')
        
        if 'BUILD' in decision:
            decision_class = 'decision-build'
        elif 'WATCH' in decision:
            decision_class = 'decision-watch'
        else:
            decision_class = 'decision-drop'
        
        all_keywords_rows += f'''
        <tr>
            <td class="keyword">{kw['keyword']}</td>
            <td><strong>{score}</strong></td>
            <td>{trend}</td>
            <td>{intent}</td>
            <td>{competition}</td>
            <td>{buildability}</td>
            <td><span class="decision-badge {decision_class}">{decision}</span></td>
            <td><span class="intent-tag">{user_intent}</span></td>
        </tr>
        '''
    
    # 用户意图分析
    intent_analysis_rows = ''
    for intent_type, intent_info in USER_INTENTS.items():
        keywords_with_intent = [r for r in build_now if intent_type in r.get('user_intent', '')]
        examples = [kw['keyword'][:40] + '...' if len(kw['keyword']) > 40 else kw['keyword'] for kw in keywords_with_intent[:3]]
        
        if examples:
            examples_html = '<br>'.join([f'<span class="intent-example">{ex}</span>' for ex in examples])
        else:
            examples_html = '<span class="intent-example">示例关键词...</span>'
        
        intent_analysis_rows += f'''
        <div class="intent-card">
            <div class="intent-type">{intent_type}</div>
            <div class="intent-goal">{intent_info['goal']}</div>
            <div class="intent-examples">
                {examples_html}
            </div>
        </div>
        '''
    
    # 用户意图类型说明
    intent_types_rows = ''
    for intent_type, intent_info in USER_INTENTS.items():
        keywords_list = ', '.join(intent_info['keywords'][:5])
        
        intent_types_rows += f'''
        <div class="intent-card">
            <div class="intent-type">📌 {intent_type}</div>
            <div class="intent-goal">{intent_info['goal']}</div>
            <div style="color: #64748b; font-size: 0.9rem;">
                <strong>触发词:</strong> {keywords_list}
            </div>
        </div>
        '''
    
    # 生成 HTML
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Profit Hunter ULTIMATE V3 - 蓝海关键词分析报告</title>
    <style>
        :root {{
            --primary: #6366f1;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --dark: #1e293b;
            --light: #f8fafc;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            border-radius: 16px;
            padding: 40px;
            margin-bottom: 24px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            color: var(--dark);
            margin-bottom: 8px;
        }}
        
        .header .subtitle {{
            color: #64748b;
            font-size: 1.1rem;
            margin-bottom: 24px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, var(--primary) 0%, #8b5cf6 100%);
            border-radius: 12px;
            padding: 24px;
            color: white;
        }}
        
        .stat-card.green {{ background: linear-gradient(135deg, var(--success) 0%, #34d399 100%); }}
        .stat-card.orange {{ background: linear-gradient(135deg, var(--warning) 0%, #fbbf24 100%); }}
        .stat-card.red {{ background: linear-gradient(135deg, var(--danger) 0%, #f87171 100%); }}
        
        .stat-value {{ font-size: 2.5rem; font-weight: 700; }}
        .stat-label {{ font-size: 0.9rem; opacity: 0.9; }}
        
        .card {{
            background: white;
            border-radius: 16px;
            padding: 32px;
            margin-bottom: 24px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        }}
        
        .card h2 {{
            font-size: 1.5rem;
            color: var(--dark);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .card h2::before {{
            content: '';
            width: 4px;
            height: 24px;
            background: var(--primary);
            border-radius: 2px;
        }}
        
        .keyword-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .keyword-table th,
        .keyword-table td {{
            padding: 16px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .keyword-table th {{
            background: #f8fafc;
            font-weight: 600;
            color: #475569;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .keyword-table tr:hover {{
            background: #f8fafc;
        }}
        
        .keyword-table .keyword {{
            font-weight: 600;
            color: var(--dark);
            font-size: 1rem;
        }}
        
        .score-badge {{
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
        }}
        
        .score-high {{ background: #dcfce7; color: #166534; }}
        .score-medium {{ background: #fef3c7; color: #92400e; }}
        .score-low {{ background: #fee2e2; color: #991b1b; }}
        
        .decision-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 16px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.9rem;
        }}
        
        .decision-build {{
            background: linear-gradient(135deg, var(--success) 0%, #34d399 100%);
            color: white;
        }}
        
        .decision-watch {{
            background: linear-gradient(135deg, var(--warning) 0%, #fbbf24 100%);
            color: white;
        }}
        
        .decision-drop {{
            background: linear-gradient(135deg, var(--danger) 0%, #f87171 100%);
            color: white;
        }}
        
        .intent-tag {{
            display: inline-block;
            padding: 4px 12px;
            background: #e0e7ff;
            color: #4338ca;
            border-radius: 6px;
            font-size: 0.85rem;
            margin-right: 6px;
            margin-bottom: 4px;
        }}
        
        .dim-attack {{
            display: inline-block;
            background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
            color: white;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        
        .score-bar {{
            width: 100%;
            height: 8px;
            background: #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .score-bar-fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 0.3s ease;
        }}
        
        .intent-analysis {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }}
        
        .intent-card {{
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            border-radius: 12px;
            padding: 24px;
            border-left: 4px solid var(--primary);
        }}
        
        .intent-type {{
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--dark);
            margin-bottom: 8px;
        }}
        
        .intent-goal {{
            color: #64748b;
            font-size: 0.95rem;
            margin-bottom: 12px;
        }}
        
        .intent-examples {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        
        .intent-example {{
            background: white;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 0.85rem;
            color: #475569;
        }}
        
        .config-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        
        .config-section {{
            background: #f8fafc;
            border-radius: 12px;
            padding: 24px;
        }}
        
        .config-section h3 {{
            font-size: 1.1rem;
            color: var(--dark);
            margin-bottom: 16px;
        }}
        
        .config-item {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .config-item:last-child {{
            border-bottom: none;
        }}
        
        .config-label {{ color: #64748b; }}
        .config-value {{ font-weight: 600; color: var(--dark); }}
        
        .formula {{
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: white;
            padding: 24px;
            border-radius: 12px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.95rem;
            overflow-x: auto;
            white-space: pre-wrap;
        }}
        
        .footer {{
            text-align: center;
            color: white;
            padding: 24px;
            opacity: 0.8;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.8rem; }}
            .keyword-table {{ font-size: 0.9rem; }}
            .keyword-table th, .keyword-table td {{ padding: 12px 8px; }}
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .card {{
            animation: fadeIn 0.5s ease forwards;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 头部 -->
        <div class="header">
            <h1>💎 Profit Hunter ULTIMATE V3</h1>
            <p class="subtitle">蓝海关键词猎取系统 | 自动化需求挖掘 + 用户意图分析</p>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{len(results)}</div>
                    <div class="stat-label">总关键词</div>
                </div>
                <div class="stat-card green">
                    <div class="stat-value">{len(build_now)}</div>
                    <div class="stat-label">🔴 BUILD NOW</div>
                </div>
                <div class="stat-card orange">
                    <div class="stat-value">{len(watch)}</div>
                    <div class="stat-label">🟡 WATCH</div>
                </div>
                <div class="stat-card red">
                    <div class="stat-value">{len(drop)}</div>
                    <div class="stat-label">❌ DROP</div>
                </div>
            </div>
        </div>
        
        <!-- Top 机会 -->
        <div class="card">
            <h2>🔥 Top 10 BUILD NOW 机会</h2>
            <p style="color: #64748b; margin-bottom: 20px;">基于多维度评分算法，自动识别高价值低竞争机会</p>
            
            <table class="keyword-table">
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>关键词</th>
                        <th>评分</th>
                        <th>决策</th>
                        <th>GPTs 热度</th>
                        <th>用户意图</th>
                        <th>用户目标</th>
                        <th>降维</th>
                    </tr>
                </thead>
                <tbody>
                    {top_keywords_rows}
                </tbody>
            </table>
        </div>
        
        <!-- 用户意图分析 -->
        <div class="card">
            <h2>🎯 用户意图深挖分析</h2>
            <p style="color: #64748b; margin-bottom: 20px;">V3 核心功能：分析用户真正想做什么（calculate / convert / generate / check）</p>
            
            <div class="intent-analysis">
                {intent_analysis_rows}
            </div>
        </div>
        
        <!-- 完整结果表 -->
        <div class="card">
            <h2>📋 完整评分结果</h2>
            <p style="color: #64748b; margin-bottom: 20px;">所有 {len(results)} 个关键词的详细评分数据</p>
            
            <table class="keyword-table">
                <thead>
                    <tr>
                        <th>关键词</th>
                        <th>最终评分</th>
                        <th>趋势分</th>
                        <th>意图分</th>
                        <th>竞争分</th>
                        <th>可实现分</th>
                        <th>决策</th>
                        <th>用户意图</th>
                    </tr>
                </thead>
                <tbody>
                    {all_keywords_rows}
                </tbody>
            </table>
        </div>
        
        <!-- 评分算法 -->
        <div class="card">
            <h2>📐 V3 评分算法</h2>
            
            <div class="formula">Final Score = Trend × 25% + Intent × 35% + Competition × 25% + Buildability × 15% + 降维(+20)</div>
            
            <div class="config-grid" style="margin-top: 24px;">
                <div class="config-section">
                    <h3>🎯 意图信号</h3>
                    <div class="config-item">
                        <span class="config-label">强痛点</span>
                        <span class="config-value">+40分 (struggling with, how to fix)</span>
                    </div>
                    <div class="config-item">
                        <span class="config-label">工具词</span>
                        <span class="config-value">+30分 (calculator, generator)</span>
                    </div>
                    <div class="config-item">
                        <span class="config-label">对比词</span>
                        <span class="config-value">+25分 (vs, alternative)</span>
                    </div>
                    <div class="config-item">
                        <span class="config-label">B2B 词</span>
                        <span class="config-value">+25分 (bulk, api)</span>
                    </div>
                    <div class="config-item">
                        <span class="config-label">速度词</span>
                        <span class="config-value">+20分 (fast, quick)</span>
                    </div>
                    <div class="config-item">
                        <span class="config-label">长尾词</span>
                        <span class="config-value">+15分 (2+词)</span>
                    </div>
                </div>
                
                <div class="config-section">
                    <h3>📊 决策阈值</h3>
                    <div class="config-item">
                        <span class="config-label">🔴 BUILD NOW</span>
                        <span class="config-value">≥ 65 分</span>
                    </div>
                    <div class="config-item">
                        <span class="config-label">🟡 WATCH</span>
                        <span class="config-value">45-65 分</span>
                    </div>
                    <div class="config-item">
                        <span class="config-label">❌ DROP</span>
                        <span class="config-value">< 45 分</span>
                    </div>
                </div>
                
                <div class="config-section">
                    <h3>💎 降维打击条件</h3>
                    <div class="config-item">
                        <span class="config-label">目标网站</span>
                        <span class="config-value">Reddit/Quora/Medium/Stack Overflow</span>
                    </div>
                    <div class="config-item">
                        <span class="config-label">加成分数</span>
                        <span class="config-value">+20 分</span>
                    </div>
                    <div class="config-item">
                        <span class="config-label">检测方式</span>
                        <span class="config-value">Playwright 真实浏览器</span>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 用户意图类型说明 -->
        <div class="card">
            <h2>🧠 用户意图类型说明</h2>
            <p style="color: #64748b; margin-bottom: 20px;">V3 核心：识别用户真正意图，精准匹配解决方案</p>
            
            <div class="intent-analysis">
                {intent_types_rows}
            </div>
        </div>
        
        <!-- 底部 -->
        <div class="footer">
            <p>Generated by Profit Hunter ULTIMATE V3 | {timestamp}</p>
            <p style="margin-top: 8px;">💎 降维打击 > 正面竞争 | 小而美 > 大而全 | 真需求 > 伪需求</p>
        </div>
    </div>
</body>
</html>'''
    
    # 保存文件
    if output_path is None:
        output_path = Path(__file__).parent / 'data' / 'profit_hunter_report.html'
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_path, len(build_now), len(watch), len(drop)


def main():
    """主函数"""
    print("=" * 80)
    print("💎 Profit Hunter ULTIMATE V3 - HTML 报告生成")
    print("=" * 80)
    
    # 准备测试数据
    gpts = GPTsAnalyzer()
    
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
        ' how to fix pivot table error',
        'fast battery health checker iphone',
        'free online video editor no watermark',
        'color palette generator from image',
        'website seo checker free online',
        'youtube thumbnail maker free online',
        'instagram story viewer anonymous free',
        'pdf to word converter online free',
    ]
    
    # 生成 GPTs 数据
    print("\n📊 生成 GPTs 对比数据...")
    gpts_data = {}
    for kw in keywords:
        gpts_result = gpts.analyze({kw: {'keyword': kw}})
        if kw in gpts_result:
            gpts_data[kw] = gpts_result[kw]
    
    # 评分
    print("🎯 执行关键词评分...")
    scorer = KeywordScorer({}, gpts_data, {})
    results = scorer.score(keywords)
    final_results = scorer.get_final_results(results)
    
    # 生成报告
    print("📄 生成 HTML 报告...")
    output_path, build, watch, drop = generate_report(final_results)
    
    print("\n" + "=" * 80)
    print("✅ 报告生成完成！")
    print("=" * 80)
    print(f"\n📄 报告路径: {output_path}")
    print(f"📊 总关键词: {len(final_results)}")
    print(f"🔴 BUILD NOW: {build} 个")
    print(f"🟡 WATCH: {watch} 个")
    print(f"❌ DROP: {drop} 个")
    print("\n💡 在浏览器中打开 HTML 文件查看完整报告")
    
    return output_path


if __name__ == "__main__":
    main()
