from src.model.agents.base_agent import BaseAgent
from src.model.config.agent_section.agent_section import AgentConfig
from src.model.config.agent_section.epsilon_greedy import (
    EpsilonGreedyStrategyConfig,
)
from src.model.config.agent_section.mf_bpi import MFBPIConfig
from src.model.config.agent_section.q_learning import QLearningConfig
from src.model.config.agent_section.upper_confidence_bound import (
    UCBStrategyConfig,
)
from src.model.config.agent_section.value_iteration import ValueIterationConfig
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
    @property
    def width(self) -> int:
        return 2

    @property
    def height(self) -> int:
        return 1

    @property
    def agent_location(self) -> tuple[int, int]:
        return 0, 0

    @property
    def entity_count(self) -> int:
        return 0


class SimpleTestDynamics(BaseDynamics):
    def __init__(self) -> None:
        super().__init__(TestGridWorldConfig())

        self.left = self.initial_state()
        self.right = self.next(self.left, action=Action.right)[0]
        self.left_entity = self.next(self.right, Action.up)[0]
        self.right_entity = self.next(self.left, Action.up)[0]

        self.state_pool.id_to_state = {
            0: self.left,
            1: self.right,
            2: self.left_entity,
            3: self.right_entity,
        }
        self.state_pool.state_to_id = {
            self.left: 0,
            self.right: 1,
            self.left_entity: 2,
            self.right_entity: 3,
        }

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


class TestEpsilonGreedyStrategyConfig(EpsilonGreedyStrategyConfig):
    @property
    def initial_exploration_ratio(self) -> float:
        return 0.5

    @property
    def decay_rate(self) -> float:
        return 0.95


class TestUCBStrategyConfig(UCBStrategyConfig):
    @property
    def exploration_bias(self) -> float:
        """Weighting applied to the uncertainty in the recorded data.

        Higher values encourage more exploration.

        Returns:
            float: The value of potential reward.
        """
        return 0.5


class TestMFBPIConfig(MFBPIConfig):

    @property
    def kbar(self) -> int:
        return 1

    @property
    def ensemble_size(self) -> int:
        return 1


class TestQLearningConfig(QLearningConfig):
    def __init__(self):
        self.epsilon_greedy = TestEpsilonGreedyStrategyConfig()
        self.upper_confidence_bound = TestUCBStrategyConfig()
        self.mf_bpi = TestMFBPIConfig()

    @property
    def learning_rate(self) -> float:
        return 0.1

    @property
    def initial_optimism(self) -> float:
        return 1

    @property
    def replay_queue_length(self) -> int:
        return 5


class TestValueIterationConfig(ValueIterationConfig):
    @property
    def stopping_epsilon(self) -> float:
        return 0.0001

    @property
    def sample_count(self) -> int:
        return 100


class TestAgentConfig(AgentConfig):
    def __init__(self) -> None:
        self.q_learning = TestQLearningConfig()
        self.value_iteration = TestValueIterationConfig()

    @property
    def discount_rate(self) -> float:
        return 0.9


class MockAgent(BaseAgent):
    """Provides the common base for different learning agents."""

    def __init__(
        self,
        min_state: float,
        max_state: float,
        min_action: float,
        max_action: float,
    ) -> None:
        self.state_values = {
            0: min_state,
            1: (min_state + max_state) / 2,
            2: max_state,
            3: max_state,
        }
        self.state_action_values = {
            Action.up: min_action,
            Action.down: min_action,
            Action.left: max_action,
            Action.right: (min_action + max_action) / 2,
        }

    def evaluate_policy(self, state: int) -> Action:
        return Action.down

    def record_transition(self, *args) -> None:
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
