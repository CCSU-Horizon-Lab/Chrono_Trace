from typing import Any, Dict

class Bridge:
    """PyWebView JS API Bridge: 暴露给前端调用的方法。"""

    def ping(self) -> str:
        return "pong"

    def ingest_data(self, file_path: str, options: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return {"ok": True, "file_path": file_path, "options": options or {}}

    def get_analysis(self, date_range: Dict[str, str]) -> Dict[str, Any]:
        return {
            "emotion": {"labels": ["2025-01-01", "2025-01-02"], "values": [0.2, 0.6]},
            "frequency": {"labels": ["Mon", "Tue"], "values": [12, 8]},
            "wordcloud": [{"text": "聊天", "weight": 10}, {"text": "建议", "weight": 6}],
        }

    def generate_suggestion(self, intent: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "intent": intent,
            "summary": "示例建议：保持耐心与共情表达。",
            "speech": ["我理解你的感受，我们一起看怎么改善。"],
        }

    def get_settings(self) -> Dict[str, Any]:
        return {
            "model": "local",
            "interval_minutes": 30,
            "range_days": 7,
        }

    def set_settings(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"saved": True, "payload": payload}
