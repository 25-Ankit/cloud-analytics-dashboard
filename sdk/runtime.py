from typing import Any
from .core import AnalyticsEvent, Extension, SDK_VERSION

class ExtensionRuntime:
    def __init__(self, extensions: list[Extension] | None=None):
        self.extensions=extensions or []
    def start(self, context: dict[str,Any] | None=None):
        ctx={"sdk_version":SDK_VERSION, **(context or {})}
        for ext in self.extensions: ext.on_start(ctx)
    def process(self, event: AnalyticsEvent) -> AnalyticsEvent:
        current=event
        for ext in self.extensions: current=ext.transform(current)
        return current
    def stop(self, context: dict[str,Any] | None=None):
        ctx={"sdk_version":SDK_VERSION, **(context or {})}
        for ext in reversed(self.extensions): ext.on_stop(ctx)
