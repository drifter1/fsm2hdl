.PHONY: build install test lint format docs clean hdl syntax sim synth synthresults perf perfresults benchclean

SRC_DIR := src/fsm2hdl

build:
	@hatch build

install:
	@hatch env create

test:
	@hatch test --all --cover

lint:
	@hatch check code --fix

format:
	@hatch check fmt --fix

docs:
	@pdoc -o docs $(SRC_DIR) --docformat numpy 

clean:
	@rm -rf dist
	@rm -rf .pytest_cache .ruff_cache 
	@rm .coverage* | :
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@hatch env prune

hdl:
	@hatch run python benchmarking/hdl_generation/main.py

syntax:
	@python3 benchmarking/syntax_tests/main.py

sim:
	@hatch run python benchmarking/sim_tests/prepare_tests.py
	@python3 benchmarking/sim_tests/main.py

synth:
	@python3 benchmarking/synth_tests/main.py

synthresults:
	@hatch run python benchmarking/synth_tests/process_reports.py
	@python3 benchmarking/synth_tests/report_visualization.py

perf:
	@hatch run python benchmarking/perf_tests/main.py

perfresults:
	@python3 benchmarking/perf_tests/result_visualization.py
	@python3 benchmarking/perf_tests/result_latex_table.py

benchclean:
	@rm -rf benchmarking/perf_tests/rtl
	@rm -rf benchmarking/sim_tests/sim_build
	@rm -rf benchmarking/sim_tests/tests
	@rm -rf projects
	@rm -rf .Xil
	@rm clockInfo.txt | :