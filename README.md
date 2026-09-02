# fsm2hdl

This is an extensible Python-based framework for the automated generation of synthesis-ready HDL code from high-level finite-state machine (FSM) specifications. It supports configurable generation of Verilog-2005 and VHDL-2008 implementations.

## Features

- Finite-state machines (FSMs) are accepted as state-transition tables in KISS2 or JSON format.
- Generate clean, synthesis-ready Verilog-2005 and VHDL-2008 code.
- Output configuration is adjustable using user-defined parameters, enabling multiple distinct HDL implementations from the same FSM specification.
- Both a command-line interface (CLI) and programmatic usage are available.
- The framework uses an explicit internal FSM data model implemented with Python data classes.
- Its modular and extensible design allows additional parameters and functionality to be added without altering the core engine.

## Validation

- The framework was validated on standard FSM benchmarks.
- Generated HDL was checked through syntax analysis.
- Behavioral correctness was confirmed through simulation with full state and transition coverage.
- Generated designs were evaluated through FPGA synthesis and implementation toolflows.
- Runtime and memory usage were measured to confirm practical overhead.

## Requirements

- [python](https://www.python.org/) >= 3.10
- [jinja2](https://jinja.palletsprojects.com/)

### Building from source

- [hatch](https://hatch.pypa.io/)
- [uv](https://docs.astral.sh/uv)

### Source code testing

- [pytest](https://pytest.org/)

### Documentation generation

- [pdoc](https://pdoc.dev/)

### Validation of Generated HDL

#### Open-source Tooling

- [Icarus Verilog](https://github.com/steveicarus/iverilog)
- [GHDL](https://github.com/ghdl/ghdl)
- [Cocotb](https://github.com/cocotb/cocotb)
- [GTKwave](https://github.com/gtkwave/gtkwave)
- [Yosys](https://github.com/YosysHQ/yosys)
- [GHDL Yosys Plugin](https://github.com/ghdl/ghdl-yosys-plugin)

> [!NOTE]
> To avoid having to manually compile any tools that are not available in your distribution or on your platform, it is strongly recommended that you use the [OSS CAD Suite](https://github.com/YosysHQ/oss-cad-suite-build).

#### Proprietary Tooling

- [AMD Vivado™ Design Suite](https://www.amd.com/en/products/software/adaptive-socs-and-fpgas/vivado.html)

### Benchmark Result Visualization

- [Matplotlib](https://matplotlib.org/)
- [NumPy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)

## Getting Started

### Building from source

Clone the repository and change into the directory:

```
git clone https://github.com/drifter1/fsm2hdl.git
cd fsm2hdl
```

To build using `hatch` type:

```
make build
```

To install in a `hatch` environment locally:

```
make install
```

### Running included tests

To run the included `pytest` tests type `make test`.

### Linting and formatting

To lint and format the source code using `hatch` type `make lint` and `make format`, respectively.

### Documentation generation

To generate the documentation using `pdoc` type `make docs`.

### Cleanup of build files

Perform cleanup with `make clean`.

## Benchmarks

The included benchmarks stem from the well-regarded MCNC91 benchmark collection.

All rights reserved by the owners.

### Reference

S. Yang 1991. Logic Synthesis and Optimization Benchmarks User Guide: Version 3.0, Microelectronics Center of North Carolina (MCNC) Research Triangle Park, NC, USA.

## Benchmarking

The tool can be evaluated using the included benchmarks with the following Make targets:

| Evaluation step | Description | Command |
|---|---|---|
| HDL generation | Generate HDL code for the included FSM benchmarks. | `make hdl` |
| Syntax checking | Check the generated HDL for syntax errors. | `make syntax` |
| Functional simulation | Simulate the generated HDL to verify functional behavior. | `make sim` |
| FPGA synthesis and implementation | Run FPGA synthesis and implementation flows. | `make synth` |
| Performance and resource footprint | Measure runtime, peak memory usage, and file utilization. | `make perf` |

## License

**fsm2hdl** is released under the [MIT license](LICENSE). You are permitted to use, modify, and distribute **fsm2hdl**, under the condition that all copies of the software include a copy of the copyright notice and license terms.


## Publication

TBD
