from src.model.agents.base_agent import BaseAgent
from src.model.config.agent_section import AgentConfig
from src.model.config.grid_world_section import GridWorldConfig
from src.model.dynamics.actions import Action
from src.model.dynamics.base_dynamics import BaseDynamics
from src.model.state.cell_entities import CellEntity
from src.model.state.state_builder import StateBuilder
from src.model.state.state_instance import StateInstance

# four states left and right, any action will move to the other state
# up action will cause an entity to be added if it was not already

# l0  r3 -> min states
# le1 re2 -> max states


class TestGridWorldConfig(GridWorldConfig):
    def width(self) -> int:
        return 2

    def height(self) -> int:
        return 1

    def agent_location(self) -> tuple[int, int]:
        return 0, 0

    def entity_count(self) -> int:
        return 0

    def energy_capacity(self) -> int:
        return 10

    def initial_energy(self) -> int:
        return self.energy_capacity()


class SimpleTestDynamics(BaseDynamics):
    def __init__(self) -> None:
        super().__init__(TestGridWorldConfig())

        l = self.initial_state()
        r = self.next(l, action=Action.right)[0]
        le = self.next(r, Action.up)[0]
        re = self.next(l, Action.up)[0]

        self.state_pool.id_to_state = {0: l, 1: le, 2: re, 3: r}
        self.state_pool.state_to_id = {l: 0, le: 1, re: 2, r: 3}

    def is_stochastic(self) -> bool:
        """Determine weather the dynamics behave stochastically.

        If stochastic then there is random variability in the output of `next`.
        However variability distribution must still be markovian.

        Raises:
            NotImplementedError: If this method has not been overridden

        Should Return:
            bool: weather this dynamics behaves stochastically.

        """
        return True

    def initial_state(self) -> StateInstance:
        """Provide the initial state of this environment.

        Raises:
            NotImplementedError: If this method has not been overridden

        Should Return:
            StateInstance: the starting state.
        """
        return StateBuilder().set_agent_location((0, 0)).build()

    def next(
        self, current_state: StateInstance, action: Action
    ) -> tuple[StateInstance, float]:
        x_pos = 1 if current_state.agent_location[0] == 0 else 0

        next_state = StateBuilder(current_state).set_agent_location((x_pos, 0))

        if action == Action.up:
            next_state.set_entity((0, 0), CellEntity.goal)

        return next_state.build(), 0


class TestAgentConfig(AgentConfig):
    def discount_rate(self) -> float:
        """Get the discount rate.

        Returns:
            float: the amount to discount future reward
        """
        return 0.9

    def stopping_epsilon(self) -> float:
        """Get the stopping epsilon.

        Returns:
            float: the maximum error allowable in a value table
        """
        return 0.1

    def learning_rate(self) -> float:
        """Get the learning rate.

        Returns:
            float: the amount to update the value table with each observation
        """
        return 0.1

    def sample_count(self) -> int:
        """Get the sample count.

        Returns:
            int: the number of samples to use for distribution analysis.
        """
        return 100


class MockAgent(BaseAgent):
    """Provides the common base for different learning agents."""

    def __init__(
        self,
        min_state: float,
        max_state: float,
        min_action: float,
        max_action: float,
    ) -> None:
        super().__init__(TestAgentConfig())
        self.state_values = {
            0: min_state,
            1: max_state,
            2: max_state,
            3: (min_state + max_state) / 2,
        }
        self.state_action_values = {
            Action.up: min_action,
            Action.down: min_action,
            Action.left: max_action,
            Action.right: (min_action + max_action) / 2,
        }

    def evaluate_policy(self, state: int) -> Action:
        return Action.down

    def record_transition(
        self,
        previous_state: int,
        previous_action: Action,
        new_state: int,
        reward: float,
    ) -> None:
        # record
        pass

    def get_state_value(self, state: int) -> float:
        """Get the agents interpretation of the value of this state.

        Args:
            state (int): the state to evaluate

        Raises:
            NotImplementedError: If this method has not been overridden by
            concrete agent.

        Returns:
            float: the agents interpretation of the value of this state
        """
        return self.state_values[state]

    def get_state_action_value(self, state: int, action: Action) -> float:
        """Get the agents interpretation of an actions value.

        allows for visualisations to be made

        Args:
            state (int): the state to perform the action in
            action (Action): the action to evaluate

        Raises:
            NotImplementedError: If this method has not been overridden by
            concrete agent.

        Returns:
            float: the agents interpretation of the value of this state and
            action
        """
        return self.state_action_values[action]
