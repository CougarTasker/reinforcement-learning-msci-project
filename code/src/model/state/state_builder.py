from typing import Optional

from typing_extensions import Self

from .cell_entities import CellEntity
from .state_instance import StateInstance


class StateBuilder(object):
    """State builder simplifies creating states.

    Since states must be immutable the state builder lets you apply multiple
    changes without creating the intermediary states.
    """

    def __init__(
        self,
        previous_state: Optional[StateInstance] = None,
    ) -> None:
        """Initialise the state builder.

        Args:
            previous_state (Optional[StateInstance]): the state to build from,
                if not specified an arbitrary state is chosen.
        """
        if previous_state is None:
            previous_state = StateInstance.get_blank_state()

        self.entities = previous_state.entities
        self.agent_location = previous_state.agent_location
        self.agent_energy = previous_state.agent_energy

    def set_agent_location(self, pos: tuple[int, int]) -> Self:
        """Set the agent's location.

        Args:
            pos (tuple[int, int]): the agent's new location

        Returns:
            Self: the builder to continue chaining methods
        """
        self.agent_location = pos
        return self

    def set_energy(self, energy: int) -> Self:
        """Set the agent's energy.

        Args:
            energy (int): the agent's new energy

        Returns:
            Self: the builder to continue chaining methods
        """
        self.agent_energy = energy
        return self

    def decrement_energy(self, amount=1) -> Self:
        """Decrement the energy by an amount.

        Args:
            amount (int): the amount to reduce the energy by. Defaults to 1.

        Returns:
            Self: the builder to continue chaining methods
        """
        self.agent_energy -= amount
        if self.agent_energy < 0:
            self.agent_energy = 0
        return self

    def set_entity(self, cell: tuple[int, int], entity: CellEntity) -> Self:
        """Set the entity that is in a cell.

        Args:
            cell (tuple[int, int]): the cell where to update the entity.
            entity (CellEntity): the new entity at this location.

        Returns:
            Self: the builder to continue chaining methods
        """
        self.entities = self.entities.set(cell, entity)
        return self

    def remove_entity(self, cell: tuple[int, int]) -> Self:
        """Remove the entity that is in a cell.

        Args:
            cell (tuple[int, int]): the cell where to update an entity.

        Returns:
            Self: the builder to continue chaining methods
        """
        self.entities = self.entities.delete(cell)
        return self

    def build(self) -> StateInstance:
        """Compile the changes into the new state.

        Returns:
            StateInstance: the new state instance after the changes have been
            applied.
        """
        return StateInstance(
            self.agent_location, self.entities, self.agent_energy
        )
