from src.model.state.state_instance import StateInstance
from src.model.state.cell_entities import CellEntity
from immutables import Map


def create_test_state(sku: int) -> StateInstance:
    return StateInstance((sku, 0), Map({(0, sku): CellEntity.goal}), 10)
