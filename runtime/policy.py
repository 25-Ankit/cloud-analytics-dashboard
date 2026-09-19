from dataclasses import dataclass, field
from pathlib import Path
import json
import time
from collections import deque
from typing import Any


@dataclass(frozen=True)
class Policy:
    allowed_event_types: frozenset[str] = frozenset({"sale"})
    max_amount: float = 1_000_000.0
    required_fields: tuple[str, ...] = ("event_type","city","category","amount")
    rate_limit_per_minute: int = 600

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Policy":
        return cls(
            allowed_event_types=frozenset(data.get("allowed_event_types", ["sale"])),
            max_amount=float(data.get("max_amount",1_000_000)),
            required_fields=tuple(data.get("required_fields",["event_type","city","category","amount"])),
            rate_limit_per_minute=int(data.get("rate_limit_per_minute",600)),
        )


def load_policy(path: str | Path) -> Policy:
    return Policy.from_dict(json.loads(Path(path).read_text()))


@dataclass
class PolicyEngine:
    policy: Policy
    _timestamps: deque[float] = field(default_factory=deque, init=False)

    def evaluate(self, event: dict[str, Any]) -> tuple[bool,str]:
        missing=[x for x in self.policy.required_fields if x not in event]
        if missing: return False, "missing fields: " + ",".join(missing)
        if str(event["event_type"]) not in self.policy.allowed_event_types:
            return False, "event_type not allowed"
        try: amount=float(event["amount"])
        except (TypeError,ValueError): return False, "amount must be numeric"
        if amount < 0 or amount > self.policy.max_amount:
            return False, "amount outside policy limit"
        now=time.monotonic()
        while self._timestamps and now-self._timestamps[0] >= 60:
            self._timestamps.popleft()
        if len(self._timestamps) >= self.policy.rate_limit_per_minute:
            return False, "rate limit exceeded"
        self._timestamps.append(now)
        return True, "allowed"
