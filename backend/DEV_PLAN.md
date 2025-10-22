# ChatMind 后端开发计划手册（更新版：长期数据 + 短期实时建议工作流）

适用对象：后端/Python 工程师
目标：本地桌面应用后端，支持微信聊天记录的长期导入分析与短期实时监听，结合 PyWebView JS Bridge 向前端提供数据与建议。

一、总体架构
- 运行形态：纯本地桌面应用，无对外端口，通过 PyWebView JS API 与前端通信。
- 技术栈：Python 3.10+、PyWebView、SQLite3、并发（threading/asyncio）。
- 关键工作流：
  1) 长期数据：解包微信数据库 → 清洗入库 → 聚合分析 → 图表与分段总结
  2) 短期数据：自动脚本实时监听 → 生成上下文 → LLM 实时建议 → 前端建议面板

二、目录结构与职责
- `backend/app/main.py`：启动入口，创建窗口并注册 Bridge。
- `backend/app/webview/bridge.py`：前端调用入口（JS Bridge）。
- `backend/app/services/`
  - `ingest_service.py`：长期导入（微信 DB/导出文件解析）、清洗、入库。
  - `realtime_service.py`：短期实时监听（脚本启动/停止、事件派发）。
  - `analysis_service.py`：长期数据聚合与分段总结（情绪、频率、词云）。
  - `suggestion_service.py`：实时建议生成（结合长期画像 + 短期上下文）。
  - `settings_service.py`：配置读写、隐私与密钥管理。
- `backend/app/db/`
  - `schema.sql` 建表；`connection.py` 连接与事务；`repo.py` 仓储。
- `backend/app/llm/`
  - `provider_base.py`、`*_provider.py`、`context_builder.py`（长期画像 + 短期上下文）。

三、通信约定（JS Bridge 方法）
- 命名与返回：方法名小写下划线；参数/返回 JSON 化；错误统一包装 `{"ok": false, "error": msg}`。
- 首批方法（骨架）：
  - `ping() -> str`
  - 长期：
    - `ingest_data(file_path: str, options: dict) -> {count:int, warnings:list}`
    - `get_analysis(date_range) -> {emotion, frequency, wordcloud, segments}`
  - 短期：
    - `realtime_start(options: dict) -> {running: bool}`（启动监听脚本）
    - `realtime_stop() -> {running: bool}`（停止监听）
    - `realtime_status() -> {running: bool, stats: dict}`
  - 建议：
    - `generate_suggestion(intent: str, context: dict) -> {summary, speech[]}`（手动触发）
    - 实时建议通过 `realtime_service` 内部驱动 + `evaluate_js`/state 推送（或前端轮询 `realtime_status`）。
  - 设置：`get_settings() / set_settings(payload)`

四、数据库设计（长期 + 短期）
- 表：
  - `conversations(id, name, platform, created_at)`
  - `messages(id, conversation_id, role, ts, content, emotion, source)`（source: long/realtime）
  - `analysis_segments(id, conversation_id, from, to, summary, metrics_json)`（分段总结）
  - `suggestions(id, conversation_id, intent, created_at, summary, speech_json, source)`（source: manual/realtime）
  - `settings(id, key, value)`
  - `runtime_events(id, type, created_at, payload_json)`（可选：监听/错误/心跳）

五、长期数据（微信 DB 解包）
- 输入：本地微信数据库/导出文本；需适配不同版本与路径。
- 处理：解析（账号→会话→消息）、清洗（去重、空白、媒体占位）、匿名化（可选）。
- 入库：批量写入 `messages`，构建索引（conversation_id, ts）。
- 分析：
  - 情绪/频率/词云聚合；
  - 分段总结：按时间窗口（周/月/自定义）生成 `analysis_segments`。

六、短期数据（实时监听）
- 监听脚本：
  - Windows 优先，定时扫描/Hook（依据可行性），或监控某导出文件刷新；
  - 将新消息转换为标准结构写入 `messages`（source=realtime）。
- 实时建议：
  - 上下文构建：最近 N 条 + 目标意图（亲密/维持/疏远）+ 历史画像摘要；
  - 生成：调用 `llm/provider_*`，返回简洁话术与策略；
  - 推送：通过 `evaluate_js` 将建议推送到前端面板，或前端定时 `realtime_status` 拉取。

七、服务实现要点
- `ingest_service`：可插拔解析器（DB 文件、txt/csv）；统一输出 Message DTO。
- `realtime_service`：线程安全，提供 start/stop/status；内部生产事件队列；与 `suggestion_service` 协作。
- `analysis_service`：聚合函数与缓存；输出可直接绘图的数据结构。
- `suggestion_service`：提示词模板、裁剪与脱敏；重试与限流；可缓存最近结果。

八、LLM 适配（实时优先）
- 接口：`chat(messages, intent, persona)`；支持超时/重试；
- 成本与隐私：本地优先、脱敏、摘要压缩；
- 可替换：OpenAI/Azure/本地模型，统一 Provider。

九、开发流程与测试
- 运行：`pip install -r backend/requirements.txt` → `python app.py`
- 单元测试：services 为主；桥接方法轻集成；
- 模拟数据：提供 `fixtures` 便于前端调试。

十、里程碑
- M1 骨架（已完成）：Bridge + 路由页面
- M2 长期导入：解析器/入库/基础分析与分段总结
- M3 短期监听：脚本运行与状态、实时建议推送
- M4 LLM 适配：提示词模板与多提供商
- M5 体验与安全：配置管理、隐私策略与导出

十一、验收标准
- 长期数据导入成功、分析与分段总结可用；
- 短期监听可启动停止，能捕捉新消息并生成至少 1 条实时建议；
- 发生错误有日志与状态反馈（realtime_status）。
