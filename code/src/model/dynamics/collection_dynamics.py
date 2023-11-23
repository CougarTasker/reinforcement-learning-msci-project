from typing import Optional, Set, Tuple

from src.model.config.grid_world_section import GridWorldConfig

from ..state.cell_entities import CellEntity
from ..state.state_builder import StateBuilder
from ..state.state_instance import StateInstance
from .actions import Action
from .base_dynamics import BaseDynamics

spawn_positions_type = Set[Tuple[int, int]]


class CollectionDynamics(BaseDynamics):
    """Simple Dynamics where the agent can move to cells to collect goals."""

    def __init__(self, config: GridWorldConfig) -> None:
        """Initialise collection dynamics.

        Args:
            config (GridWorldConfig): the configuration used by this dynamics.
        """
        super().__init__(config)
        self.spawn_positions: Optional[spawn_positions_type] = None

    def is_stochastic(self) -> bool:
        """Determine weather the dynamics behave stochastically.

        Returns:
            bool: false, this dynamics is deterministic
        """
        return False

    def get_spawn_positions(self) -> spawn_positions_type:
        """Get the positions where flags can be spawned.

        these will be a number of unique positions in the grid world bounds.
        Initially chosen at random but then fixed for subsequent calls

        Returns:
            spawn_positions_type: the set of positions where goals can be
            spawned.
        """
        if self.spawn_positions is not None:
            return self.spawn_positions
        agent_location = self.config.agent_location()
        self.spawn_positions = set()
        while len(self.spawn_positions) < self.config.entity_count():
            location = self.grid_world.random_in_bounds_cell()
            if location != agent_location:
                self.spawn_positions.add(location)
        return self.spawn_positions

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

        for goal in self.get_spawn_positions():
            initial_state_builder.set_entity(goal, CellEntity.goal)

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
        if not current_state.entities:
            # Terminal state all goals have been collected, this should be an
            # absorbing state
            return current_state, 0

        next_state_builder = StateBuilder(current_state)
        next_agent_location = self.grid_world.movement_action(
            current_state.agent_location, action
        )
        if not self.grid_world.is_in_bounds(next_agent_location):
            return current_state, 0

        next_state_builder.set_agent_location(next_agent_location)

        if next_agent_location not in current_state.entities:
            return next_state_builder.build(), 0

        next_state_builder.remove_entity(next_agent_location)
        return next_state_builder.build(), 1