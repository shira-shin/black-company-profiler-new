# Black Company Profiler

**企業のデータをワンクリックで診断し、スコアとAIによる解説コメントを返すWeb APIサービス**です。

---

## 📦 概要

- FastAPI で構築した `/profile` エンドポイント  
- e-Stat（総務省統計局）から売上・利益などの統計データ取得  
- Wikipedia や独自検索ツールで背景情報を取得  
- 売上成長率・利益率・情報充実度を正規化・重み付けして総合スコア算出  
- OpenAI GPT モデルで 300 字以内の解説コメントを自動生成  

---

## ⚙️ セットアップ

### 前提条件

- Python 3.11+  
- Git  
- GitHub Actions（CI 用）  

### ローカル開発環境構築

```bash
# リポジトリをクローン
git clone https://github.com/shira-shin/black-company-profiler-new.git
cd black-company-profiler-new

# 仮想環境作成 & アクティベート
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 依存パッケージインストール
pip install --upgrade pip
pip install -r requirements.txt
