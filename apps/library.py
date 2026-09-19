from sdk import AnalyticsEvent

def to_event(city: str, genre: str, value: float=0.0) -> AnalyticsEvent:
    return AnalyticsEvent("library_checkout", city, genre, value, {"source":"library"})
