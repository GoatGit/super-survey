# CODEX.md

本项目使用公共 AI 开发规则模块：`.agents-rules/`。

## 基本规则

- 使用中文回答问题
- 新增和修改接口时必须同步更新接口契约（如 OpenAPI、路由 schema、shared DTO 类型）；叙述型文档变更需先确认
- 禁止主动编写叙述型文档，除非遇到重大改动并先询问是否需要；文档放项目约定目录
- 添加新功能时，如要求保留旧版本，需形成版本说明
- 修改前确保获取足够上下文，删除或修改功能需确保所有引用位置都已更新
- 禁止随意修改用户展示页面，需获得允许并充分评估后再修改
- 更改路由等逻辑时不要修改页面排版
- 复杂或跨模块新功能落地前需先进行技术架构设计，确认后再实现；小型局部修改可直接实施

## 公共规则

- [架构设计](.agents-rules/rules/architecture.md) - 分层架构、双层模型、Repository 接口、类型单一来源
- [编码规范](.agents-rules/rules/coding-standards.md) - 硬编码规范、边界日志、日志规范、错误处理、错误码与状态码
- [数据库规范](.agents-rules/rules/database.md) - 外键约束、软删除、审计字段、乐观锁、JSONB 写入、查询优化
- [API 规范](.agents-rules/rules/api-standards.md) - 字段命名、DTO 类型、输入验证、响应格式
- [安全规范](.agents-rules/rules/security.md) - 多租户隔离、执行上下文隔离、限流、SSE 连接限制
- [并发规范](.agents-rules/rules/concurrency.md) - Redis 原子操作、异步批量、资源关闭、重试策略、失败清理
- [测试规范](.agents-rules/rules/testing.md) - 覆盖率目标、测试隔离、安全测试、并发安全测试
- [前端规范](.agents-rules/rules/frontend.md) - Mock 清理、SSE 事件、Hook 封装、长操作反馈
- [部署规范](.agents-rules/rules/deployment.md) - Docker 镜像、服务安全、健康检查、优雅关闭
- [反模式清单](.agents-rules/rules/anti-patterns.md) - 禁止的常见反模式、实现对齐审查原则

## 可选工具规则

如果本项目启用了 code-review-graph，请同时遵守：

- [code-review-graph](.agents-rules/rules/tools/code-review-graph.md)

## 项目补充规则

如果存在 `AGENTS.local.md`，其中规则优先于公共规则，用于记录项目特有约束。
