import contextlib
import json
import os
from collections import deque
from dataclasses import asdict
from pathlib import Path

from fsm2hdl import Fsm, State, Transition, parse_fsm_kiss2

FILE_PATH = Path(__file__).resolve().parent
PROJ_PATH = FILE_PATH.parent.parent
BENCHMARK_PATH = PROJ_PATH / "benchmarks"
TESTS_PATH = FILE_PATH / "tests"


def fsm_to_adj(fsm: Fsm):
    adj = {}
    for s in fsm.states.values():
        for t in s.transitions:
            if t.state_source not in adj:
                adj[t.state_source] = set()

            if t.state_target not in adj:
                adj[t.state_target] = set()

    for s in fsm.states.values():
        for t in s.transitions:
            adj[s.name].add(t.state_target)

    return adj


def get_transition_from_id(fsm, t_id):
    for s in fsm.states.values():
        for t in s.transitions:
            if t.transition_id == t_id:
                return t
    return None


def shortest_path_bfs(adj, start, end):
    if start == end:
        return [start]

    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        current, path = queue.popleft()
        for neighbor in adj.get(current, []):
            if neighbor not in visited:
                if neighbor == end:
                    return [*path, neighbor]
                visited.add(neighbor)
                queue.append((neighbor, [*path, neighbor]))
    return None


prev_coverage: float = 0.0
coverage: float = 0.0

with contextlib.suppress(FileExistsError):
    os.mkdir(TESTS_PATH)

for path, _dirs, files in os.walk(BENCHMARK_PATH):
    for file_name in sorted(files):
        file_name_stem: str = str(Path(file_name).stem)
        extension: str = str(Path(file_name).suffix)
        path_stem: str = str(Path(path).stem)
        current_output_path = Path(TESTS_PATH) / path_stem / file_name_stem
        current_json_file_stem = file_name_stem
        if file_name_stem[-1].isdigit():
            current_json_file_stem += "_"

        current_output_path.mkdir(parents=True, exist_ok=True)

        fsm: Fsm = parse_fsm_kiss2(path, file_name_stem)

        adj = fsm_to_adj(fsm)

        covered_ids = set()

        transition_count = sum(
            len(state.transitions) for state in fsm.states.values()
        )

        state_count = len(fsm.states)

        expected_ids = set(range(1, transition_count + 1))

        missing = expected_ids

        prev_coverage = 0
        coverage = 0

        i: int = 0
        while True:
            cur_state: State = fsm.states[fsm.start_state]
            cur_test_vectors = []
            prev_coverage = coverage
            for _ in range(state_count * 2):
                target_tid = next(iter(missing))
                target_transition: Transition = get_transition_from_id(
                    fsm, target_tid
                )

                if target_transition.state_source == cur_state.name:
                    cur_transition = target_transition
                else:
                    path_bfs = shortest_path_bfs(
                        adj, cur_state.name, target_transition.state_source
                    )

                    if path_bfs is None:
                        break

                    cur_transition: Transition = None

                    next_target = path_bfs[1]

                    for t in cur_state.transitions:
                        if t.state_target == next_target:
                            cur_transition = t
                            break

                    if cur_transition is None:
                        break

                transition_info = asdict(cur_transition)
                transition_info["inputs"] = {}
                transition_info["outputs"] = {}

                for fsm_input in fsm.inputs:
                    transition_info["inputs"][fsm_input] = 0

                for transition_input in cur_transition.inputs:
                    if transition_input.name == "1":
                        break
                    if not transition_input.inverted:
                        transition_info["inputs"][transition_input.name] = 1

                if len(cur_transition.outputs) > 0:
                    for fsm_output in fsm.outputs:
                        if fsm_output in cur_transition.outputs:
                            transition_info["outputs"][fsm_output] = 1
                        else:
                            transition_info["outputs"][fsm_output] = 0

                cur_test_vectors.append(transition_info)

                cur_state: State = fsm.states[cur_transition.state_target]

                del cur_transition

                present_ids = {t["transition_id"] for t in cur_test_vectors}
                covered_ids |= present_ids
                missing = sorted(expected_ids - covered_ids)

                if not missing:
                    break

            current_json_file = current_json_file_stem + str(i) + ".json"

            with open(current_output_path / current_json_file, "w") as f:
                json.dump(cur_test_vectors, f, indent=2)

            coverage = 100 * len(covered_ids) / transition_count

            if coverage > prev_coverage:
                i += 1
                print(f"Coverage for {file_name_stem} is {coverage:.2f}%.")  # noqa: T201

            if not missing:
                break
