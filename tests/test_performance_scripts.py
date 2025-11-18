from scripts.performance_eval.memory_eval import memory_eval
from scripts.performance_eval.time_eval import time_eval


def test_memory_eval_completion():
    """Test if memory eval runs without errors."""
    assert memory_eval(verbose=False)


def test_time_eval_completion():
    """Test if time eval runs without errors."""
    assert time_eval(verbose=False)
