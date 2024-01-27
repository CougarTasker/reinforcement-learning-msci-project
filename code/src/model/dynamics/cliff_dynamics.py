from typing import Set, Tuple

from src.model.config.grid_world_section import GridWorldConfig

from ..state.cell_entities import CellEntity
from ..state.state_builder import StateBuilder
from ..state.state_instance import StateInstance
from .actions import Action
from .base_dynamics import BaseDynamics

spawn_positions_type = Set[Tuple[int, int]]


class CliffDynamics(BaseDynamics):
    """Simple Dynamics where the agent should avoid the cliff."""

    def __init__(self, config: GridWorldConfig) -> None:
        """Initialise collection dynamics.

        Args:
            config (GridWorldConfig): the configuration used by this dynamics.
        """
        super().__init__(config)
        self.reset_location = (0, config.height() - 1)

    def is_stochastic(self) -> bool:
        """Determine weather the dynamics behave stochastically.

        Returns:
            bool: false, this dynamics is deterministic
        """
        return False

    def initial_state(self) -> StateInstance:
        """Provide the initial state of this environment.

        Raises:
            ValueError: if the config specifies an invalid state. such as the
                agent location being outside the bounds of the grid.

        Returns:
            StateInstance: the starting state.

        """
        if not self.grid_world.is_in_bounds(self.config.agent_location()):
            raise ValueError("config agent location outside of map bounds")

        initial_state_builder = (
            StateBuilder()
            .set_agent_location(self.config.agent_location())
            .set_energy(self.config.initial_energy())
        )
        cliff_y = self.config.height() - 1
        cliff_end_x = self.config.width() - 1
        for cliff_x in range(1, cliff_end_x):
            position = (cliff_x, cliff_y)
            initial_state_builder.set_entity(position, CellEntity.warning)

        goal_position = (cliff_end_x, cliff_y)
        initial_state_builder.set_entity(goal_position, CellEntity.goal)
        return initial_state_builder.build()

    def next(
        self, current_state: StateInstance, action: Action
    ) -> tuple[StateInstance, float]:
        """Compute the next state and reward.

        Must only compute the next reward and state based on only the provided
        current state and reward to obey the markov property.

        Args:
            current_state (StateInstance): the state that the action is
                performed in
            action (Action): the action the agent has chosen


        Returns:
            tuple[StateInstance, float]: the resulting state after the action
            has been performed and the reward from this action
        """
        next_state_builder = StateBuilder(current_state)
        next_agent_location = self.grid_world.movement_action(
            current_state.agent_location, action
        )
        if not self.grid_world.is_in_bounds(next_agent_location):
            return current_state, -1

        next_state_builder.set_agent_location(next_agent_location)

        if next_agent_location not in current_state.entities:
            return next_state_builder.build(), -1

        entity = current_state.entities.get(next_agent_location)
        next_state_builder.set_agent_location(self.reset_location)
        reset_state = next_state_builder.build()

        if entity is CellEntity.warning:
            return reset_state, -100

        return reset_state, 100
