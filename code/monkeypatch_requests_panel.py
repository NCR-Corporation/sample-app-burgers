from requests_panel.panel import RequestsDebugPanel

class SafeRequestsDebugPanel(RequestsDebugPanel):
    def generate_stats(self, request, response):
        super().generate_stats(request, response)

        stats = self.get_stats()
        cleaned_requests = []

        for stat in stats.get("requests", []):
            if isinstance(stat, dict):
                stat.pop("stacktrace", None)  # safe removal from dict
                cleaned_requests.append(stat)
            elif hasattr(stat, "__dict__"):
                if hasattr(stat, "stacktrace"):
                    setattr(stat, "stacktrace", None)
                cleaned_requests.append(stat)

        self.record_stats({"requests": cleaned_requests})
