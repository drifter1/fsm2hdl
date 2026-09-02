from dataclasses import dataclass
from time import perf_counter


@dataclass
class Timer:
    start_time: float = 0.0
    end_time: float = 0.0

    def start(self) -> None:
        self.start_time = perf_counter()

    def end(self) -> None:
        self.end_time = perf_counter()

    def calc_diff(self) -> float:
        return self.end_time - self.start_time
