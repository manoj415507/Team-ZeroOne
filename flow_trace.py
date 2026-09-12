"""
AI Flow Trace — end-to-end step tracking, anomaly flagging, and audit support.
"""
import time


class FlowTrace:
    def __init__(self):
        self.steps = []

    def track(self, stage, status, details=None, anomaly=False):
        self.steps.append({
            "stage": stage,
            "status": status,
            "details": details or {},
            "anomaly": anomaly,
            "timestamp": time.time(),
        })

    def anomalies(self):
        return [s for s in self.steps if s["anomaly"]]

    def to_list(self):
        return self.steps
