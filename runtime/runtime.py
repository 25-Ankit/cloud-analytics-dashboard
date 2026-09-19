import os
from pathlib import Path
from typing import Any

from stream.stream import init_db, put_event
from .policy import PolicyEngine, load_policy


class EventRuntime:
    def __init__(self, policy_engine: PolicyEngine | None = None):
        init_db()
        if policy_engine is None:
            policy_path=os.getenv("POLICY_PATH", "runtime/policies/default.json")
            policy_engine=PolicyEngine(load_policy(policy_path))
        self.policy_engine=policy_engine

    def submit(self, event: dict[str, Any]) -> dict[str, Any]:
        allowed, reason=self.policy_engine.evaluate(event)
        if not allowed:
            return {"accepted":False,"reason":reason}
        event_id=put_event(event["city"],event["category"],event["amount"],event["event_type"],event.get("created_at"))
        return {"accepted":True,"event_id":event_id}
