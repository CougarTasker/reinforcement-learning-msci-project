from immutables import Map

from .cell_entities import CellEntity


class StateInstance(object):
    """This class represents a possible state in the grid world of this MDP."""

    def __init__(
        self,
        agent_location: tuple[int, int],
        entities: Map[tuple[int, int], CellEntity],
        agent_energy: int,
    ) -> None:
        """Initialise a new state.

        each state must be immutable. therefore to achieve a state with
        different properties a new state must be created, this is done by the
        dynamics.

        Args:
            agent_location (tuple[int, int]): _description_
            entities (Map[tuple[int, int], CellEntity]): _description_
            agent_energy (int): _description_
        """
        self.agent_location = agent_location
        self.entities = entities
        self.agent_energy = agent_energy

    @classmethod
    def get_blank_state(cls):
        """Create a blank state.

        Returns:
            _type_: _description_
        """
        return StateInstance((0, 0), Map(), 10)

    def __hash__(self) -> int:
        """Generate a hash value for this state.

        Helpful in speeding up indexing operations.

        Returns:
            int: the hash of this state
        """
        return hash((self.agent_location, self.entities, self.agent_energy))

    def __eq__(self, other: object) -> bool:
        """Test for equality between two states.

        Args:
            other (object): the other state to compare to

        Returns:
            bool: true if the two states can be considered equal.
        """
        if not isinstance(other, StateInstance):
            return False
        return (
            self.agent_location == other.agent_location
            and self.entities == other.entities
            and self.agent_energy == other.agent_energy
        )
