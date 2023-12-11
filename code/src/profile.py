import cProfile
import pstats

from .main import main


def profiled_code():
    """Run the profiled code.

    The code in this method will be profiled by the application.
    """
    main()


def profile():
    """Entry point for profiling the application."""
    profiler = cProfile.Profile()
    profiler.enable()
    profiled_code()
    profiler.disable()
    ps = pstats.Stats(profiler)
    ps.dump_stats("profile_result.prof")


if __name__ == "__main__":
    profile()
