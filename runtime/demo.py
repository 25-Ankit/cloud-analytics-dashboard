from runtime.runtime import EventRuntime

rt=EventRuntime()
print(rt.submit({"event_type":"sale","city":"Mumbai","category":"Electronics","amount":999}))
print(rt.submit({"event_type":"not_allowed","city":"Mumbai","category":"Test","amount":10}))
