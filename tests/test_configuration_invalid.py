"""
pytest test for the Configuration __post_init__() method.
"""

import pytest

from fsm2hdl.common import Configuration
from fsm2hdl.common.parameters import FSMType


def test_configuration_invalid():
    """
    Perform tests for `` __post_init__()`` method:
    - check whether exception is raised when configuration is not valid.
    """

    with pytest.raises(TypeError, match="invalid type"):
        Configuration(hdl_type=FSMType.MOORE)
