from dataclasses import dataclass


@dataclass
class BenchmarkResult:
    benchmark_format: str
    benchmark_name: str
    configuration: str
    hdl_type: str

    state_count: int
    transition_count: int
    input_count: int
    output_count: int

    parsing_execution_time: float
    parsing_peak_memory_usage: int

    generation_execution_time: float
    generation_peak_memory_usage: int
    generation_utilization: int
