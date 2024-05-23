from random import random
from typing import Set, Tuple

from src.model.config.grid_world_section import GridWorldConfig

from ..state.cell_entities import CellEntity
from ..state.state_builder import StateBuilder
from ..state.state_instance import StateInstance
from .actions import Action
from .base_dynamics import BaseDynamics

spawn_positions_type = Set[Tuple[int, int]]


class WindDynamics(BaseDynamics):
    """Simple Dynamics where the agent should avoid the navigate the wind."""

    wind_probability = 0.4

    def __init__(self, config: GridWorldConfig) -> None:
        """Initialise collection dynamics.

        Args:
            config (GridWorldConfig): the configuration used by this dynamics.
        """
        super().__init__(config)
        self.reset_location = (0, config.height // 2)

    def is_stochastic(self) -> bool:
        """Determine weather the dynamics behave stochastically.

        Returns:
            bool: false, this dynamics is deterministic
        """
        return True

    def state_count_upper_bound(self) -> int:
        """Get an upper bound on the number of states.

        used for pre-allocating memory.

        Returns:
            int: an upper bound on the number of state.
        """
        return self.grid_world.width * self.grid_world.height

    def initial_state(self) -> StateInstance:
        """Provide the initial state of this environment.

        Raises:
            ValueError: if the config specifies an invalid state. such as the
                agent location being outside the bounds of the grid.

        Returns:
            StateInstance: the starting state.

        """
        initial_state_builder = StateBuilder().set_agent_location(
            self.reset_location
        )
        wind_start = self.config.width // 3
        for wind_x in range(wind_start, self.config.width):
            initial_state_builder.set_entity((wind_x, 0), CellEntity.wind_left)
            for wind_y in range(1, self.config.height):
                wind_loc = (wind_x, wind_y)
                initial_state_builder.set_entity(wind_loc, CellEntity.wind_up)

        goal_position = (self.config.width - 2, self.config.height // 2)
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

        entity = current_state.entities.get(current_state.agent_location, None)

        match entity:
            case CellEntity.wind_up:
                if random() < self.wind_probability:
                    next_agent_location = self.grid_world.movement_action(
                        current_state.agent_location, Action.up
                    )
                    next_state_builder.set_agent_location(next_agent_location)

                    return next_state_builder.build(), -1
            case CellEntity.wind_left:
                if random() < self.wind_probability:
                    next_agent_location = self.grid_world.movement_action(
                        current_state.agent_location, Action.left
                    )
                    next_state_builder.set_agent_location(next_agent_location)

                    return next_state_builder.build(), -1

            case CellEntity.goal:
                next_state_builder.set_agent_location(self.reset_location)
                return next_state_builder.build(), 100

        next_agent_location = self.grid_world.movement_action(
            current_state.agent_location, action
        )
        if not self.grid_world.is_in_bounds(next_agent_location):
            return current_state, -10

        next_state_builder.set_agent_location(next_agent_location)

        return next_state_builder.build(), 0
