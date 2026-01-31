#!/usr/bin/env python3
"""
Profit Hunter ULTIMATE V3 - 平滑消耗调度器
每天 4 次运行：00:00, 06:00, 12:00, 18:00
每次 1 小时深度分析
"""

import schedule
import time
import sys
import logging
from pathlib import Path
from datetime import datetime, timedelta

# 配置日志
log_dir = Path(__file__).parent / 'logs'
log_dir.mkdir(exist_ok=True)
log_file = log_dir / 'scheduler.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TokenBudget:
    """Token 预算控制 - 平滑消耗"""
    
    def __init__(self, max_tokens_per_day=2000000):
        self.max_tokens_per_day = max_tokens_per_day
        self.used_today = 0
        self.last_reset = datetime.now().date()
    
    def check_budget(self, estimated_tokens):
        """检查预算，平滑消耗"""
        today = datetime.now().date()
        
        # 重置每日预算
        if today > self.last_reset:
            self.used_today = 0
            self.last_reset = today
        
        # 如果接近预算限制，延迟执行
        if self.used_today + estimated_tokens > self.max_tokens_per_day:
            remaining = self.max_tokens_per_day - self.used_today
            logger.warning(f'⚠️ Token 预算接近限制，剩余 {remaining} tokens')
            logger.info('💤 等待 1 小时后重试...')
            time.sleep(3600)
            return False
        
        return True
    
    def consume(self, tokens):
        """消耗 token"""
        self.used_today += tokens
        logger.info(f'📊 Token 消耗: {tokens:,} (今日: {self.used_today:,}/{self.max_tokens_per_day:,})')


class SmoothRunner:
    """平滑运行器"""
    
    def __init__(self):
        self.token_budget = TokenBudget(max_tokens_per_day=2000000)
        self.min_interval = 6 * 3600  # 最小间隔 6 小时
        self.last_run = None
        self.run_count = 0
    
    def estimate_tokens(self, num_keywords):
        """估算 token 消耗 - 深度搜索版本"""
        base_tokens = 1000
        per_keyword_tokens = 600  # 深度分析
        return base_tokens + (num_keywords * per_keyword_tokens)
    
    def run_job(self):
        """执行挖掘任务"""
        self.run_count += 1
        now = datetime.now()
        
        # 检查最小间隔
        if self.last_run and (now - self.last_run).total_seconds() < self.min_interval:
            wait_time = self.min_interval - (now - self.last_run).total_seconds()
            logger.info(f'⏰ 距离上次运行不足 6 小时，等待 {wait_time/3600:.1f} 小时...')
            return
        
        logger.info('=' * 80)
        logger.info(f'🚀 Profit Hunter ULTIMATE V3 - 第 {self.run_count} 次运行')
        logger.info(f'⏰ 运行时间: {now.strftime("%Y-%m-%d %H:%M:%S")}')
        logger.info('=' * 80)
        
        # 估算 token 消耗
        estimated_tokens = self.estimate_tokens(200)
        logger.info(f'📊 预估 Token 消耗: {estimated_tokens:,}')
        
        # 检查预算
        if not self.token_budget.check_budget(estimated_tokens):
            logger.warning('⏸️  跳过本次运行（Token 预算不足）')
            return
        
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            from profit_hunter_ultimate import run_pipeline
            
            class Args:
                trends = True
                playwright = True
                deep_search = True  # ✅ 深度社区搜索
                max = 200
                trends_only = False
                quiet = False
            
            args = Args()
            
            # 执行挖掘
            results = run_pipeline(args)
            
            # 统计 BUILD NOW
            build_now = [r for r in results if 'BUILD NOW' in r.get('decision', '')]
            
            # 实际消耗
            actual_tokens = self.estimate_tokens(len(results))
            self.token_budget.consume(actual_tokens)
            
            logger.info('\n' + '=' * 80)
            logger.info('✅ 本次运行完成！')
            logger.info(f'   发现 {len(build_now)} 个 BUILD NOW 机会')
            logger.info(f'   实际 Token 消耗: {actual_tokens:,}')
            logger.info('=' * 80)
            
            self.last_run = now
            
            # 生成简短报告
            self._send_summary(build_now)
            
        except Exception as e:
            logger.error(f'❌ 运行失败: {e}')
            import traceback
            traceback.print_exc()
    
    def _send_summary(self, build_now):
        """发送简短总结"""
        if not build_now:
            return
        
        logger.info('\n🔥 本次 Top 5 机会：')
        for i, kw in enumerate(build_now[:5], 1):
            logger.info(f'   {i}. {kw["keyword"]} ({kw["final_score"]}分)')
            logger.info(f'      意图: {kw.get("user_intent", "N/A")} | 目标: {kw.get("user_goal", "")}')


def main():
    """主函数"""
    print('=' * 80)
    print('💎 Profit Hunter ULTIMATE V3 - 深度分析调度器')
    print('=' * 80)
    print('\n⏰ 计划任务：每天 4 次（00:00, 06:00, 12:00, 18:00）')
    print('📊 Token 预算：每日 2,000,000 tokens（深度详细搜索）')
    print('🛡️  保护措施：预算不足自动延迟执行')
    print('\n按 Ctrl+C 停止\n')
    
    runner = SmoothRunner()
    
    # 设置固定时间调度（00:00, 06:00, 12:00, 18:00）
    schedule.every().day.at("00:00").do(runner.run_job)
    schedule.every().day.at("06:00").do(runner.run_job)
    schedule.every().day.at("12:00").do(runner.run_job)
    schedule.every().day.at("18:00").do(runner.run_job)
    
    logger.info('📅 调度器已启动！运行时间：')
    logger.info('   • 00:00 (深夜)')
    logger.info('   • 06:00 (早晨)')
    logger.info('   • 12:00 (中午)')
    logger.info('   • 18:00 (傍晚)')
    logger.info('')
    
    # 立即运行一次（首次）
    logger.info('\n🎯 立即执行首次挖掘...')
    runner.run_job()
    
    # 主循环
    logger.info('\n⏳ 等待下次运行时间...')
    while True:
        schedule.run_pending()
        time.sleep(60)
        
        # 显示下次运行时间
        next_run = schedule.next_run()
        if next_run:
            wait = (next_run - datetime.now()).total_seconds()
            if wait > 0 and wait < 3600:
                print(f'\r⏰ 下次运行: {next_run.strftime("%Y-%m-%d %H:%M")} ({wait/60:.0f}分钟后)', end='', flush=True)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n⏹️  调度器已停止')
        sys.exit(0)
