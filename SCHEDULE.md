# Profit Hunter ULTIMATE V3 - 定时任务配置
# ==========================================

## 方案 1：使用平滑调度器（推荐）
# ------------------------------

# 启动平滑调度器（每 8 小时，平滑消耗 token）
cd /root/clawd/skills/profit-hunter-ultimate/scripts
nohup python3 smooth_scheduler.py > scheduler_output.log 2>&1 &

# 查看运行状态
ps aux | grep smooth_scheduler

# 查看日志
tail -f logs/scheduler.log


## 方案 2：使用 Crontab（简单可靠）
# ---------------------------------

# 编辑 crontab
crontab -e

# 添加以下行（每 8 小时运行）
# 分 时 日 月 周
0 */8 * * * cd /root/clawd/skills/profit-hunter-ultimate/scripts && python3 profit_hunter_ultimate.py >> logs/cron.log 2>&1

# 示例：每天 0:00, 8:00, 16:00 运行
# 0 0,8,16 * * * cd /root/clawd/skills/profit-hunter-ultimate/scripts && python3 profit_hunter_ultimate.py >> logs/cron.log 2>&1


## 方案 3：Systemd 服务（生产环境推荐）
# ------------------------------------

# 创建服务文件 /etc/systemd/system/profit-hunter.service
[Unit]
Description=Profit Hunter ULTIMATE V3 - 蓝海关键词挖掘
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/clawd/skills/profit-hunter-ultimate/scripts
ExecStart=/usr/bin/python3 smooth_scheduler.py
Restart=always
RestartSec=10
Environment=TOKEN_LIMIT=50000

[Install]
WantedBy=multi-user.target

# 启用并启动服务
systemctl daemon-reload
systemctl enable profit-hunter
systemctl start profit-hunter

# 查看状态
systemctl status profit-hunter

# 查看日志
journalctl -u profit-hunter -f


## Token 消耗控制
# ---------------

# 每日预算：50,000 tokens
# 每次运行预估：8,000 tokens
# 每日可运行：6 次（但调度器设置为 8 小时 1 次 = 3 次）

# 如果 token 不足，调度器会自动：
# 1. 延迟 1 小时后重试
# 2. 跳过本次运行
# 3. 记录警告日志


## 日志位置
# ---------

logs/
├── scheduler.log     # 平滑调度器日志
├── cron.log          # Crontab 日志
└── profit_hunter_ultimate.log  # 主程序日志
