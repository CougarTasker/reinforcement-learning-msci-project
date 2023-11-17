from ..dynamics.test_collection_dynamics import dynamics
from src.model.dynamics.collection_dynamics import CollectionDynamics
from src.model.agents.value_iteration.agent import ValueIterationAgent


def test_get_table(dynamics: CollectionDynamics):
    a = ValueIterationAgent(0.9, dynamics)
    a.get_value_table()
