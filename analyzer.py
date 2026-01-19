import json
from janome.tokenizer import Tokenizer
from collections import Counter
import re

# IT技術用語辞書
TECH_KEYWORDS = {
    # プログラミング言語
    'Python', 'JavaScript', 'TypeScript', 'Java', 'Go', 'Rust', 'C++', 'C#', 'PHP', 
    'Ruby', 'Swift', 'Kotlin', 'Dart', 'Scala', 'R', 'SQL',
    
    # フロントエンド
    'React', 'Vue', 'Angular', 'Next.js', 'Nuxt', 'Svelte', 'jQuery', 'HTML', 'CSS',
    'Tailwind', 'Bootstrap', 'Webpack', 'Vite',
    
    # バックエンド
    'Node.js', 'Express', 'Django', 'Flask', 'FastAPI', 'Spring', 'Rails',
    'Laravel', 'ASP.NET',
    
    # インフラ・クラウド
    'Docker', 'Kubernetes', 'k8s', 'AWS', 'GCP', 'Azure', 'Firebase', 
    'Vercel', 'Netlify', 'Heroku', 'Terraform', 'Ansible',
    
    # データベース
    'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch', 'DynamoDB',
    'Oracle', 'SQLite', 'MariaDB',
    
    # AI・機械学習
    'AI', 'ChatGPT', 'Claude', 'Gemini', 'GPT', 'LLM', 'TensorFlow', 'PyTorch',
    '機械学習', 'ディープラーニング', '深層学習', '自然言語処理', 'NLP',
    
    # セキュリティ
    'セキュリティ', '脆弱性', 'XSS', 'CSRF', 'SQL', 'OAuth', 'JWT', 'HTTPS',
    
    # 開発ツール
    'GitHub', 'GitLab', 'Git', 'VSCode', 'IntelliJ', 'Vim', 'Docker', 'CI/CD',
    'GitHub Actions', 'Jenkins',
    
    # Web技術
    'API', 'REST', 'GraphQL', 'WebSocket', 'HTTP', 'gRPC', 'JSON', 'XML',
    
    # モバイル
    'iOS', 'Android', 'Flutter', 'React Native', 'SwiftUI',
    
    # その他技術トレンド
    'マイクロサービス', 'サーバーレス', 'コンテナ', 'アジャイル', 'DevOps',
    'CI', 'CD', 'テスト駆動開発', 'TDD', 'クラウドネイティブ', 'Edge',
    
    # 企業・サービス名
    'Google', 'Microsoft', 'Apple', 'Amazon', 'Meta', 'Twitter', 'X',
    'OpenAI', 'Anthropic', 'Notion', 'Slack', 'Discord', 'Figma',
    'Cloudflare', 'Stripe'
}

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

def extract_tech_keywords(articles):
    """
    記事タイトルから技術キーワードのみを抽出
    """
    tokenizer = Tokenizer()
    keywords = []
    
    print("\n🔍 技術キーワード抽出中...\n")
    
    for article in articles:
        title = article.get("title", "")
        
        # まずタイトル全体から技術用語辞書に完全一致するものを探す
        for tech_word in TECH_KEYWORDS:
            # 大文字小文字を区別せずに検索
            if tech_word.lower() in title.lower() or tech_word in title:
                keywords.append(tech_word)
        
        # 次に形態素解析で名詞を抽出し、技術用語辞書と照合
        for token in tokenizer.tokenize(title):
            parts = str(token).split("\t")
            if len(parts) >= 2:
                word = parts[0]
                pos = parts[1].split(",")[0]
                
                # 名詞で、技術用語辞書に含まれるもの
                if pos == "名詞" and word in TECH_KEYWORDS:
                    keywords.append(word)
    
    return keywords

def analyze_trending_words(keywords, top_n=15):
    """
    頻出ワードをカウントしてランキング化
    """
    counter = Counter(keywords)
    ranking = counter.most_common(top_n)
    
    print(f"🔥🔥🔥 IT技術トレンドワード TOP{top_n} 🔥🔥🔥\n")
    print("-" * 60)
    
    if not ranking:
        print("⚠️  技術キーワードが見つかりませんでした")
        return []
    
    for rank, (word, count) in enumerate(ranking, 1):
        # ビジュアル的に見やすく
        bar = "█" * min(count, 20)  # 最大20文字
        print(f"{rank:2d}位: {word:20s} {bar} ({count}回)")
    
    print("-" * 60)
    
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
    print("\n" + "=" * 60)
    print("📊 IT技術トレンドワード分析開始")
    print("=" * 60)
    
    # JSONファイルを読み込み
    articles = load_json(json_filename)
    
    if not articles:
        print("⚠️  データがありません")
        return []
    
    print(f"\n📚 {len(articles)}件の記事を分析します")
    
    # 技術キーワード抽出
    keywords = extract_tech_keywords(articles)
    
    print(f"✅ {len(keywords)}個の技術キーワードを抽出しました\n")
    
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