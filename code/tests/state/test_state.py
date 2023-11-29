from .create_test_state import create_test_state


def test_state_equality():
    # same
    zero_a = create_test_state(0)
    zero_b = create_test_state(0)

    one_a = create_test_state(1)
    one_b = create_test_state(1)

    assert zero_a is not zero_b
    assert one_a is not one_b

    # same objects
    assert zero_a == zero_a
    assert zero_b == zero_b
    assert one_a == one_a
    assert one_b == one_b

    # symmetry + equality in class
    assert zero_a == zero_b
    assert zero_b == zero_a
    assert one_a == one_b
    assert one_b == one_a

    assert zero_a != one_a
    assert one_b != zero_b

    assert zero_a != 1
    assert zero_a != 0
    assert zero_a != ""


def test_state_hash():
    zero_a = create_test_state(0).__hash__()
    zero_b = create_test_state(0).__hash__()

    assert zero_a == zero_b

    c = create_test_state(100).__hash__()
    d = create_test_state(100000).__hash__()

    assert c != d
    assert c != zero_a
    assert d != zero_a

    near_d = create_test_state(100001).__hash__()

    assert d != near_d

    assert hash(create_test_state(0)) == zero_a