from ..state.state_instance import StateInstance
from ..state.state_pool import StatePool
from .actions import Action


class BaseDynamics(object):
    """The abstract base class for dynamics classes.

    This class provides the basic methods a dynamics class is expected to
    implement and some common functionality
    """

    def __init__(self) -> None:
        """Instantiate a dynamics, provides the minimal required properties."""
        self.state_pool = StatePool()

    def initial_state(self) -> StateInstance:
        """Provide the initial state of this environment.

        Raises:
            NotImplementedError: If this method has not been overridden

        Should Return:
            StateInstance: the starting state.
        """
        raise NotImplementedError(
            "This method must be overridden by concrete dynamics classes"
        )

    def next(self, current_state: int, action: Action) -> tuple[int, float]:
        """Compute the next state and reward.

        Must only compute the next reward and state based on only the provided
        current state and reward to obey the markov property.

        Args:
            current_state (int): the state that the action is
            performed in
            action (Action): the action the agent has chosen


        Raises:
            NotImplementedError: If this method has not been overridden

        Should Return:
            tuple[int, float]: the resulting state after the action has been
            performed and the reward from this action
        """
        raise NotImplementedError(
            "This method must be overridden by concrete dynamics classes"
        )
