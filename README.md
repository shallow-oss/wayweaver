# WayWeaver AI

> A constraint-aware, tool-using intelligent travel planning platform.

WayWeaver AI（中文暂定名：织途）是一个面向自由行用户的开源智能旅行助手。它通过自然语言理解旅行需求，调用地点、路线、天气、航班和酒店等实时工具，使用确定性规划程序生成可执行的多日行程，并支持对话式调整、版本管理、预算计算和来源追踪。

## 项目标识

| 项目 | 建议值 |
|---|---|
| 产品英文名 | WayWeaver AI |
| 产品中文名 | 织途 |
| GitHub 仓库名 | `wayweaver-ai` |
| Python 包名 | `wayweaver` |
| API 服务名 | `wayweaver-api` |
| Worker 服务名 | `wayweaver-worker` |
| 默认分支 | `main` |
| 开源许可证 | Apache License 2.0 |

## 命名说明

“WayWeaver”表达“把地点、路线、时间、预算和偏好编织成一条可执行旅程”的产品含义。快速公开检索未发现明显同名的主流 AI 旅行助手，但这不构成商标法律意见；如果未来商业化，应再进行目标国家或地区的商标和域名检索。

GitHub 仓库名称只需在你的个人账号或组织下唯一。如果 `wayweaver-ai` 在你的账号下尚未使用，即可创建：

```text
https://github.com/<YOUR_USERNAME>/wayweaver-ai
```

## 项目一句话介绍

中文：

> 一个能够理解旅行约束、调用实时工具、生成可执行行程并支持持续修改的智能旅行助手。

英文：

> An open-source travel planning agent that turns user constraints and live provider data into feasible, versioned, and explainable itineraries.

## GitHub About 建议

```text
Constraint-aware AI travel planner with live tools, itinerary optimization, versioning, citations, and human-in-the-loop workflows.
```

建议 Topics：

```text
ai-agent
travel-planner
fastapi
langgraph
postgresql
postgis
llm
tool-calling
itinerary
python
```

## T001 文档

- [产品需求文档](docs/product-requirements.md)
- [系统架构文档](docs/architecture.md)
- [API 设计草案](docs/api-design.md)
- [数据模型设计](docs/data-model.md)
- [实施路线图](docs/implementation-roadmap.md)

## 当前范围

第一版聚焦：

- 中文 Web 应用；
- 中国境内单城市、多日自由行；
- 用户输入目的地、日期、人数、预算和偏好；
- 生成按天、按时间段排列的可执行行程；
- 接入地点、路线和天气实时工具；
- 支持预算估算、冲突检查和对话修改；
- 保存行程版本、工具调用来源和 Agent 运行记录；
- 只做航班、酒店搜索与推荐，不处理支付、出票或真实预订。

## 开源建议

推荐 Apache License 2.0，原因：

- 允许学习、修改、分发和商业使用；
- 包含明确的专利授权条款；
- 适合包含多个服务、Provider 适配器和第三方贡献的项目。

正式提交前还应增加：

```text
LICENSE
CONTRIBUTING.md
CODE_OF_CONDUCT.md
SECURITY.md
.github/ISSUE_TEMPLATE/
.github/PULL_REQUEST_TEMPLATE.md
```

## T001 完成标准

- [x] 确定产品名与仓库名。
- [x] 明确目标用户和第一版范围。
- [x] 明确 P0、P1、P2 功能。
- [x] 明确 LLM、确定性程序和外部工具的职责。
- [x] 给出总体架构与核心工作流。
- [x] 给出 API 和数据模型草案。
- [x] 给出分 Ticket 实施路线图。
- [ ] 用户确认产品范围。
- [ ] 创建 GitHub 仓库。
- [ ] 将本目录中的文档复制到仓库。
- [ ] 创建初始项目骨架，进入 T002。
