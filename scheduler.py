import schedule
import time
import subprocess
from datetime import datetime

def run_scraper():
    """
    スクレイピングを実行する関数
    """
    print(f"\n{'='*60}")
    print(f"⏰ 自動実行開始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    try:
        # main.pyを実行
        result = subprocess.run(
            ['python', 'main.py'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        # 実行結果を表示
        print(result.stdout)
        
        if result.returncode == 0:
            print("\n✅ スクレイピング成功！")
        else:
            print("\n❌ エラーが発生しました")
            print(result.stderr)
            
    except Exception as e:
        print(f"\n❌ 予期しないエラー: {e}")
    
    print(f"\n{'='*60}")
    print(f"⏰ 自動実行終了: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

# スケジュール設定
print("🚀 スケジューラー起動")
print("⏰ 毎朝8時に自動実行します")
print("   (Ctrl+C で停止)\n")

# 毎朝8時に実行
schedule.every().day.at("08:00").do(run_scraper)

# テスト用: 起動後すぐに1回実行したい場合はコメント解除
# run_scraper()

# スケジューラーをずっと動かし続ける
while True:
    schedule.run_pending()
    time.sleep(60)  # 1分ごとにチェック