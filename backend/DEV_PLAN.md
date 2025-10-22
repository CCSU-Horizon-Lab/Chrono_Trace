# ChatMind 后端开发计划手册

适用对象：后端/Python 工程师
目标：基于 PyWebView 的本地桌面应用后端骨架，提供数据持久化、业务服务与 JS Bridge。

一、总体架构
- 运行形态：本地桌面应用（无对外 REST 端口），通过 PyWebView JS API 与前端通信。
- 技术栈：Python 3.10+、PyWebView、SQLite3（后续可引入 SQLAlchemy 或 sqlite-utils）。
- 目录结构：
  - `backend/app/main.py` 启动入口，创建窗口并注册 `Bridge`
  - `backend/app/webview/bridge.py` 暴露前端可调用的方法
  - `backend/app/services/` 业务服务（无状态/可测试）
  - `backend/app/db/` 数据库连接、建表与仓储
  - `backend/requirements.txt` 依赖

二、通信约定（JS Bridge）
- 桥接类：`Bridge`
- 方法命名与返回：
  - 所有方法小写 + 下划线；参数与返回均为可 JSON 化对象
  - 标准返回：`{"ok": true, "data": any}` 或直接返回数据结构（当前骨架为直接返回）
- 首批接口（占位，后续落库/落服务）：
  - `ping() -> str`：连通性检查
  - `ingest_data(file_path: str, options: dict) -> dict`：导入聊天记录（后续接入清洗/入库）
  - `get_analysis(date_range: {from: str, to: str}) -> dict`：统计数据（后续接入聚合）
  - `generate_suggestion(intent: str, context: dict) -> dict`：AI 建议（后续接入 LLM）
  - `get_settings() / set_settings(payload)`：读取/保存配置

三、数据库设计（里程碑 M2 落地）
- 初版表：
  - `conversations(id, name, platform, created_at)`
  - `messages(id, conversation_id, role, ts, content, emotion)`
  - `analysis_snapshots(id, from, to, payload, created_at)`
  - `suggestions(id, intent, summary, speech, created_at)`
  - `settings(id, key, value)`
- 连接与迁移：
  - `db/connection.py` 提供 `get_conn()` 上下文管理
  - `db/schema.sql` 初始化建表脚本
  - 后续可添加简单迁移版本表 `schema_meta`

四、服务与职责
- `services/ingest_service.py`：文件解析、清洗、去重、入库
- `services/analysis_service.py`：区间聚合（情绪、频率、词云）+ 缓存
- `services/suggestion_service.py`：上下文构建、LLM 调用、结果规整
- `services/settings_service.py`：配置读写与敏感信息加密
- 注意：服务不直接与前端通信，不包含 PyWebView 依赖

五、LLM 适配（M3）
- `llm/provider_base.py` 定义 `chat(messages, **opts)` 接口
- `llm/*_provider.py` 具体实现（OpenAI/Azure/本地）
- 成本控制：消息裁剪、摘要压缩、重试、缓存

六、开发流程
- 环境准备：
  - `pip install -r backend/requirements.txt`
  - 本地运行：`python app.py`
- 代码规范：
  - 类型注解、黑盒可测试；函数纯度优先
  - 业务逻辑在 services，Bridge 仅做参数校验与调度
- 测试：
  - `tests/`（后续新增）对 services 进行单元测试；桥方法做轻量集成测试

七、里程碑与任务拆分
- M1 骨架（已完成）：窗口启动、Bridge 方法占位
- M2 数据层：建表、连接与 repo、`ingest_service` 最小实现
- M3 分析：`analysis_service` 返回真实统计，前端可视化对接
- M4 建议：`suggestion_service` 接 LLM 适配层
- M5 设置与安全：API Key 加密、本地优先策略、数据导出/清理

八、风险与对策
- 数据源格式多样：建立解析适配器与规范
- 长任务阻塞：异步线程 + 进度回调（evaluate_js 或状态）
- 隐私安全：默认本地处理，最小权限与加密存储

九、验收标准
- Bridge 方法稳定、参数校验清晰、错误可追踪
- 数据一致性与幂等：重复导入不产生重复记录
- 性能：5w+ 消息聚合在秒级返回（缓存后更快）
