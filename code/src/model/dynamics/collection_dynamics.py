from typing import Set

from ..state.cell_entities import CellEntity
from ..state.state_builder import StateBuilder
from ..state.state_instance import StateInstance
from .actions import Action
from .base_dynamics import BaseDynamics


class CollectionDynamics(BaseDynamics):
    """Simple Dynamics where the agent can move to cells to collect goals."""

    def initial_state(self) -> StateInstance:
        """Provide the initial state of this environment.

        Returns:
            StateInstance: the starting state.
        """
        initial_state_builder = (
            StateBuilder()
            .set_agent_location(self.config.agent_location())
            .set_energy(self.config.initial_energy())
        )

        goal_locations: Set[tuple[int, int]] = set()
        while len(goal_locations) < self.config.entity_count():
            goal_locations.add(self.grid_world.random_in_bounds_cell())

        for goal in goal_locations:
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
