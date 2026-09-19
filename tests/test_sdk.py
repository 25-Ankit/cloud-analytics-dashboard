from sdk import AnalyticsEvent,ExtensionRuntime
from sdk.examples.simple_extension import NormalizeCategory

def test_extension_lifecycle():
    rt=ExtensionRuntime([NormalizeCategory()]); rt.start()
    e=rt.process(AnalyticsEvent("sale","Mumbai"," electronics ",10))
    rt.stop(); assert e.category=="Electronics"
