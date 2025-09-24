import status_queue

sq = status_queue.Rpc()
print([s for s in sq.__dir__() if not s.startswith("__")])