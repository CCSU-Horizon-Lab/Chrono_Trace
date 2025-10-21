import os
import webview
from backend.app.webview.bridge import Bridge


def get_dist_index_path() -> str:
    root = os.path.abspath(os.path.dirname(__file__))
    dist_index = os.path.join(root, 'frontend', 'dist', 'index.html')
    return dist_index if os.path.exists(dist_index) else ''


def main():
    dist_index = get_dist_index_path()
    bridge = Bridge()

    if dist_index:
        window = webview.create_window('ChatMind', url=dist_index, js_api=bridge)
    else:
        html = """
        <!doctype html>
        <html>
          <head><meta charset='utf-8'><title>ChatMind</title></head>
          <body>
            <div style='font-family: system-ui; padding: 24px;'>
              <h1>ChatMind</h1>
              <p>前端构建产物未找到，请先在 frontend 目录执行构建。</p>
              <p>命令：npm i && npm run build</p>
            </div>
          </body>
        </html>
        """
        window = webview.create_window('ChatMind', html=html, js_api=bridge)

    webview.start()


if __name__ == '__main__':
    main()
