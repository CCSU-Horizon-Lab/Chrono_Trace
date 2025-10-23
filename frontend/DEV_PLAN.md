# Chrono_Trace 前端开发计划手册（更新版：长期数据 + 短期实时建议工作流）

适用对象：前端/Vue 工程师
目标：构建 Vue3 前端，支持长期数据的图表与分段总结展示，以及短期实时建议面板，通过 PyWebView Bridge 与后端通信。

一、页面与路由（保持四页）
- `/` 首页：引导用户导入长期数据、启动/停止短期监听，显示运行状态。
- `/analytics` 历史数据：日期选择，展示情绪曲线、聊天频率、词云与分段总结卡片。
- `/suggestions` AI建议：实时建议面板（按意图切换：亲密/维持/疏远），展示最新建议流与手动触发入口。
- `/settings` 设置：模型与 API Key、隐私选项、数据源路径、监听策略。

二、桥接通信与状态
- 封装在 `src/api/bridge.ts`：
  - 长期：`ingest_data(filePath, options)`；`get_analysis(dateRange)`
  - 短期：`realtime_start(options)` / `realtime_stop()` / `realtime_status()`
  - 建议：`generate_suggestion(intent, context)`（手动触发）
  - 设置：`get_settings()` / `set_settings(payload)`
- 就绪：所有调用前 `await bridgeReady()`；错误轻提示。
- 实时建议流：
  - 方案A：后端 `evaluate_js` 推送到前端（需事件处理函数）。
  - 方案B：前端定时轮询 `realtime_status()` 并更新面板（MVP 优先）。

三、页面骨架与交互
- 首页：
  - 文件选择组件（导入长期数据） → 调用 `ingest_data` → 显示导入统计
  - 监听控制：按钮启动/停止 → 显示 `realtime_status.running`
- 历史数据：
  - 日期区间选择器；图表占位（ECharts/Chart.js 后续接入）
  - 分段总结：卡片式列表（时间段 + 摘要/指标）
- AI建议：
  - 意图选择器（亲密/维持/疏远）；
  - 实时建议流（列表/气泡），支持手动触发 `generate_suggestion`
- 设置：
  - 配置表单：模型、API Key、数据源路径、监听策略；保存/读取调用桥接。

四、工程与样式
- 侧边栏布局已完成；系统字体、浅色主题。
- 后续引入组件库与图表库（建议：Element Plus + ECharts）。
- 状态管理：M3 引入 Pinia（缓存最近分析结果与建议流）。

五、开发与构建
- 开发：`npm i && npm run dev`（调试前端逻辑）
- 联调：`npm run build` → `python app.py`（PyWebView 加载 dist）

六、里程碑
- M1 骨架（已完成）：侧边栏布局与四页占位
- M2 长期数据 UX：导入流程与分析展示框架（图表占位与分段卡片）
- M3 短期监听与建议：监听控制与状态、建议面板轮询刷新
- M4 组件与体验：UI 组件库、加载态/错误态、主题与细节

七、验收标准
- 首页可导入数据并显示统计；可启动/停止监听并显示运行状态；
- 历史数据页可展示基础分析结果及分段总结占位；
- AI建议页能看到实时建议列表流（哪怕是模拟数据先行）；
- 设置页可读写配置并生效。
