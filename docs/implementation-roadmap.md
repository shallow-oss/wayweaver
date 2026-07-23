# WayWeaver AI 实施路线图

文档状态：Draft  
版本：0.1.0  
开发方式：Vertical Slice + Engineering Tickets

## 1. 推进规则

每个 Ticket 必须完成：

```text
需求与验收条件
→ API/数据设计
→ 测试设计
→ 实现
→ 手动验证
→ Code Review
→ 文档更新
→ Git 提交
```

未通过验收时不叠加下一个复杂模块。

## 2. 第一里程碑：可运行的后端地基

### T002 项目骨架、配置与健康检查

交付：

- FastAPI；
- Pydantic Settings；
- PostgreSQL/PostGIS；
- SQLAlchemy；
- Alembic；
- `/health/live`；
- `/health/ready`；
- pytest；
- Docker Compose。

验收：

- 数据库可用时 ready 返回 200；
- 数据库不可用时返回 503；
- `.env` 不进入 Git；
- 全新环境可启动。

### T003 User 模型与注册

交付：

- User ORM；
- Alembic migration；
- 注册接口；
- 密码哈希；
- 邮箱唯一约束；
- Repository 与 Service 测试。

### T004 登录与身份认证

交付：

- 登录；
- Access Token；
- Refresh Token 或受控会话；
- `GET /users/me`；
- 认证依赖；
- 未认证和过期测试。

### T005 Trip CRUD

交付：

- Trip 模型；
- 创建、列表、详情、修改、归档；
- 日期、人数和预算校验；
- 所有权校验；
- 分页。

### T006 TravelerProfile 与 TripPreference

交付：

- Profile；
- TripPreference；
- 兴趣、节奏、步行、饮食、酒店偏好；
- 更新和读取接口。

## 3. 第二里程碑：第一个端到端行程闭环

### T007 Provider 接口与 Fake 实现

交付：

- PlacesProvider；
- RoutesProvider；
- WeatherProvider；
- Fake 实现；
- 标准响应 Schema；
- 超时与错误类型。

### T008 旅行需求结构化模型

交付：

- `TravelRequirements`；
- 表单输入转换；
- 自然语言部分先用 Fake Parser；
- 缺失字段检测；
- 用户确认状态。

### T009 候选地点评分

交付：

- 地点标准模型；
- 兴趣匹配；
- 必去优先级；
- 预算匹配；
- 距离惩罚；
- 可解释评分结果。

### T010 行程规划引擎 V1

交付：

- 每日时间窗口；
- 候选地点分配；
- 交通时间；
- 用餐和休息；
- 每日项目排序；
- 固定输入的单元测试。

### T011 冲突验证

交付：

- 时间重叠；
- 营业时间；
- 交通不足；
- 每日过载；
- 预算超限；
- 必去遗漏；
- ValidationIssue 模型。

### T012 行程持久化与版本

交付：

- ItineraryVersion；
- Day；
- Item；
- 创建版本；
- 查询版本；
- 激活版本；
- 版本 diff 基础实现。

第一个可演示闭环：

```text
创建 Trip
→ 保存偏好
→ Fake Places/Routes/Weather
→ Planner 生成行程
→ Validator 检查
→ 保存版本
→ API 返回
```

## 4. 第三里程碑：真实旅行工具

### T013 Open-Meteo Weather Provider

交付：

- 坐标天气查询；
- 日期范围检查；
- 超出预报范围的降级；
- 缓存；
- Fake 与真实实现契约测试。

### T014 高德 Places Provider

交付：

- POI 关键词搜索；
- 地点详情标准化；
- 分类映射；
- 坐标处理；
- 来源和获取时间；
- 限流与错误转换。

### T015 高德 Routes Provider

交付：

- 步行、公交、驾车路线；
- 路线矩阵或批量计算封装；
- 距离和耗时标准化；
- 缓存；
- Provider 故障降级。

### T016 真实数据重新规划

交付：

- 用真实 Places/Routes/Weather 替换 Fake；
- 数据快照；
- 缓存过期；
- 端到端集成测试；
- 演示用西安固定场景。

## 5. 第四里程碑：Agent

### T017 LLM Provider 抽象

交付：

- FakeLLM；
- RealLLM adapter；
- Structured Output；
- Token 和耗时记录；
- 限流与超时。

### T018 自然语言需求提取

交付：

- 文本到 TravelRequirements；
- 缺失字段；
- 用户确认；
- 20 条提取评测样本。

### T019 手写 Tool Calling Loop

交付：

- Tool Registry；
- 参数 Schema；
- 最大轮数；
- 工具白名单；
- 错误回传；
- Run 与 ToolCall 记录。

### T020 LangGraph 工作流

交付：

- State；
- Nodes；
- Conditional Edges；
- Checkpoint；
- Human-in-the-loop；
- 取消；
- 失败恢复。

### T021 SSE 运行事件

交付：

- Planning Run；
- 事件队列；
- SSE；
- 心跳；
- 客户端断开；
- 取消接口。

## 6. 第五里程碑：对话修改

### T022 Conversation 与 Message

交付：

- 会话；
- 消息保存；
- Trip 上下文；
- 历史截断策略。

### T023 变更提取

交付：

- 用户修改文本转结构化 Patch；
- 修改范围识别；
- 无关日期保护；
- 变更确认。

### T024 局部重新规划

交付：

- 基于当前版本重新规划；
- 保留未受影响行程项；
- 重新验证；
- 新版本；
- 变更摘要。

## 7. 第六里程碑：增强工具

### T025 航班搜索

- Amadeus Flight Provider；
- 搜索和标准化；
- 价格时间戳；
- 不做出票。

### T026 酒店搜索

- Amadeus Hotel Provider；
- 地理与预算过滤；
- 价格时间戳；
- 不做支付。

### T027 预算引擎

- 分类预算；
- 真实与估算标识；
- 超预算修复建议；
- 汇率接口。

### T028 OR-Tools 优化

- 时间窗口；
- 必选地点；
- 路线成本；
- 求解时间限制；
- 与 V1 规划结果比较。

## 8. 第七里程碑：前端

### T029 Web 基础

- 登录；
- Trip 列表；
- 创建 Trip；
- 偏好表单。

### T030 对话和事件流

- Chat UI；
- SSE；
- 工具进度；
- 用户确认。

### T031 行程和地图

- 按天时间轴；
- 地图 Marker；
- 路线；
- 预算；
- 天气；
- 来源。

### T032 版本与导出

- 版本列表；
- Diff；
- 恢复；
- PDF；
- Calendar。

## 9. 第八里程碑：工程化和开源

### T033 日志与指标

- request_id；
- run_id；
- 结构化日志；
- Provider 指标；
- Token 和费用。

### T034 幂等与可靠性

- Idempotency-Key；
- Retry；
- Circuit Breaker 基础；
- 分布式锁；
- 故障注入。

### T035 安全

- RBAC；
- SSRF 防护；
- 日志脱敏；
- Prompt Injection 测试；
- 工具权限；
- 依赖扫描。

### T036 CI/CD 与部署

- Ruff；
- pytest；
- coverage；
- GitHub Actions；
- Docker 镜像；
- 演示环境部署。

### T037 开源治理

- LICENSE；
- CONTRIBUTING；
- SECURITY；
- Issue Template；
- PR Template；
- Code of Conduct；
- Roadmap；
- Release Notes。

### T038 求职作品集

- README 架构图；
- 3～5 分钟演示；
- 固定演示数据；
- 评测报告；
- 技术难点说明；
- 简历项目描述；
- `v1.0.0` Release。

## 10. 当前下一步

T001 文档确认后，只进入 T002：

```text
项目骨架
配置管理
PostgreSQL/PostGIS
SQLAlchemy
Alembic
健康检查
pytest
Docker Compose
```

此时不接入 LLM，不接入地图 API，不实现 Agent。
