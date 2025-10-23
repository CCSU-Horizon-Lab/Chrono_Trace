import os
import webview
from backend.app.webview.bridge import Bridge
from backend.app.config import get_dist_index_path, PROD_WINDOW_TITLE



def main():
    bridge = Bridge()
    dist_index = get_dist_index_path()
    if not dist_index:
        raise RuntimeError('未找到 frontend/dist/index.html，请先执行 npm run build')
    webview.create_window(PROD_WINDOW_TITLE, url=dist_index, js_api=bridge, frameless=False)
    webview.start()


if __name__ == '__main__':
    main()
