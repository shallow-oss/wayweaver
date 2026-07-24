# WayWeaver AI API 设计草案

文档状态：Draft  
版本：0.1.0  
基础路径：`/api/v1`

## 1. API 约定

### 1.1 格式

- 请求和响应使用 JSON；
- 时间使用包含时区的 ISO 8601；
- 内部统一保存 UTC；
- ID 使用 UUID；
- 金额不使用二进制浮点，使用字符串 Decimal 或最小货币单位；
- 经度、纬度使用 WGS84；
- 列表接口统一分页。

### 1.2 成功响应

单个资源直接返回资源对象：

```json
{
  "id": "...",
  "title": "西安家庭旅行"
}
```

列表：

```json
{
  "items": [],
  "page": 1,
  "page_size": 20,
  "total": 0
}
```

### 1.3 错误响应

```json
{
  "error": {
    "code": "TRIP_NOT_FOUND",
    "message": "Trip was not found",
    "request_id": "..."
  }
}
```

### 1.4 常用状态码

| 状态码 | 用途 |
|---:|---|
| 200 | 查询或修改成功 |
| 201 | 创建成功 |
| 202 | 已接受后台任务 |
| 204 | 删除成功，无响应体 |
| 400 | 请求语义错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 409 | 状态冲突或幂等冲突 |
| 422 | Schema 校验失败 |
| 429 | 超出限流 |
| 503 | 依赖服务不可用 |

## 2. 健康检查

```text
GET /health/live
GET /health/ready
```

## 3. 认证

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
GET  /api/v1/users/me
PATCH /api/v1/users/me
```

### 3.1 用户注册

```http
POST /api/v1/auth/register
Content-Type: application/json
```

请求体：

```json
{
  "email": "student@example.com",
  "password": "a sufficiently long password",
  "display_name": "WayWeaver Student",
  "timezone": "Asia/Shanghai"
}
```

字段规则：

| 字段 | 必填 | 规则 |
|---|---:|---|
| `email` | 是 | 有效邮箱，去除首尾空格并转换为小写 |
| `password` | 是 | 长度 15～128 个字符，不自动去除空格 |
| `display_name` | 是 | 去除首尾空格后长度为 1～100 |
| `timezone` | 否 | 有效 IANA 时区，默认 `Asia/Shanghai` |

成功响应：

```http
HTTP/1.1 201 Created
Content-Type: application/json
```

```json
{
  "id": "52d913cd-ad7a-498d-83b9-0f46f835702e",
  "email": "student@example.com",
  "display_name": "WayWeaver Student",
  "timezone": "Asia/Shanghai",
  "is_active": true,
  "created_at": "2026-07-24T10:30:00Z",
  "updated_at": "2026-07-24T10:30:00Z"
}
```

注册响应不得包含：

- `password`；
- `password_hash`；
- Access Token；
- Refresh Token。

邮箱已经存在：

```http
HTTP/1.1 409 Conflict
Content-Type: application/json
```

```json
{
  "detail": "An account with this email already exists"
}
```

输入校验失败：

```http
HTTP/1.1 422 Unprocessable Entity
```

注册流程：

```text
接收 UserCreate
→ 校验并规范化输入
→ 查询规范化邮箱是否存在
→ 对密码执行安全哈希
→ 创建 User ORM 对象
→ Repository 写入数据库
→ Service 提交事务
→ 转换为 UserResponse
→ 返回 201 Created
```

## 4. Traveler Profile

```text
GET /api/v1/users/me/traveler-profile
PUT /api/v1/users/me/traveler-profile
```

请求示例：

```json
{
  "home_city": "上海",
  "preferred_currency": "CNY",
  "travel_pace": "slow",
  "walking_tolerance_km_per_day": 5,
  "interests": ["历史", "美食"],
  "dietary_preferences": [],
  "accessibility_needs": []
}
```

## 5. Trips

```text
POST   /api/v1/trips
GET    /api/v1/trips
GET    /api/v1/trips/{trip_id}
PATCH  /api/v1/trips/{trip_id}
DELETE /api/v1/trips/{trip_id}
```

创建请求：

```json
{
  "title": "西安家庭旅行",
  "origin": "上海",
  "destination": "西安",
  "start_date": "2026-10-01",
  "end_date": "2026-10-05",
  "travelers": {
    "adults": 2,
    "children": 0,
    "seniors": 2
  },
  "budget": {
    "amount": "12000.00",
    "currency": "CNY"
  }
}
```

## 6. Trip Preferences

```text
GET /api/v1/trips/{trip_id}/preferences
PUT /api/v1/trips/{trip_id}/preferences
```

请求示例：

```json
{
  "interests": ["历史", "文化"],
  "must_visit": ["秦始皇帝陵博物院", "陕西历史博物馆"],
  "avoid_categories": ["高强度徒步"],
  "travel_pace": "slow",
  "preferred_transport_modes": ["subway", "taxi"],
  "daily_start_time": "09:00",
  "daily_end_time": "20:30",
  "walking_tolerance_km_per_day": 5,
  "hotel_preferences": {
    "near_subway": true,
    "max_nightly_price": "600.00"
  }
}
```

## 7. 自然语言需求提取

```text
POST /api/v1/trips/parse-requirements
```

请求：

```json
{
  "message": "我和父母国庆从上海去西安四天，总预算一万二，不想走太多路。"
}
```

响应：

```json
{
  "requirements": {
    "origin": "上海",
    "destination": "西安",
    "start_date": null,
    "end_date": null,
    "travelers": {
      "adults": 1,
      "seniors": 2
    },
    "budget": {
      "amount": "12000.00",
      "currency": "CNY"
    },
    "travel_pace": "slow"
  },
  "missing_fields": [
    "start_date",
    "end_date"
  ],
  "requires_confirmation": true
}
```

## 8. 规划运行

```text
POST /api/v1/trips/{trip_id}/planning-runs
GET  /api/v1/trips/{trip_id}/planning-runs
GET  /api/v1/planning-runs/{run_id}
GET  /api/v1/planning-runs/{run_id}/events
POST /api/v1/planning-runs/{run_id}/cancel
```

启动规划：

```json
{
  "message": "帮我生成一个不要太累的四日行程",
  "base_version_id": null
}
```

响应：

```json
{
  "run_id": "...",
  "status": "queued"
}
```

状态：

```text
queued
running
waiting_for_user
completed
failed
cancelled
```

## 9. SSE 事件

```text
run.queued
run.started
requirements.extracted
clarification.required
tool.started
tool.completed
tool.failed
planning.started
planning.validation_failed
planning.repaired
version.created
run.completed
run.failed
run.cancelled
```

事件格式：

```json
{
  "event_id": "...",
  "type": "tool.completed",
  "run_id": "...",
  "timestamp": "2026-07-23T12:00:00Z",
  "data": {
    "tool_name": "weather.forecast",
    "duration_ms": 325
  }
}
```

## 10. 行程版本

```text
GET  /api/v1/trips/{trip_id}/itinerary-versions
GET  /api/v1/trips/{trip_id}/itinerary-versions/{version_id}
POST /api/v1/trips/{trip_id}/itinerary-versions/{version_id}/activate
GET  /api/v1/trips/{trip_id}/itinerary-versions/{version_id}/diff/{other_version_id}
```

## 11. 对话修改

```text
POST /api/v1/trips/{trip_id}/messages
GET  /api/v1/trips/{trip_id}/messages
```

请求：

```json
{
  "content": "第二天太累了，删掉一个景点，并增加午休。"
}
```

系统行为：

```text
保存用户消息
→ 创建 planning run
→ 读取当前 itinerary version
→ 提取变更
→ 局部重新规划
→ 校验
→ 创建新 version
```

## 12. Provider 调试接口

只在开发环境启用：

```text
GET /api/v1/dev/providers/status
POST /api/v1/dev/providers/weather/test
POST /api/v1/dev/providers/places/test
POST /api/v1/dev/providers/routes/test
```

生产环境不得暴露供应商密钥或原始敏感响应。

## 13. 导出

P1：

```text
POST /api/v1/trips/{trip_id}/exports/pdf
POST /api/v1/trips/{trip_id}/exports/calendar
GET  /api/v1/exports/{export_id}
```

## 14. 幂等性

以下创建接口接受：

```text
Idempotency-Key: <client-generated-key>
```

- 创建 Trip；
- 启动 Planning Run；
- 创建导出任务。

## 15. 权限

Trip 角色：

```text
owner
editor
viewer
```

权限矩阵：

| 操作 | owner | editor | viewer |
|---|---:|---:|---:|
| 查看 Trip | 是 | 是 | 是 |
| 修改偏好 | 是 | 是 | 否 |
| 启动规划 | 是 | 是 | 否 |
| 激活版本 | 是 | 是 | 否 |
| 邀请成员 | 是 | 否 | 否 |
| 删除 Trip | 是 | 否 | 否 |
