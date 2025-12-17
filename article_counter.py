import json
import requests
from bs4 import BeautifulSoup
import time
import re

def load_json(filename="hatena_ranking.json"):
    """
    JSONファイルを読み込む
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ エラー: {filename} が見つかりません")
        return []
    except json.JSONDecodeError:
        print(f"❌ エラー: {filename} の形式が正しくありません")
        return []

def fetch_article_content(url, headers):
    """
    記事のURLから本文を取得
    """
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # 不要なタグを削除（スクリプト、スタイル、ヘッダー、フッターなど）
        for tag in soup(["script", "style", "header", "footer", "nav", "aside", "iframe"]):
            tag.decompose()
        
        # 本文っぽい要素を探す（優先順位順）
        content = None
        
        # よくある記事本文のclass/id
        article_selectors = [
            "article",
            "[class*='article']",
            "[class*='content']",
            "[class*='post']",
            "[class*='entry']",
            "main",
            "[role='main']"
        ]
        
        for selector in article_selectors:
            content = soup.select_one(selector)
            if content:
                break
        
        # 見つからなかったらbodyから取得
        if not content:
            content = soup.find("body")
        
        if content:
            # テキストを抽出
            text = content.get_text(separator="\n", strip=True)
            
            # 改行を整理
            text = re.sub(r'\n+', '\n', text)
            
            # 空白を整理
            text = re.sub(r' +', ' ', text)
            
            return text
        
        return ""
        
    except requests.exceptions.Timeout:
        print(f"    ⚠️  タイムアウト: {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"    ⚠️  アクセスエラー: {e}")
        return None
    except Exception as e:
        print(f"    ⚠️  予期しないエラー: {e}")
        return None

def count_article_characters(articles, headers):
    """
    各記事の文字数をカウント
    """
    print("\n📏 記事の文字数をカウント中...\n")
    print("-" * 70)
    
    for idx, article in enumerate(articles, 1):
        link = article.get("link", "")
        title = article.get("title", "不明")
        
        print(f"[{idx}/{len(articles)}] {title[:50]}...")
        
        # 記事本文を取得
        content = fetch_article_content(link, headers)
        
        if content is None:
            article["char_count"] = 0
            article["status"] = "取得失敗"
            print(f"    ❌ 取得失敗")
        elif content == "":
            article["char_count"] = 0
            article["status"] = "本文なし"
            print(f"    ⚠️  本文が見つかりませんでした")
        else:
            # 文字数をカウント
            char_count = len(content)
            article["char_count"] = char_count
            article["status"] = "成功"
            
            # 読了時間を推定（400文字/分として計算）
            reading_time = max(1, round(char_count / 400))
            article["reading_time"] = reading_time
            
            print(f"    ✅ {char_count:,}文字 (約{reading_time}分)")
        
        print("-" * 70)
        
        # サーバーに優しく（1秒待機）
        time.sleep(1)
    
    return articles

def save_json(data, filename="hatena_ranking_with_count.json"):
    """
    文字数を含めたデータを保存
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ {filename} に保存しました！")

def display_statistics(articles):
    """
    統計情報を表示
    """
    print("\n" + "=" * 70)
    print("📊 統計情報")
    print("=" * 70)
    
    # 成功・失敗のカウント
    success_count = sum(1 for a in articles if a.get("status") == "成功")
    fail_count = sum(1 for a in articles if a.get("status") == "取得失敗")
    no_content_count = sum(1 for a in articles if a.get("status") == "本文なし")
    
    print(f"✅ 取得成功: {success_count}件")
    print(f"❌ 取得失敗: {fail_count}件")
    print(f"⚠️  本文なし: {no_content_count}件")
    
    # 文字数の統計
    char_counts = [a.get("char_count", 0) for a in articles if a.get("status") == "成功"]
    
    if char_counts:
        avg_chars = sum(char_counts) / len(char_counts)
        max_chars = max(char_counts)
        min_chars = min(char_counts)
        
        print(f"\n平均文字数: {avg_chars:,.0f}文字")
        print(f"最大文字数: {max_chars:,}文字")
        print(f"最小文字数: {min_chars:,}文字")
    
    print("=" * 70)

def count_from_json(json_filename="hatena_ranking.json", output_filename="hatena_ranking_with_count.json"):
    """
    JSONファイルから読み込んで文字数カウント（外部から呼び出し用）
    """
    print("\n" + "=" * 70)
    print("📏 記事文字数カウント開始")
    print("=" * 70)
    
    # ヘッダー設定
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # JSONファイルを読み込み
    articles = load_json(json_filename)
    
    if not articles:
        print("⚠️  データがありません")
        return []
    
    print(f"\n📚 {len(articles)}件の記事の文字数をカウントします")
    print("⏱️  1記事あたり約1秒かかります（サーバーに優しく）")
    
    # 文字数カウント
    articles_with_count = count_article_characters(articles, headers)
    
    # 保存
    save_json(articles_with_count, output_filename)
    
    # 統計表示
    display_statistics(articles_with_count)
    
    print("\n🎉 文字数カウント完了！\n")
    
    return articles_with_count

def main():
    """
    単体実行用のメイン処理
    """
    count_from_json()

if __name__ == "__main__":
    main()