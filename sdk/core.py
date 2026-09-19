from dataclasses import dataclass, field
from typing import Any, Protocol

SDK_VERSION="1.0.0"

@dataclass
class AnalyticsEvent:
    event_type: str
    city: str
    category: str
    amount: float
    metadata: dict[str,Any]=field(default_factory=dict)

class Extension(Protocol):
    name: str
    version: str
    def on_start(self, context: dict[str,Any]) -> None: ...
    def transform(self, event: AnalyticsEvent) -> AnalyticsEvent: ...
    def on_stop(self, context: dict[str,Any]) -> None: ...
