from os import path
from typing import Any

import toml

from .agent_section import AgentConfig
from .base_section import BaseConfigSection
from .grid_world_section import GridWorldConfig
from .gui_section import GUIConfig


class ConfigReader(object):
    """
    Configuration Reader.

    loads the program's configuration into memory and provides access to the
    sections of variables within. This class is a singleton to avoid redundant
    loading
    """

    config_file_name = "config.toml"
    _instance = None

    def __new__(cls):
        """Create a config object.

        Overridden to provide the singleton patten, there must only be one
        config object. to avoid redundant loading

        Returns:
            ConfigReader: The config object with the loaded data
        """
        # https://python-patterns.guide/gang-of-four/singleton/
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        """Load or reload the configuration from the disk."""
        config_file_path = path.abspath(
            path.join(
                path.dirname(__file__), "..", "..", "..", self.config_file_name
            )
        )

        with open(config_file_path, "r") as config_file:
            self.__raw_config = toml.load(config_file)

    def grid_world(self) -> GridWorldConfig:
        """Get the configuration for the environment.

        Returns:
            GridWorldConfig: an object that describes the environment
            configuration
        """
        return self.__initialise_section(GridWorldConfig())

    def gui(self) -> GUIConfig:
        """Get the configuration for the GUI.

        Returns:
            GUIConfig: an object that describes the gui
            configuration
        """
        return self.__initialise_section(GUIConfig())

    def agent(self) -> AgentConfig:
        """Get the configuration for agents.

        Returns:
            AgentConfig: an object that describes the agent
            configuration
        """
        return self.__initialise_section(AgentConfig())

    def __initialise_section(self, section: BaseConfigSection) -> Any:
        """Populate a section object with data.

        This is an internal method

        Args:
            section (BaseConfigSection): the section to populate

        Returns:
            Any: the section object that has been populated
        """
        section_raw_data = self.__raw_config[section.section_name]
        section.initialise(section_raw_data)
        return section
