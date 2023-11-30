from src.model.state.cell_entities import CellEntity
from src.model.state.state_builder import StateBuilder
from src.model.state.state_instance import StateInstance


def test_default_state():
    blank = StateBuilder().build()
    assert isinstance(blank, StateInstance)
    assert blank == StateInstance.get_blank_state()
    assert blank == StateBuilder().build()


def test_set_location():
    loc_1 = (10, 5)
    loc_2 = (5, 10)
    one = StateBuilder().set_agent_location(loc_1).build()
    two = StateBuilder().set_agent_location(loc_2).build()

    assert one.agent_location == loc_1
    assert two.agent_location == loc_2
    # test other properties are not changed
    assert one.agent_energy == two.agent_energy


def test_set_energy():
    e_1 = 10
    e_2 = 5
    one = StateBuilder().set_energy(e_1).build()
    two = StateBuilder().set_energy(e_2).build()

    assert one.agent_energy == e_1
    assert two.agent_energy == e_2

    assert one.agent_location == two.agent_location


def test_decrement_energy():
    base = 8
    offset = 5
    goal = base - offset

    start = StateBuilder().set_energy(base).build()
    assert start.agent_energy == base

    one_decrement = StateBuilder(start).decrement_energy(offset).build()

    assert one_decrement.agent_energy == goal

    reset_decrement = (
        StateBuilder(one_decrement)
        .set_energy(base)
        .decrement_energy(offset)
        .build()
    )

    assert one_decrement == reset_decrement

    minimum_energy = StateBuilder().decrement_energy(base * 100).build()

    assert minimum_energy.agent_energy == 0


def test_set_entity():
    test_loc = (1, 1)
    assert StateBuilder().build().entities.get(test_loc) is None

    agent_state = StateBuilder().set_entity(test_loc, CellEntity.agent).build()

    assert agent_state.entities.get(test_loc) == CellEntity.agent

    goal_state = (
        StateBuilder(agent_state).set_entity(test_loc, CellEntity.goal).build()
    )

    assert goal_state.entities.get(test_loc) == CellEntity.goal

    agent_state_2 = (
        StateBuilder(goal_state)
        .set_entity(test_loc, CellEntity.agent)
        .set_entity(test_loc, CellEntity.goal)
        .set_entity(test_loc, CellEntity.agent)
        .build()
    )

    assert agent_state == agent_state_2


def test_remove_entity():
    test_loc = (5, 6)

    assert StateBuilder().build().entities.get(test_loc) is None
    agent_state = StateBuilder().set_entity(test_loc, CellEntity.agent).build()
    assert agent_state.entities.get(test_loc) == CellEntity.agent
    removed_state = StateBuilder(agent_state).remove_entity(test_loc).build()
    assert removed_state.entities.get(test_loc) is None
    multi_remove = (
        StateBuilder()
        .set_entity(test_loc, CellEntity.agent)
        .remove_entity(test_loc)
        .set_entity(test_loc, CellEntity.agent)
        .build()
    )
    assert multi_remove == agent_state


def test_entity_locality():
    test_loc_a = (9, 7)
    test_loc_b = (0, 0)

    two_entities = (
        StateBuilder()
        .set_entity(test_loc_a, CellEntity.agent)
        .set_entity(test_loc_b, CellEntity.goal)
        .build()
    )

    assert two_entities.entities.get(test_loc_a) == CellEntity.agent
    assert two_entities.entities.get(test_loc_b) == CellEntity.goal

    swap_entities = (
        StateBuilder(two_entities)
        .set_entity(test_loc_a, CellEntity.goal)
        .set_entity(test_loc_b, CellEntity.agent)
        .build()
    )

    assert swap_entities.entities.get(test_loc_a) == CellEntity.goal
    assert swap_entities.entities.get(test_loc_b) == CellEntity.agent

    local_entity_removed = (
        StateBuilder(two_entities)
        .set_entity(test_loc_a, CellEntity.goal)
        .remove_entity(test_loc_b)
        .build()
    )

    assert local_entity_removed.entities.get(test_loc_a) == CellEntity.goal
    assert local_entity_removed.entities.get(test_loc_b) is None
