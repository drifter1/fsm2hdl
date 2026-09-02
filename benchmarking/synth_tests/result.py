from dataclasses import dataclass, field


@dataclass
class StageResults:
    lut: int = 0
    ff: int = 0
    fmax: float = 0.0
    power: float = 0.0
    time: int = 0
    memory: float = 0


@dataclass
class ToolResults:
    synth_results: StageResults = field(default_factory=StageResults)
    impl_results: StageResults = field(default_factory=StageResults)


@dataclass
class BenchmarkResults:
    benchmark_format: str
    benchmark_name: str
    hdl_file: str
    parameters: list[str]
    vivado_results: ToolResults = field(default_factory=ToolResults)
    yosys_results: ToolResults = field(default_factory=ToolResults)
