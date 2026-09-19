from sdk import AnalyticsEvent

def to_event(city: str, activity: str, calories: float) -> AnalyticsEvent:
    return AnalyticsEvent("fitness_activity", city, activity, calories, {"source":"fitness"})
