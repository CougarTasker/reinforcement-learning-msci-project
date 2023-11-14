from .create_test_state import create_test_state
from src.model.state.state_pool import StatePool


def test_state_pool_get():
    s = StatePool()
    zero_a = create_test_state(0)
    zero_b = create_test_state(0)

    id_zero_a = s.get_state_id(zero_a)
    id_zero_b = s.get_state_id(zero_b)

    assert id_zero_a == id_zero_b
    assert isinstance(id_zero_a, int)

    one_a = create_test_state(1)
    one_b = create_test_state(1)
    id_one_a = s.get_state_id(one_a)
    id_one_b = s.get_state_id(one_b)

    assert id_one_a == id_one_b
    assert id_one_a != id_zero_a

    assert s.get_state_from_id(id_zero_a) is zero_a
    assert s.get_state_from_id(id_one_a) is one_a

def test_state_pool_has():
    s = StatePool()
    a = create_test_state(0)
    b = create_test_state(0)
    c = create_test_state(1)

    assert not s.is_existing_state(a)
    assert not s.is_existing_state(b)
    assert not s.is_existing_state(c)

    s.get_state_id(a)

    assert s.is_existing_state(a)
    assert s.is_existing_state(b)
    assert not s.is_existing_state(c)

    s.get_state_id(c)

    assert s.is_existing_state(a)
    assert s.is_existing_state(b)
    assert s.is_existing_state(c)


