#!/usr/bin/env python3
"""
Profit Hunter ULTIMATE - 定时调度器

Usage:
    python scheduler.py              # 每 6 小时运行一次
    python scheduler.py --interval 12 # 每 12 小时运行一次
    python scheduler.py --immediate  # 立即运行一次

Windows 后台运行:
    start /B python scheduler.py

Linux/Mac 后台运行:
    nohup python scheduler.py > scheduler.log 2>&1 &
"""

import argparse
import schedule
import time
from datetime import datetime
from pathlib import Path
import sys

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from profit_hunter import ProfitHunterUltimate


def job():
    """定时任务：运行关键词分析"""
    print("\n" + "="*60)
    print(f"⏰ 定时任务启动: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    try:
        hunter = ProfitHunterUltimate()
        results = hunter.run(
            use_trends=True,
            use_playwright=True,
            max_keywords=500
        )
        
        # 统计 BUILD NOW 的数量
        build_now = [r for r in results if r["decision"] == "🔴 BUILD NOW"]
        
        print(f"\n✅ 任务完成！发现 {len(build_now)} 个立即做机会")
        
        # 可以在这里添加通知逻辑（邮件、Slack 等）
        # notify_new_opportunities(build_now)
        
    except Exception as e:
        print(f"\n❌ 任务失败: {e}")
        # 可以在这里添加错误通知
        # notify_error(e)
    
    print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(
        description="Profit Hunter ULTIMATE 定时调度器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python scheduler.py                    # 默认每 6 小时运行
    python scheduler.py --interval 12      # 每 12 小时运行
    python scheduler.py --interval 1       # 每 1 小时运行（测试用）
    python scheduler.py --immediate        # 立即运行一次
    python scheduler.py --run-once         # 运行一次后退出（不循环）
        """
    )
    
    parser.add_argument("--interval", type=float, default=6,
                       help="运行间隔（小时），默认 6")
    parser.add_argument("--immediate", action="store_true",
                       help="立即运行一次（然后按间隔继续）")
    parser.add_argument("--run-once", action="store_true",
                       help="只运行一次，不循环")
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("💎 Profit Hunter ULTIMATE - 调度器")
    print("="*60)
    print(f"⏱️  运行间隔: {args.interval} 小时")
    print(f"📋  模式: {'单次运行' if args.run_once else '循环运行'}")
    print("-" * 60)
    
    # 设置定时任务
    schedule.every(args.interval).hours.do(job)
    
    # 立即运行一次（如果指定）
    if args.immediate or args.run_once:
        print("\n🚀 立即执行任务...")
        job()
    
    # 主循环
    if not args.run_once:
        print(f"\n⏳ 等待中... (每 {args.interval} 小时执行一次)")
        print("   按 Ctrl+C 停止\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
        except KeyboardInterrupt:
            print("\n\n⏹️  调度器已停止")
    
    print("\n✅ 完成！")


if __name__ == "__main__":
    main()
