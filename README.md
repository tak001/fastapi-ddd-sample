# FastAPI + Clean Architecture + DDD サンプルプロジェクト

FastAPI を使った Web API のテストプロジェクトです。
Clean Architecture + DDD (Domain-Driven Design) + Hexagonal Architecture で設計しています。

Docker を使うのでローカル環境を汚しません。

---

## 前提条件

以下がインストールされていることを確認してください。

| ツール | 確認コマンド | インストール方法 |
|--------|-------------|----------------|
| Docker | `docker --version` | [Docker Desktop](https://www.docker.com/products/docker-desktop/) |
| Docker Compose | `docker compose version` | Docker Desktop に同梱 |

> **Python のインストールは不要です。** すべて Docker コンテナ内で動きます。

---

## セットアップ（初回のみ）

```bash
# 1. プロジェクトディレクトリに移動
cd fastapi-ddd-sample

# 2. Docker イメージをビルドして起動
docker compose up --build
```

以下のログが出れば成功です:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Started reloader process
```

---

## API を使ってみる

サーバーが起動したら、別のターミナルを開いて試してみましょう。

### ヘルスチェック

```bash
curl http://localhost:8000/health
```

レスポンス:
```json
{"status": "ok"}
```

### タスクを作成する

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "牛乳を買う", "description": "スーパーで低脂肪乳"}'
```

レスポンス:
```json
{
  "id": "a1b2c3d4...",
  "title": "牛乳を買う",
  "description": "スーパーで低脂肪乳",
  "status": "todo"
}
```

### タスク一覧を取得する

```bash
curl http://localhost:8000/tasks
```

### 特定のタスクを取得する

```bash
curl http://localhost:8000/tasks/{上で返ってきたid}
```

### Swagger UI (API ドキュメント)

ブラウザで以下を開くと、API を GUI で試せます:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## テストを実行する

```bash
# コンテナ内でテストを実行
docker compose exec api uv run pytest

# 詳細な出力
docker compose exec api uv run pytest -v
```

---

## 開発の流れ

### TDD (テスト駆動開発) で開発します

```
1. Red    — 失敗するテストを書く
2. Green  — テストが通る最小限のコードを書く
3. Refactor — コードをきれいにする
```

### ホットリロード

`src/` 配下のファイルを編集すると、サーバーが自動で再起動します。
Docker を再ビルドする必要はありません。

### よく使うコマンド

| やりたいこと | コマンド |
|-------------|---------|
| サーバー起動 | `docker compose up` |
| 初回 or Dockerfile変更後 | `docker compose up --build` |
| バックグラウンドで起動 | `docker compose up -d` |
| ログを見る | `docker compose logs -f` |
| テスト実行 | `docker compose exec api uv run pytest` |
| サーバー停止 | `docker compose down` |
| コンテナに入る | `docker compose exec api bash` |

---

## ディレクトリ構成

```
fastapi-ddd-sample/
├── Dockerfile              # コンテナ定義
├── docker-compose.yml      # ローカル開発用
├── pyproject.toml          # Python プロジェクト設定
├── src/
│   ├── main.py             # エントリポイント
│   ├── domain/             # ドメイン層 (ビジネスロジック)
│   ├── application/        # アプリケーション層 (ユースケース)
│   └── infrastructure/     # インフラ層 (API, DB, 外部連携)
├── tests/                  # テストコード
└── docs/
    └── architecture.md     # アーキテクチャ詳細
```

各層の詳しい説明は [docs/architecture.md](docs/architecture.md) を参照してください。

---

## トラブルシューティング

### ポート 8000 が使用中

```bash
# 使用中のプロセスを確認
lsof -i :8000

# docker-compose.yml のポートを変更
ports:
  - "8001:8000"  # ← 8001 に変更
```

### Docker イメージの再ビルド

`pyproject.toml` を変更した場合は再ビルドが必要です:

```bash
docker compose up --build
```
