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
        window = webview.create_window('ChatMind', url=dist_index, js_api=bridge,frameless= True)
    webview.start()


if __name__ == '__main__':
    main()
