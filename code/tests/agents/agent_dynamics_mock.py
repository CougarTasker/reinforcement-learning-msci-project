from enum import Enum

import numpy as np
from src.model.config.grid_world_section import GridWorldConfig

from src.model.dynamics.actions import Action
from src.model.dynamics.base_dynamics import BaseDynamics
from tests.dynamics.mini_config import TestConfig


class VacuumStates(Enum):
    ddl = 0  # dirty dirty, bot left
    ddr = 1
    cdl = 2
    cdr = 3  # clean dirty, bot right
    dcl = 4
    dcr = 5
    cc = 6


class VacuumDynamics(BaseDynamics):
    def __init__(self) -> None:
        super().__init__(TestConfig())

    transitions = {
        # dd left right
        (VacuumStates.ddl.value, Action.right): (VacuumStates.ddr.value, 0),
        (VacuumStates.ddr.value, Action.left): (VacuumStates.ddl.value, 0),
        # dd clean
        (VacuumStates.ddl.value, Action.up): (VacuumStates.cdl.value, 1),
        (VacuumStates.ddr.value, Action.up): (VacuumStates.dcr.value, 1),
        # cd left right
        (VacuumStates.cdl.value, Action.right): (VacuumStates.cdr.value, 0),
        (VacuumStates.cdr.value, Action.left): (VacuumStates.cdl.value, 0),
        # dc left right
        (VacuumStates.dcl.value, Action.right): (VacuumStates.dcr.value, 0),
        (VacuumStates.dcr.value, Action.left): (VacuumStates.dcl.value, 0),
        # second clean
        (VacuumStates.dcl.value, Action.up): (VacuumStates.cc.value, 1),
        (VacuumStates.cdr.value, Action.up): (VacuumStates.cc.value, 1),
    }

    def is_stochastic(self) -> bool:
        return False

    def initial_state_id(self) -> int:
        """Provide the initial state id of this environment.

        Raises:
            NotImplementedError: If this method has not been overridden

        Returns:
            int: the starting state id.
        """
        return VacuumStates.ddl.value

    def next_state_id(
        self, current_state_id: int, action: Action
    ) -> tuple[int, float]:
        """Compute the next state and reward.

        Must only compute the next reward and state based on only the provided
        current state and reward to obey the markov property.

        Args:
            current_state_id (int): the state that the action is
            performed in
            action (Action): the action the agent has chosen


        Raises:
            NotImplementedError: If this method has not been overridden

        Returns:
            tuple[int, float]: the resulting state after the action has been
            performed and the reward from this action
        """
        next_state = self.transitions.get((current_state_id, action), None)
        if next_state is None:
            return current_state_id, 0
        return next_state


class TestAgentConfig:
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
        return float(np.finfo(np.float64).eps) * 2

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
        return 1
