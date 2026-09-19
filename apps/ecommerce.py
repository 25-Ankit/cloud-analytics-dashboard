from sdk import AnalyticsEvent

def to_event(city: str, category: str, amount: float) -> AnalyticsEvent:
    return AnalyticsEvent("ecommerce_sale", city, category, amount, {"source":"ecommerce"})
