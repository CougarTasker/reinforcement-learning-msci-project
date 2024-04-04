from immutables import Map

from src.model.state.cell_entities import CellEntity
from src.model.state.state_instance import StateInstance


def create_test_state(sku: int) -> StateInstance:
    return StateInstance((sku, 0), Map({(0, sku): CellEntity.goal}))
