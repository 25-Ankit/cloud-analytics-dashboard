from sdk import AnalyticsEvent

class NormalizeCategory:
    name="normalize-category"
    version="1.0.0"
    def on_start(self, context): pass
    def transform(self, event: AnalyticsEvent) -> AnalyticsEvent:
        event.category=event.category.strip().title()
        return event
    def on_stop(self, context): pass
