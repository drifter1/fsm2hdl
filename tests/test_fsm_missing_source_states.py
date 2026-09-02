"""
pytest test for the FSM __post_init__() method.
"""

from fsm2hdl.common import Fsm, Input, State, Transition


def test_fsm_missing_source_states():
    """
    Perform tests for `` __post_init__()`` method:
    - check whether missing source states are added
    """

    states: dict[str, State] = {}

    # define state a1
    states["a1"] = State("a1")

    # a1 -> a2 when input x1, outputs y1
    states["a1"].transitions.append(
        Transition(1, "a1", "a2", [Input("x1", inverted=False)], ["y1"])
    )

    # a1 -> a3 with inverted input x1, no outputs
    states["a1"].transitions.append(
        Transition(2, "a1", "a3", [Input("x1", inverted=True)], [])
    )

    # create FSM
    fsm: Fsm = Fsm("test", states)

    # assert whether missing definitions for a2 and a3
    # where added to the states dictionary
    assert "a2" in fsm.states
    assert "a3" in fsm.states
