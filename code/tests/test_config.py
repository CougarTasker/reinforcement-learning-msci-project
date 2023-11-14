from src.model.config.reader import ConfigReader
import pytest


@pytest.fixture(autouse=True)
def config_cleanup():
    ConfigReader._instance = None


test_file = """
[grid_world]
width = 16
height = 9
entity_count = 5
[grid_world.energy]
energy_capacity=10
initial_energy=10
[grid_world.agent_location]
x = 10
y = 10
"""


def test_singleton(mocker):
    mock_open = mocker.patch("builtins.open")
    mock_open.return_value.__enter__.return_value.read.return_value = test_file

    a = ConfigReader()
    b = ConfigReader()
    assert a is b


def test_load_config_correctly(mocker):
    mock_open = mocker.patch("builtins.open")
    mock_open.return_value.__enter__.return_value.read.return_value = test_file

    config = ConfigReader()

    assert mock_open.call_args.args[0].endswith(config.config_file_name)
    assert mock_open.call_args.args[1] == "r"

    grid_config = config.grid_world()

    assert grid_config.width() == 16
    assert grid_config.height() == 9


test_missing = """
[grid_world]
width = 16
"""


def test_validate_missing_data(mocker):
    mock_open = mocker.patch("builtins.open")
    mock_open.return_value.__enter__.return_value.read.return_value = (
        test_missing
    )
    config = ConfigReader()
    with pytest.raises(Exception):
        config.grid_world()


test_incorrect_data = """
[grid_world]
width = true
height = false
entity_count = 5
[grid_world.energy]
energy_capacity=10
initial_energy=10
[grid_world.agent_location]
x = 10
y = 10
"""


def test_validate_incorrect_data(mocker):
    mock_open = mocker.patch("builtins.open")
    mock_open.return_value.__enter__.return_value.read.return_value = (
        test_incorrect_data
    )
    config = ConfigReader()
    with pytest.raises(Exception):
        config.grid_world()
