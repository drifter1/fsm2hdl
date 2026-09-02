import tracemalloc


class MemoryTracker:
    def start(self):
        tracemalloc.start()

    def stop(self):
        tracemalloc.stop()

    def reset(self):
        tracemalloc.reset_peak()

    def get(self) -> int:
        _current, peak = tracemalloc.get_traced_memory()

        return peak
