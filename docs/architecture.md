# アーキテクチャ設計書

## 概要

このプロジェクトは以下の3つの設計思想を組み合わせています:

- **Clean Architecture** — 依存方向を内側に統一し、ビジネスロジックを外部技術から独立させる
- **DDD (Domain-Driven Design)** — ビジネスの概念をそのままコードに反映する
- **Hexagonal Architecture** — ポート（インターフェース）とアダプタ（実装）でシステムの境界を明確にする

---

## 依存方向（最重要ルール）

**依存は常に内側に向かう。外側の層が内側の層に依存する。逆方向は禁止。**

```
┌─────────────────────────────────────────────┐
│  Infrastructure (インフラ層)                  │
│  ┌─────────────────────────────────────────┐ │
│  │  Application (アプリケーション層)          │ │
│  │  ┌─────────────────────────────────────┐ │ │
│  │  │  Domain (ドメイン層)                  │ │ │
│  │  │  ビジネスロジックの核心                │ │ │
│  │  └─────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

```
Infrastructure → Application → Domain
  (外側)           (中間)        (内側)
```

- Domain は何にも依存しない（純粋な Python のみ）
- Application は Domain にのみ依存する
- Infrastructure は Domain と Application に依存する

---

## 各層の責務

### Domain 層（ドメイン層）

**場所**: `src/domain/`

ビジネスロジックの核心。外部ライブラリへの依存は一切なし。

| ファイル | 責務 |
|---------|------|
| `shared/entity_id.py` | 全エンティティ共通の ID 基底クラス（UUID 生成） |
| `task/entity.py` | **Task 集約ルート** — タスクの生成・状態変更などのビジネスロジック |
| `task/value_objects.py` | TaskId, TaskStatus, TaskTitle — イミュータブルな値オブジェクト |
| `task/repository.py` | **TaskRepository ABC (駆動ポート)** — 永続化のインターフェース定義のみ |
| `task/exceptions.py` | ドメイン固有の例外（TaskNotFoundError, TaskValidationError） |

**設計のポイント:**

- **Rich Domain Model**: ビジネスロジックはエンティティのメソッドに持たせる（貧血ドメインモデルの回避）
  - `Task.create()` — タスク生成のビジネスルール
  - `Task.change_status()` — 状態遷移のビジネスルール
  - `Task.update_title()` — タイトル変更のビジネスルール
- **イミュータブル**: 全て `frozen=True` の dataclass。状態変更は新しいインスタンスを返す
- **Value Object**: `TaskTitle` は値で等価性を判定し、バリデーションを内包する

### Application 層（アプリケーション層）

**場所**: `src/application/`

ユースケース（ビジネスの手続き）を定義する。ドメイン層のみに依存。

| ファイル | 責務 |
|---------|------|
| `shared/use_case.py` | **UseCase ABC (ドライバポート)** — ユースケースのインターフェース |
| `task/create_task.py` | タスク作成ユースケース（Command + Handler） |
| `task/get_task.py` | タスク取得ユースケース（Query + Handler） |
| `task/list_tasks.py` | タスク一覧取得ユースケース（Query + Handler） |

**設計のポイント:**

- **Command / Query パターン**: 入力は Command (書き込み) または Query (読み取り) の dataclass
- **Result dataclass**: ドメインエンティティをそのまま返さず、専用の結果型にマッピングする
- ドメインオブジェクトの組み立てとリポジトリの呼び出しを調整する「オーケストレーター」

### Infrastructure 層（インフラストラクチャ層）

**場所**: `src/infrastructure/`

外部技術との接続。FastAPI, データベース, 外部 API などの具体的な実装。

| ファイル | 責務 |
|---------|------|
| `persistence/in_memory_task_repository.py` | **駆動アダプタ** — TaskRepository の In-Memory 実装 |
| `http/task_router.py` | **ドライバアダプタ** — FastAPI ルーター（HTTP → ユースケース変換） |
| `http/schemas/task_schemas.py` | Pydantic スキーマ（リクエスト/レスポンスの型定義） |
| `config/di.py` | **Composition Root** — 全依存関係の配線 |

**設計のポイント:**

- **Composition Root (di.py)**: 依存の組み立ては1箇所に集約。アプリケーション起動時にすべてのインスタンスを生成
- **アダプタパターン**: リポジトリのインターフェース (ドメイン層) を実装し、具体的な永続化手段を隠蔽

---

## ポートとアダプタ（Hexagonal Architecture）

```
                     ┌──────────────┐
  HTTP Request  ──→  │ task_router  │  ──→ ユースケース ──→ ドメインロジック
  (ドライバ側)        │ (ドライバ     │
                     │  アダプタ)    │
                     └──────────────┘
                                           ↓
                     ┌──────────────┐
                     │ InMemory     │  ←── TaskRepository ABC
                     │ Repository   │      (駆動ポート)
                     │ (駆動アダプタ) │
                     └──────────────┘
```

| 種別 | ポート（インターフェース） | アダプタ（実装） |
|------|-------------------------|-----------------|
| ドライバ（入力側） | `UseCase` ABC | `task_router.py`（FastAPI） |
| 駆動（出力側） | `TaskRepository` ABC | `InMemoryTaskRepository` |

---

## TDD 開発フロー

このプロジェクトは **TDD (テスト駆動開発)** で開発しています。

### Red → Green → Refactor サイクル

```
┌─────────┐     ┌─────────┐     ┌───────────┐
│  Red    │ ──→ │  Green  │ ──→ │ Refactor  │ ──→ (繰り返し)
│ テスト   │     │ 最小実装 │     │ きれいに   │
│ を書く   │     │ で通す   │     │ する       │
└─────────┘     └─────────┘     └───────────┘
```

### 各層のテスト戦略

| 層 | テスト種別 | 何をテストするか | 外部依存 |
|----|-----------|---------------|---------|
| Domain | **単体テスト** | エンティティのビジネスロジック、値オブジェクトのバリデーション | なし |
| Application | **単体テスト** | ユースケースのオーケストレーション | InMemory リポジトリ |
| Infrastructure | **統合テスト** | リポジトリの永続化、API エンドポイント | InMemory / TestClient |

### テスト実装の順序

1. **ドメイン層のテスト**: 値オブジェクト → エンティティ
2. **アプリケーション層のテスト**: 各ユースケース
3. **インフラ層のテスト**: リポジトリ実装 → API エンドポイント

### テスト実行

```bash
# 全テスト実行
docker compose exec api uv run pytest

# 詳細出力
docker compose exec api uv run pytest -v

# 特定の層だけ実行
docker compose exec api uv run pytest tests/domain/
docker compose exec api uv run pytest tests/application/
docker compose exec api uv run pytest tests/infrastructure/
```

---

## 新しい機能を追加するときの手順

例: 「タスク削除」機能を追加する場合

### 1. ドメイン層（必要なら）

- 削除に関するビジネスルールがあればエンティティに追加
- 例: 「完了済みタスクは削除不可」→ `Task.validate_deletable()` メソッド

### 2. アプリケーション層

```
1. tests/application/task/test_delete_task.py を書く (Red)
2. src/application/task/delete_task.py を実装 (Green)
3. リファクタ (Refactor)
```

### 3. インフラストラクチャ層

```
1. TaskRepository に delete メソッドを追加 (ABC)
2. InMemoryTaskRepository に実装
3. task_router.py に DELETE /tasks/{id} エンドポイントを追加
4. di.py に DeleteTaskUseCase を追加
```

---

## アンチパターンチェックリスト

新しいコードを書く前に確認してください:

| チェック項目 | OK の基準 |
|-------------|----------|
| ドメイン層に外部ライブラリの import がないか | `dataclass`, `enum`, `abc`, `uuid` のみ許可 |
| エンティティにビジネスロジックがあるか | Service にロジックを書いて Entity がただのデータ入れ物になっていないか |
| リポジトリは集約単位か | テーブル単位やエンティティ単位で作っていないか |
| ユースケースを経由しているか | ルーターからリポジトリを直接呼んでいないか |
| テストを先に書いたか | TDD の Red → Green → Refactor を守っているか |
