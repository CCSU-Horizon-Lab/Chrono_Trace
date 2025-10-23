import os

# 项目根目录（本文件位于 backend/app/config.py，向上两层即为项目根）
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# 前端目录
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')

# 默认开发期本地地址（可被环境变量 DEV_URL 覆盖）
DEV_URL_DEFAULT = 'http://localhost:5173'

# 窗口标题（统一管理）
PROD_WINDOW_TITLE = 'Chrono_Trace'
DEV_WINDOW_TITLE = 'Chrono_Trace (DEV)'


def get_dist_index_path() -> str:
    """
    返回打包后的入口 index.html 路径，没有则返回空字符串。
    """
    dist_index = os.path.join(FRONTEND_DIR, 'dist', 'index.html')
    return dist_index if os.path.exists(dist_index) else ''
