# Profit Hunter ULTIMATE V4 - 蓝海关键词智能猎取系统

## 核心能力

### 1. 需求真伪识别 (Demand Validation) - 5问法

不再只看热度，而是用5个问题验证需求是否真实：

```
Q1: 是 Info 还是 Transactional 意图?
   - Transactional (工具/解决方案) → ✅
   - Info (只是看看) → ⚠️ 降权

Q2: 是否有工具/解决方案信号?
   - tool, app, software, generator → ✅

Q3: 用户是否在抱怨?
   - struggling with, fix, error, manual → ✅✅ 痛点 = 钱

Q4: 是否有付费意愿?
   - Reddit讨论活跃、solution seeking → ✅

Q5: 竞争是否激烈?
   - 巨头存在 → 🔴 撤退
   - 弱竞争者 (Reddit/博客) → 💎 降维打击机会
```

### 2. 商业价值判断 (Monetization Signal)

区分"止痛药"和"维生素"：

| 类型 | 信号词 | 商业价值 |
|------|--------|----------|
| 止痛药 | fix, error, broken, struggling | ⭐⭐⭐ 高客单价 |
| 维生素 | how to, guide, tutorial | ⭐ 低客单价 |
| B2B | bulk, API, export, team | ⭐⭐⭐ 高客单价 |
| 工具 | tool, generator, converter | ⭐⭐ 中等 |

### 3. GPTS 锚定基准

不再看绝对搜索量，而是和 "GPTs" 基准词对比：

- **5%**: 入门门槛
- **10%**: 好机会
- **20%**: 绝佳机会
- **50%**: 极品机会

### 4. 痛点 = 钱

痛点信号词库 (PAIN_TRIGGERS):

```
critical: struggling with, how to fix, error, broken, not working, manual, tedious
medium: difficult, hard to, looking for, need a tool
fix: fix, repair, recover, solve
```

### 5. 增长黑客策略

- **pSEO 潜力评估**: 检测能否裂变出1000个页面
- **截流建议**: 竞品词直接做对比页
- **降维打击**: 识别前三名是论坛/博客的机会

## 工作流程

```
1. 挖词 (Alphabet Soup)
   ↓
2. 筛选 (痛点识别 + 商业意图)
   ↓
3. 验证 (5问法需求真伪)
   ↓
4. 竞争分析 (SERP 对手是谁?)
   ↓
5. GPTS 锚定 (相对比率)
   ↓
6. 决策 (BUILD NOW / WATCH / DROP)
```

## 评分体系

| 维度 | 权重 | 说明 |
|------|------|------|
| 需求验证 | 25% | 5问法结果 |
| 商业价值 | 25% | B2B/Transactional |
| 痛点深度 | 20% | 痛点信号强度 |
| 竞争环境 | 20% | 弱竞争 = 机会 |
| 趋势 | 10% | 相对 GPTS 比率 |

## 使用方法

```bash
# 基本运行
python3 profit_hunter_ultimate.py

# 启用深度验证
python3 profit_hunter_ultimate.py --deep-search

# 启用 Playwright SERP 分析
python3 profit_hunter_ultimate.py --playwright

# 定时调度器 (每天4次: 00:00, 06:00, 12:00, 18:00)
python3 smooth_scheduler.py
```

## 核心文件

| 文件 | 说明 |
|------|------|
| `config.py` | 配置：痛点词库、商业信号、阈值 |
| `profit_hunter_ultimate.py` | 主程序 |
| `scorer.py` | 评分器 V4：需求验证+商业价值 |
| `deep_search.py` | 深度分析：5问法验证 |
| `serp_analyzer.py` | SERP 竞争分析 |
| `smooth_scheduler.py` | 定时调度器 |
| `generate_report.py` | HTML 报告生成 |
| `words.md` | 种子词列表 |

## 输出示例

```
🔥 Top 1: batch audio to text for journalists free
   需求验证: ✅ Transactional + 痛点
   痛点分数: 85 (critical)
   竞争环境: 🟢 弱 (前三名全是旧博客)
   GPTS对比: 12.5% (远超5%门槛)
   决策: 🔴 BUILD NOW 💎
   变现建议: B2B模式: API服务/企业订阅
```

## 核心理念

> "痛点 = 钱。止痛药比维生素更值钱。"

- 寻找正在抱怨的用户
- 避开巨头把持的领域
- 找到"又老又丑"的竞争对手
- 用现代 UI 实现降维打击
