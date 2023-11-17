import cProfile
import pstats

import pytest


def profiled_code():
    """Run the profiled code.

    The code in this method will be profiled by the application.
    """
    pytest.main(
        [
            "tests/dynamics/test_dynamics_distribution.py",
            "-k",
            "test_duration",
        ]
    )


def main():
    """Entry point for profiling the application."""
    profiler = cProfile.Profile()
    profiler.enable()
    profiled_code()
    profiler.disable()
    ps = pstats.Stats(profiler)
    ps.dump_stats("profile_result.prof")


if __name__ == "__main__":
    main()
