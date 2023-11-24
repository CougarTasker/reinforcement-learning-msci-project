import cProfile
import pstats

from .controller.learning_instance_controller import InstanceController
from .controller.options import AgentOptions, DynamicsOptions


def profiled_code():
    """Run the profiled code.

    The code in this method will be profiled by the application.
    """
    cont = InstanceController(
        AgentOptions.value_iteration, DynamicsOptions.collection
    )
    cont.get_agent()


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
