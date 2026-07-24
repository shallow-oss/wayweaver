# WayWeaver Local Development Guide

本文档说明如何在本地启动、验证、测试和停止 WayWeaver 后端开发环境。

## 1. 项目结构

```text
wayweaver/
├── docs/                       # 项目文档
├── migrations/                 # Alembic 数据库迁移
│   └── versions/               # 数据库迁移版本
├── src/
│   └── wayweaver/              # Python 应用包
│       ├── api/                # API 路由
│       ├── core/               # 配置与核心组件
│       ├── db/                 # 数据库 Engine 和 Session
│       ├── models/             # SQLAlchemy ORM 模型
│       ├── schemas/            # Pydantic Schema
│       └── main.py             # FastAPI 应用入口
├── tests/                      # 自动化测试
├── .env.example                # 环境变量示例
├── .gitignore                  # Git 忽略规则
├── alembic.ini                 # Alembic 配置
├── compose.yaml                # 本地基础设施
├── pytest.ini                  # pytest 配置
├── README.md                   # 项目说明
└── requirements.txt            # Python 依赖
```

## 2. 进入项目目录

后续命令默认在项目根目录执行：

```powershell
cd E:\GitHub\wayweaver
```

确认当前目录：

```powershell
Get-Location
```

预期路径：

```text
E:\GitHub\wayweaver
```

## 3. 激活 Conda 环境

```powershell
conda activate wayweaver
```

检查当前 Python：

```powershell
python --version
Get-Command python
```

预期使用 `wayweaver` Conda 环境中的 Python 3.12。

## 4. 准备环境变量

### 4.1 创建 `.env`

第一次运行项目时，从示例文件复制本地配置：

```powershell
Copy-Item .env.example .env
```

如果 `.env` 已经存在，则不需要重复复制。

### 4.2 环境变量说明

推荐的 `.env.example` 内容：

```env
# Application
WAYWEAVER_APP_NAME=WayWeaver
WAYWEAVER_APP_ENV=development
WAYWEAVER_DEBUG=false

# PostgreSQL container initialization
POSTGRES_DB=wayweaver
POSTGRES_USER=wayweaver
POSTGRES_PASSWORD=wayweaver

# Application infrastructure
WAYWEAVER_DATABASE_URL=postgresql+psycopg://wayweaver:wayweaver@localhost:5432/wayweaver
WAYWEAVER_DATABASE_ECHO=false
WAYWEAVER_REDIS_URL=redis://localhost:6379/0
```

配置分为两类。

Docker 使用下面的配置初始化 PostgreSQL：

```env
POSTGRES_DB=wayweaver
POSTGRES_USER=wayweaver
POSTGRES_PASSWORD=wayweaver
```

FastAPI 和 SQLAlchemy 使用下面的配置连接 PostgreSQL：

```env
WAYWEAVER_DATABASE_URL=postgresql+psycopg://wayweaver:wayweaver@localhost:5432/wayweaver
```

数据库 URL 的格式：

```text
postgresql+psycopg://用户名:密码@主机:端口/数据库名
```

Docker 初始化配置和数据库 URL 中的用户名、密码、数据库名必须保持一致。

> `.env` 是本地配置文件，可能包含密码和密钥，不应提交到 Git。项目只提交 `.env.example`。

## 5. 启动本地基础设施

WayWeaver 当前使用以下本地基础设施：

- PostgreSQL 17
- PostGIS 3.5
- Redis

启动服务：

```powershell
docker compose up -d
```

查看容器状态：

```powershell
docker compose ps
```

预期能够看到：

```text
db       running/healthy
redis    running/healthy
```

容器刚启动时，健康状态可能暂时显示为：

```text
health: starting
```

等待几秒后重新执行：

```powershell
docker compose ps
```

本地服务地址：

| 服务 | 地址 |
|---|---|
| PostgreSQL/PostGIS | `127.0.0.1:5432` |
| Redis | `127.0.0.1:6379` |

查看容器日志：

```powershell
docker compose logs db
docker compose logs redis
```

持续查看日志：

```powershell
docker compose logs -f db
```

使用 `Ctrl+C` 可以退出日志查看，不会停止容器。

## 6. 执行数据库迁移

### 6.1 升级到最新版本

```powershell
python -m alembic upgrade head
```

该命令会执行尚未运行的数据库迁移。

### 6.2 查看当前迁移版本

```powershell
python -m alembic current
```

当前 T002 阶段的预期结果：

```text
208550e459c5 (head)
```

### 6.3 查看迁移历史

```powershell
python -m alembic history
```

### 6.4 验证 PostGIS

```powershell
docker compose exec db psql -U wayweaver -d wayweaver -c "SELECT PostGIS_Version();"
```

如果成功返回 PostGIS 版本号，说明：

- PostgreSQL 可以正常访问；
- `wayweaver` 数据库已经创建；
- 数据库用户配置正确；
- Alembic 迁移已经执行；
- PostGIS 扩展已经启用。

也可以检查扩展列表：

```powershell
docker compose exec db psql -U wayweaver -d wayweaver -c "\dx"
```

## 7. 启动 FastAPI

项目采用 `src` 目录结构，因此启动时需要通过 `--app-dir src` 指定 Python 应用目录。

```powershell
python -m uvicorn wayweaver.main:app --reload --app-dir src
```

参数说明：

```text
wayweaver.main:app
│         │    └── main.py 中创建的 FastAPI app 对象
│         └── main.py 模块
└── wayweaver Python 包
```

`--reload` 表示开发过程中代码发生变化时，Uvicorn 自动重新加载应用。

`--app-dir src` 表示将 `src` 加入 Python 模块搜索路径。

启动成功后应该看到：

```text
Uvicorn running on http://127.0.0.1:8000
Application startup complete.
```

## 8. 本地访问地址

应用启动后可以访问：

| 功能 | 地址 |
|---|---|
| API 根地址 | `http://127.0.0.1:8000` |
| Swagger UI | `http://127.0.0.1:8000/docs` |
| OpenAPI JSON | `http://127.0.0.1:8000/openapi.json` |
| Liveness | `http://127.0.0.1:8000/health/live` |
| Readiness | `http://127.0.0.1:8000/health/ready` |

浏览器可以直接打开：

```text
http://127.0.0.1:8000/docs
```

也可以在新的 PowerShell 终端中执行：

```powershell
curl.exe -i http://127.0.0.1:8000/health/live
curl.exe -i http://127.0.0.1:8000/health/ready
```

## 9. 健康检查

WayWeaver 提供两种不同用途的健康检查。

### 9.1 Liveness

请求：

```http
GET /health/live
```

Liveness 用于判断 FastAPI 应用进程是否存活。

它不会检查数据库或其他外部依赖。

正常响应：

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
{
  "status": "ok"
}
```

即使 PostgreSQL 暂时不可用，只要 FastAPI 进程仍然运行，Liveness 就应该继续返回 `200 OK`。

### 9.2 Readiness

请求：

```http
GET /health/ready
```

Readiness 用于判断应用是否已经准备好接收真实业务请求。

当前实现会执行：

```sql
SELECT 1;
```

该查询用于验证：

- 数据库地址是否正确；
- 数据库端口是否可访问；
- 用户名和密码是否正确；
- SQLAlchemy 能否取得连接；
- PostgreSQL 能否执行查询。

数据库正常时返回：

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
{
  "status": "ok"
}
```

数据库不可用时返回：

```http
HTTP/1.1 503 Service Unavailable
Content-Type: application/json
```

```json
{
  "detail": "Database is not ready"
}
```

## 10. 手动验证 Readiness

### 10.1 数据库正常时

确认数据库容器正常：

```powershell
docker compose ps
```

发送请求：

```powershell
curl.exe -i http://127.0.0.1:8000/health/ready
```

预期状态码：

```text
HTTP/1.1 200 OK
```

### 10.2 模拟数据库故障

停止 PostgreSQL：

```powershell
docker compose stop db
```

检查 Liveness：

```powershell
curl.exe -i http://127.0.0.1:8000/health/live
```

预期状态码：

```text
HTTP/1.1 200 OK
```

检查 Readiness：

```powershell
curl.exe -i http://127.0.0.1:8000/health/ready
```

预期状态码：

```text
HTTP/1.1 503 Service Unavailable
```

### 10.3 恢复数据库

```powershell
docker compose start db
docker compose ps
```

等待数据库恢复为 `healthy` 后，再次请求：

```powershell
curl.exe -i http://127.0.0.1:8000/health/ready
```

预期重新返回：

```text
HTTP/1.1 200 OK
```

## 11. 运行自动化测试

### 11.1 运行全部测试

```powershell
pytest -v
```

### 11.2 只运行健康检查测试

```powershell
pytest tests/test_health.py -v
```

### 11.3 只运行配置测试

```powershell
pytest tests/test_config.py -v
```

### 11.4 只运行数据库基础测试

```powershell
pytest tests/test_database.py -v
```

### 11.5 运行指定测试

```powershell
pytest tests/test_health.py::test_health_ready_returns_ok_when_database_is_available -v
```

健康检查单元测试使用 FastAPI 的依赖覆盖机制：

```python
app.dependency_overrides[get_db] = override_get_db
```

这样可以使用模拟的 `AsyncSession` 测试成功和失败场景，而不依赖真实 PostgreSQL。

真实数据库连接通过手动验收流程单独验证。

## 12. 停止本地环境

### 12.1 停止并删除容器

```powershell
docker compose down
```

该命令会：

- 停止容器；
- 删除容器；
- 保留 PostgreSQL 和 Redis 数据卷。

下次运行：

```powershell
docker compose up -d
```

原有数据仍然存在。

### 12.2 只停止容器

```powershell
docker compose stop
```

恢复容器：

```powershell
docker compose start
```

### 12.3 删除本地数据卷

```powershell
docker compose down -v
```

> 警告：该命令会删除当前 Compose 项目的 PostgreSQL 和 Redis 数据，通常无法恢复。只有在确认本地数据不需要保留时才能使用。

## 13. 常见问题

### 13.1 `No module named 'wayweaver'`

错误示例：

```text
ModuleNotFoundError: No module named 'wayweaver'
```

原因是项目采用 `src` 目录结构，但启动 Uvicorn 时没有指定应用目录。

请在项目根目录执行：

```powershell
python -m uvicorn wayweaver.main:app --reload --app-dir src
```

不要使用：

```powershell
python -m uvicorn src.wayweaver.main:app --reload
```

### 13.2 数据库密码认证失败

错误示例：

```text
password authentication failed for user "wayweaver"
```

检查 `.env` 中以下配置是否一致：

```env
POSTGRES_USER=wayweaver
POSTGRES_PASSWORD=wayweaver
WAYWEAVER_DATABASE_URL=postgresql+psycopg://wayweaver:wayweaver@localhost:5432/wayweaver
```

PostgreSQL 只会在第一次创建数据卷时使用 `POSTGRES_PASSWORD` 初始化用户密码。

如果修改了 `.env`，已有数据库用户的密码不会自动改变。

如果数据库中没有需要保留的数据，可以重新初始化本地数据卷：

```powershell
docker compose down -v
docker compose up -d
```

> 执行前必须确认本地数据库数据可以删除。

### 13.3 PostgreSQL 容器还没有准备好

检查状态：

```powershell
docker compose ps
```

查看日志：

```powershell
docker compose logs db
```

等待数据库状态变为 `healthy` 后，再执行迁移或访问 Readiness。

### 13.4 端口 5432 已被占用

检查端口：

```powershell
Get-NetTCPConnection -LocalPort 5432 -ErrorAction SilentlyContinue
```

如果本机已经运行另一个 PostgreSQL，它可能与 Docker 中的 PostgreSQL 冲突。

同时检查 Docker 端口映射：

```powershell
docker compose ps
docker compose port db 5432
```

### 13.5 Alembic 找不到应用包

请确认：

- 当前终端位于项目根目录；
- `alembic.ini` 中配置了 `prepend_sys_path = src`；
- `src/wayweaver` 目录存在；
- `src/wayweaver/__init__.py` 文件存在。

然后重新执行：

```powershell
python -m alembic upgrade head
```

## 15. 推荐开发启动顺序

每天开始开发时，推荐按照以下顺序操作：

```powershell
cd E:\GitHub\wayweaver
conda activate wayweaver
docker compose up -d
docker compose ps
python -m alembic upgrade head
pytest -v
python -m uvicorn wayweaver.main:app --reload --app-dir src
```

每天完成开发后，可以停止应用，并根据需要停止 Docker 服务：

```powershell
docker compose stop
```

如果希望保留容器运行，可以不执行停止命令。
