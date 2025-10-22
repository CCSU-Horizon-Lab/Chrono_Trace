# ChatMind 前端开发计划手册

适用对象：前端/Vue 工程师
目标：基于 Vite + Vue3 的本地桌面应用前端骨架，通过 PyWebView JS Bridge 与 Python 通信。

一、总体架构
- 运行形态：Vue 构建为静态文件（frontend/dist），由 PyWebView 加载。
- 技术栈：Vue3、Vue Router、TypeScript、Vite。
- 路由结构：
  - `/` 首页
  - `/analytics` 历史数据
  - `/suggestions` AI建议
  - `/settings` 设置

二、目录结构
- `src/`
  - `api/bridge.ts`：封装 `window.pywebview.api.*`，提供 `bridgeReady()`
  - `router/index.ts`：路由管理（Hash 模式，适配本地文件）
  - `views/`：四个页面骨架
  - `App.vue`：侧边栏布局与路由占位
  - `main.ts`：应用入口

三、页面要求（M1 骨架）
- 统一布局：左侧 240px 侧栏，右侧内容区自适应
- 四个页面仅展示标题与简单占位/按钮，调用桥接演示：
  - 首页：显示欢迎信息与 ping 按钮（调用 `api.ping`）
  - 历史数据：按钮触发 `api.get_analysis` 并以 `<pre>` 展示结果
  - AI建议：下拉选择意图 + 按钮调用 `api.generate_suggestion`
  - 设置：读取/保存按钮调用 `api.get_settings`/`api.set_settings`

四、通信与错误处理
- 在任何桥调用前 `await bridgeReady()`，监听 `pywebviewready`
- API 调用统一放在 `api/bridge.ts` 的代理中；页面层只感知 `api.xxx`
- 错误处理：页面捕获异常后以轻提示显示（后续接入全局消息组件）

五、样式与组件
- 基础样式：系统字体、浅色主题；active 路由高亮
- 后续可引入组件库（如 Element Plus/Naive UI）与图表库（ECharts/Chart.js）

六、开发与构建
- 开发：`npm i && npm run dev`（如需与 PyWebView 联调，使用 `npm run build` 后 `python app.py`）
- 构建：`npm run build`，产物位于 `frontend/dist`，由 PyWebView 直接加载

七、里程碑与任务拆分
- M1 骨架（已完成）：侧边栏布局、四页面路由、桥接基础
- M2 数据展示：引入图表库，历史数据渲染曲线/频率/词云占位
- M3 交互与状态：Pinia 状态管理、加载态与错误态、缓存最近结果
- M4 体验优化：主题、快捷键、窗口尺寸记忆

八、验收标准
- 在 `python app.py` 启动后能正常显示四个页面
- 每个页面的按钮能成功调用桥接并显示示例数据
- 构建后产物可被 PyWebView 正常加载（无跨域/路径问题）
