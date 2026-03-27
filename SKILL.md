---
name: fastapi-ddd-project
description: >
  FastAPI + Clean Architecture + DDD + Hexagonal Architecture + TDD のプロジェクト開発ガイド。
  このプロジェクトでコードを追加・変更する際は必ずこのスキルに準拠すること。
  Docker でローカル開発環境を構築し、TDD (Red → Green → Refactor) で開発する。
---

# FastAPI + Clean Architecture + DDD + TDD 開発ガイド

このプロジェクトでコードを書く際に **必ず守るべきルール** をまとめたものです。

---

## 絶対ルール（違反禁止）

### 1. 依存方向は内側のみ

```
Adapters       → Application → Domain
Infrastructure → Application → Domain
  (外側)              (中間)      (内側・最重要)
```

- **Domain 層は何にも依存しない**（`dataclass`, `enum`, `abc`, `uuid` のみ許可）
- Application 層は Domain にのみ依存する
- Adapters 層は Application にのみ依存する（Infrastructure への依存は禁止）
- Infrastructure 層は Domain と Application に依存する
- Composition Root（`di.py`）のみが全層を参照できる唯一の例外
- **逆方向の依存は絶対に禁止**

### 2. TDD で開発する（例外なし）

```
Red → Green → Refactor
```

1. **Red**: 失敗するテストを先に書く
2. **Green**: テストが通る最小限のコードを書く
3. **Refactor**: コードをきれいにする（テストは通ったまま）

テストなしのコード追加は禁止。

### 3. Docker 内で開発する

ローカル環境に Python や依存パッケージを直接インストールしない。

```bash
docker compose up --build      # 起動
docker compose exec api uv run pytest  # テスト
```

---

## アーキテクチャ規約

### Domain 層 (`src/domain/`)

**ビジネスロジックの核心。外部ライブラリ依存ゼロ。**

| 要素 | ルール |
|------|--------|
| Entity (集約ルート) | `@dataclass(frozen=True)` で定義。ビジネスロジックをメソッドに持つ（Rich Domain Model） |
| Value Object | `@dataclass(frozen=True)` で定義。値で等価性判定。バリデーションは `__post_init__` |
| Repository | `ABC` でインターフェースのみ定義（実装は Infrastructure 層） |
| Exception | ドメイン固有の例外をここに定義 |

**禁止事項:**
- Pydantic, FastAPI, SQLAlchemy などのインポート
- 可変な状態（`frozen=True` 必須）
- 外部 I/O（DB, HTTP, ファイル操作）

**イミュータブル原則:**
- 状態変更は新しいインスタンスを返す (`dataclasses.replace` を使用)
- `let` 相当のミュータブル変数は使わない

```python
# OK: 新しいインスタンスを返す
def change_status(self, new_status: TaskStatus) -> Task:
    return replace(self, status=new_status)

# NG: 自身を変更する
def change_status(self, new_status: TaskStatus) -> None:
    self.status = new_status  # frozen=True なので不可能だが、設計意図として禁止
```

### Application 層 (`src/application/`)

**ユースケースの定義。Domain 層のみに依存。**

| 要素 | ルール |
|------|--------|
| UseCase ABC | `UseCase[TInput, TOutput]` を継承して実装 |
| Command | 書き込み操作の入力 DTO (`@dataclass(frozen=True)`) |
| Query | 読み取り操作の入力 DTO (`@dataclass(frozen=True)`) |
| Result | ユースケースの出力 DTO（ドメインエンティティを直接返さない） |

**禁止事項:**
- Infrastructure 層のインポート
- HTTP, DB などの具体的な技術への依存
- ドメインエンティティをそのまま外部に返す

### Adapters 層 (`src/adapters/`)

**Interface Adapters。外部世界と Application 層を繋ぐ変換層。**

| 要素 | 配置場所 | 説明 |
|------|---------|------|
| Driving Adapter (HTTP) | `http/` | FastAPI ルーター（HTTP → UseCase 変換） |
| HTTP スキーマ | `http/schemas/` | Pydantic v2 のリクエスト/レスポンス定義 |
| Driven Adapter (Agent) | `agent/` | ChatAgentPort の具体実装（LangGraph など） |

**ルール:**
- Adapters 層は Application 層にのみ依存する
- `infrastructure/` への直接依存は禁止（Composition Root 経由で注入する）
- ルーターはルーティングと Schema 変換のみ行う（ビジネスロジックを書かない）

### Infrastructure 層 (`src/infrastructure/`)

**Frameworks & Drivers。外部技術の具体実装。**

| 要素 | 配置場所 | 説明 |
|------|---------|------|
| Driven Adapter (DB) | `persistence/` | Repository の具体実装 (InMemory, DB など) |
| Agent フレームワーク | `agent/` | LangGraph グラフ・ノード・State の実装 |
| Composition Root | `config/di.py` | **全依存関係の配線はここだけ** |

**Composition Root (di.py) のルール:**
- 依存の組み立ては `di.py` に集約する
- FastAPI の `Depends()` でユースケースを注入する
- 新しいユースケースを追加したら必ず `di.py` にも追加する
- `di.py` は全層（domain/application/adapters/infrastructure）を参照できる唯一の例外

---

## ファイル追加時のチェックリスト

新しい機能を追加するときは以下の順序で作業する:

### 1. テストを書く (Red)

```
tests/{layer}/{aggregate}/test_{feature}.py
```

- テストが **失敗する** ことを確認してから次に進む
- 条件分岐は全てテストする
- 正常系・異常系・境界値をカバーする

### 2. 実装する (Green)

```
Domain 層 → Application 層 → Adapters 層 / Infrastructure 層
```

- テストが **通る最小限のコード** を書く
- 内側の層から順に実装する

### 3. リファクタする (Refactor)

- テストが通ったままコードを整理する
- 命名、責務の分割、重複の除去

### 4. 全テスト実行

```bash
docker compose exec api uv run pytest -v
```

---

## コーディング規約

### Python スタイル

| ルール | 詳細 |
|--------|------|
| 型ヒント | 全ての関数に型ヒントをつける |
| イミュータブル | `frozen=True` dataclass を使う。`let` 相当のミュータブル変数は禁止 |
| マジックナンバー禁止 | 定数に名前をつける (`TITLE_MAX_LENGTH = 100`) |
| 早期リターン | ネストを浅く保つ |
| メソッド名 | 動詞始まり (`create_task`, `find_by_id`) |
| 単一責任 | 1メソッド = 1つの責務 |

### ファイル構成

| ルール | 詳細 |
|--------|------|
| 1ファイル1クラス | 大きなクラスは分割する（Value Object は例外的に1ファイルにまとめてもよい） |
| `__init__.py` | 全パッケージに配置する |
| テストファイル | 実装と同じディレクトリ構造を `tests/` に再現する |

### FastAPI 固有

| ルール | 詳細 |
|--------|------|
| ルーターでロジックを書かない | UseCase を呼ぶだけにする |
| Pydantic は Adapters 層のみ | Domain 層で Pydantic を使わない |
| 例外ハンドラ | ドメイン例外は `main.py` で HTTP ステータスに変換する |
| DI | `Depends()` + `di.py` で注入する |

### Docker 固有

| ルール | 詳細 |
|--------|------|
| ベースイメージ | `python:3.12-slim` を使用 |
| パッケージマネージャ | `uv` を使用 |
| ホットリロード | `src/` をボリュームマウントし `uvicorn --reload` |
| pyproject.toml 変更時 | `docker compose up --build` で再ビルド必須 |

---

## アンチパターン（やってはいけないこと）

| アンチパターン | なぜダメか | 正しい方法 |
|--------------|----------|----------|
| 貧血ドメインモデル | Entity がただのデータ入れ物になる | ビジネスロジックを Entity のメソッドに持たせる |
| Entity 単位の Repository | 集約の境界を壊す | **集約単位で1つの Repository** |
| Domain に Pydantic | インフラ依存が漏洩する | Domain は `dataclass`/`enum`/`ABC` のみ |
| Router から Repository 直呼び | UseCase 層をスキップしている | 必ず UseCase を経由する |
| テストなしの実装 | TDD 違反 | テストを先に書く |
| `di.py` 以外での依存組み立て | 依存関係が散らばる | `di.py` に集約する |
| ミュータブルなエンティティ | 予期しない状態変更が起きる | `frozen=True` + `replace()` |

---

## 新機能追加の具体例

例: 「タスク削除」機能を追加する

### Step 1: Domain 層 (必要なら)

```python
# テスト: tests/domain/task/test_entity.py に追加
def test_completed_task_is_not_deletable(self) -> None:
    task = Task.create(title="Test", description="")
    done_task = task.change_status(TaskStatus.DONE)
    with pytest.raises(TaskValidationError):
        done_task.validate_deletable()
```

```python
# 実装: src/domain/task/entity.py に追加
def validate_deletable(self) -> None:
    if self.status == TaskStatus.DONE:
        raise TaskValidationError("Completed tasks cannot be deleted")
```

### Step 2: Application 層

```python
# テスト: tests/application/task/test_delete_task.py
class TestDeleteTaskUseCase:
    def test_delete_existing_task(self, task_repository, sample_task):
        task_repository.save(sample_task)
        use_case = DeleteTaskUseCase(task_repository)
        use_case.execute(DeleteTaskCommand(task_id=sample_task.id.value))
        assert task_repository.find_by_id(sample_task.id) is None
```

```python
# 実装: src/application/task/delete_task.py
class DeleteTaskUseCase(UseCase[DeleteTaskCommand, None]):
    def execute(self, input_data: DeleteTaskCommand) -> None:
        task = self._task_repository.find_by_id(TaskId(value=input_data.task_id))
        if task is None:
            raise TaskNotFoundError(input_data.task_id)
        task.validate_deletable()
        self._task_repository.delete(task.id)
```

### Step 3: Adapters 層 / Infrastructure 層

1. `TaskRepository` ABC に `delete` メソッドを追加
2. `InMemoryTaskRepository` に実装（`infrastructure/persistence/`）
3. `adapters/http/task_router.py` に `DELETE /tasks/{id}` を追加
4. `di.py` に `DeleteTaskUseCase` を配線

### Step 4: 全テスト実行

```bash
docker compose exec api uv run pytest -v
```

---

## テスト戦略

| 層 | テスト種別 | 外部依存 | 実行速度 |
|----|-----------|---------|---------|
| Domain | 単体テスト | なし | 最速 |
| Application | 単体テスト | InMemory Repository | 速い |
| Adapters | 統合テスト | TestClient / MockUseCase | 普通 |
| Infrastructure | 統合テスト | InMemory / MockLLM | 普通 |

### テストの書き方

```python
# AAA パターン (Arrange-Act-Assert)
class TestCreateTaskUseCase:
    def test_create_task_successfully(self, task_repository: TaskRepository) -> None:
        # Arrange
        use_case = CreateTaskUseCase(task_repository)
        command = CreateTaskCommand(title="Buy groceries", description="Milk")

        # Act
        result = use_case.execute(command)

        # Assert
        assert result.title == "Buy groceries"
        assert result.status == "todo"
```

### テスト命名規則

```
test_{何をテストするか}_{どういう条件で}_{期待する結果}
```

例:
- `test_create_task_with_valid_data`
- `test_create_task_with_empty_title_raises_error`
- `test_get_nonexistent_task_raises_not_found`
