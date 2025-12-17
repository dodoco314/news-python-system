# ライブラリのインポート
import requests
from bs4 import BeautifulSoup
import time
from file_handler import save_to_json
from analyzer import analyze_from_json

# はてなブックマークのURL
URL = "https://b.hatena.ne.jp/hotentry/it"

# 訪問の連絡呪文
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

print("=" * 60)
print("🚀 はてなブックマーク スクレイピング＆分析ツール")
print("=" * 60)

print("\n📡 はてなブックマークにアクセス中...")
response = requests.get(URL, headers=headers)

# タグを見やすい形に
soup = BeautifulSoup(response.content, "html.parser")

# 記事１個ずつの箱を、全部見つけ出す
entries = soup.find_all("li", class_="cat-it")

# ぜんぶの情報を貯めておくための、空っぽのリストを用意
ranking_data = [] 

print(f"✅ {len(entries)}件の記事を取得しました。処理開始！\n")
print("-" * 60)

# forループで、箱を一個ずつ見ていく
for idx, entry in enumerate(entries, 1):
    
    # h3タグを探す
    h3_tag = entry.find("h3", class_="entrylist-contents-title")
    
    # もし、h3タグが見つかったら…
    if h3_tag:
        # h3タグの中から、aタグを探す！
        a_tag = h3_tag.find("a")
        
        # もし、aタグが見つかったら…
        if a_tag:
            # <a>タグから、「title（記事のタイトル）」を引っこ抜く
            title = a_tag.get("title")
            
            # <a>タグから、「href（記事のリンク）」を引っこ抜く
            link = a_tag.get("href")
            
            # ブックマーク数を抜いてくる
            users_span = entry.find("span", class_="entrylist-contents-users")
            
            # エラーを起こさないように
            if users_span:
                users_text = users_span.find("a").find("span").text
                hatebu_count = int(users_text.replace(" users", ""))
            else:
                hatebu_count = 0
            
            # 投稿日時を抜いてくる
            data_li = entry.find("li", class_="entrylist-contents-date")
            
            if data_li:
                published_date = data_li.text.strip()
            else:
                published_date = ""
            
            # データを辞書にまとめる
            article_data = {
                "title": title,
                "link": link,
                "hatebu_count": hatebu_count,
                "published_date": published_date
            }
            
            # 🔥 ここが重要！ ranking_dataに追加する
            ranking_data.append(article_data)
            
            # 画面表示
            print(f"[{idx}] {title}")
            print(f"    📌 {hatebu_count} users | 🕒 {published_date}")
            print(f"    🔗 {link}")
            print("-" * 60)

# 最終チェック！
print("\n" + "=" * 60)
print("📊 スクレイピング結果サマリー")
print("=" * 60)
print(f"✅ 取得した記事数: {len(ranking_data)}件")
print(f"📁 JSONファイルに保存中...")

# JSONファイルに保存
save_to_json(ranking_data)

print("=" * 60)
print("\n🔥 次は急上昇ワード分析を開始します！\n")

# 🎉 ここで急上昇ワード分析を実行！
trending_words = analyze_from_json("hatena_ranking.json", top_n=15)

print("\n" + "=" * 60)
print("🎊 全ての処理が完了しました！")
print("=" * 60)
print("📄 生成されたファイル:")
print("  - hatena_ranking.json (記事データ)")
print("  - trending_words.json (急上昇ワード)")
print("=" * 60)