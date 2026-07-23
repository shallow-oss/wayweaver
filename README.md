# WayWeaver AI

> A constraint-aware, tool-using intelligent travel planning platform.

WayWeaver AI（织途）是一个面向自由行用户的开源智能旅行助手。它通过自然语言理解旅行需求，调用地点、路线、天气、航班和酒店等实时工具，使用确定性规划程序生成可执行的多日行程，并支持对话式调整、版本管理、预算计算和来源追踪。

## 项目相关文档

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
