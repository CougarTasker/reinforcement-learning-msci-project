from ..state.state_instance import StateInstance
from ..state.state_pool import StatePool
from .actions import Action


class BaseDynamics(object):
    """The abstract base class for dynamics classes.

    This class provides the basic methods a dynamics class is expected to
    implement and some common functionality
    """

    def __init__(self, width: int, height: int) -> None:
        """Instantiate a dynamics, provides the minimal required properties.

        Raises:
            TypeError: If the width or height are not integers
            ValueError: if the width or height are not positive integer

        Args:
            width (int): The width of the grid world.
            height (int): The height of the gird world.
        """
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("width and height must be valid integers")
        elif width < 1 or height < 1:
            raise ValueError("width and height must be positive integers")

        self.width = width
        self.height = height
        self.state_pool = StatePool

    def is_in_bounds(self, position: tuple[int, int]) -> bool:
        """Detect either a position is within the bounds of the grid.

        Args:
            position (tuple[int, int]): the position to test

        Returns:
            bool: true where the position is within the bounds of the grid
            world.
        """
        x_pos, y_pos = position
        return 0 <= x_pos < self.width and 0 <= y_pos < self.height

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
