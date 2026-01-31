#!/usr/bin/env python3
"""
定时任务调度器 - 每 6 小时自动运行
"""

import schedule
import time
import sys
from pathlib import Path

# 添加 scripts 目录到 path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from profit_hunter_ultimate import run_pipeline
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='scheduler.log'
)
logger = logging.getLogger(__name__)


def job():
    """定时任务"""
    logger.info("=" * 60)
    logger.info("⏰ 定时任务触发")
    
    class Args:
        trends = True
        playwright = True
        max = 20
        trends_only = False
        quiet = True
    
    try:
        results = run_pipeline(Args())
        
        build_now = [r for r in results if r.get('decision') == 'BUILD NOW']
        logger.info(f"✅ 完成: 发现 {len(build_now)} 个 BUILD NOW 机会")
        
    except Exception as e:
        logger.error(f"❌ 任务失败: {e}")


def main():
    logger.info("🚀 Profit Hunter 调度器启动")
    logger.info("⏰ 计划任务：每 6 小时运行一次")
    logger.info("   时间点: 00:00, 06:00, 12:18:00")
    
    # 设置定时任务
    schedule.every(6).hours.do(job)
    
    # 立即运行一次
    print("\n🎯 立即运行首次扫描...")
    job()
    
    # 主循环
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    print("启动 Profit Hunter 调度器...")
    print("按 Ctrl+C 停止\n")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ 调度器已停止")
        sys.exit(0)
