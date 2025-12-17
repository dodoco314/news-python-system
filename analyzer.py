import json
from janome.tokenizer import Tokenizer
from collections import Counter
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

def extract_keywords(articles):
    """
    記事タイトルから名詞キーワードを抽出
    """
    tokenizer = Tokenizer()
    keywords = []
    
    # ストップワード（除外する単語）- 強化版
    stop_words = {
        # 一般的な語
        "こと", "これ", "それ", "もの", "ため", "よう", "とき", 
        "ところ", "みたい", "する", "なる", "ある", "いる", "できる",
        "さん", "つ", "の", "記事", "紹介", "解説", "まとめ", "方法",
        "場合", "理由", "話", "内容", "結果", "情報", "サービス",
        # 曖昧な語
        "たち", "可能", "サイト", "ブログ", "エントリ", "投稿",
        "世界", "今回", "最近", "自分", "みんな", "人", "方",
        # プラットフォーム名（Qiitaなど除外したい場合）
        "Qiita", "BLOG", "ブログ"
    }
    
    print("\n🔍 キーワード抽出中...\n")
    
    for article in articles:
        title = article.get("title", "")
        
        # 形態素解析
        for token in tokenizer.tokenize(title):
            # トークン情報を分割
            parts = str(token).split("\t")
            if len(parts) >= 2:
                word = parts[0]  # 単語
                pos = parts[1].split(",")[0]  # 品詞
                
                # フィルタリング条件
                # 1. 名詞であること
                # 2. 2文字以上
                # 3. ストップワードでない
                # 4. 数字だけではない
                # 5. 記号を含まない
                if (pos == "名詞" and 
                    len(word) >= 2 and 
                    word not in stop_words and
                    not word.isdigit() and
                    not re.search(r'[!-/:-@[-`{-~]', word)):
                    keywords.append(word)
    
    return keywords

def analyze_trending_words(keywords, top_n=15):
    """
    頻出ワードをカウントしてランキング化
    """
    counter = Counter(keywords)
    ranking = counter.most_common(top_n)
    
    print(f"🔥🔥🔥 急上昇ワード TOP{top_n} 🔥🔥🔥\n")
    print("-" * 50)
    
    if not ranking:
        print("⚠️  キーワードが見つかりませんでした")
        return []
    
    for rank, (word, count) in enumerate(ranking, 1):
        # ビジュアル的に見やすく
        bar = "█" * count
        print(f"{rank:2d}位: {word:20s} {bar} ({count}回)")
    
    print("-" * 50)
    
    return ranking

def save_trending_words(ranking, filename="trending_words.json"):
    """
    急上昇ワードをJSONで保存
    """
    data = [{"rank": i+1, "word": word, "count": count} 
            for i, (word, count) in enumerate(ranking)]
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ {filename} に保存しました！")

def analyze_from_json(json_filename="hatena_ranking.json", top_n=15):
    """
    JSONファイルから読み込んで分析（外部から呼び出し用）
    """
    print("\n" + "=" * 50)
    print("📊 急上昇ワード分析開始")
    print("=" * 50)
    
    # JSONファイルを読み込み
    articles = load_json(json_filename)
    
    if not articles:
        print("⚠️  データがありません")
        return []
    
    print(f"\n📚 {len(articles)}件の記事を分析します")
    
    # キーワード抽出
    keywords = extract_keywords(articles)
    
    print(f"✅ {len(keywords)}個のキーワードを抽出しました\n")
    
    # 急上昇ワードランキング
    ranking = analyze_trending_words(keywords, top_n=top_n)
    
    # JSONに保存
    if ranking:
        save_trending_words(ranking)
    
    print("\n🎉 分析完了！\n")
    
    return ranking

def main():
    """
    単体実行用のメイン処理
    """
    analyze_from_json()

if __name__ == "__main__":
    main()