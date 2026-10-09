import time

class ExpiringCache:
    """
    In-memory cache with automatic TTL expiration to prevent RAM leaks
    from abandoned YouTube quality selection menus.
    """
    def __init__(self, ttl_seconds: int = 1800):
        self.ttl = ttl_seconds
        self.data = {}
        self.timestamps = {}

    def set(self, key: str, value: any):
        self.cleanup()
        self.data[key] = value
        self.timestamps[key] = time.time()

    def get(self, key: str):
        self.cleanup()
        if key in self.data:
            return self.data[key]
        return None

    def delete(self, key: str):
        self.data.pop(key, None)
        self.timestamps.pop(key, None)

    def cleanup(self):
        now = time.time()
        expired = [k for k, t in self.timestamps.items() if now - t > self.ttl]
        for k in expired:
            self.data.pop(k, None)
            self.timestamps.pop(k, None)

    def __contains__(self, key):
        return self.get(key) is not None

yt_cache = ExpiringCache(ttl_seconds=1800)

