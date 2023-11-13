from os import path
from typing import Any

import toml

from .base_section import BaseConfigSection
from .grid_world_section import GridWorldConfig


class ConfigReader:
    """
    Configuration Reader, loads the program's configuration into memory and
    provides access to the sections of variables within. This class is a
    singleton to avoid redundant loads
    """

    config_file_name = "config.toml"
    """name of file to load configuration from"""
    _instance = None

    def __new__(cls):
        # https://python-patterns.guide/gang-of-four/singleton/
        if cls._instance is None:
            cls._instance = super(ConfigReader, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        """load or reload the configuration from the disk"""
        config_file_path = path.abspath(
            path.join(
                path.dirname(__file__), "..", "..", "..", self.config_file_name
            )
        )

        with open(config_file_path, "r") as config_file:
            self.__raw_config = toml.load(config_file)

    def __initialise_section(self, section: BaseConfigSection) -> Any:
        """internal method for populating a section object with data

        Args:
            section (BaseConfigSection): the section to populate

        Returns:
            BaseConfigSection: the section object that has been populated
        """
        data = self.__raw_config[section.section_name]
        section.initialise(data)
        return section

    def grid_world(self) -> GridWorldConfig:
        """Get the configuration for the environment.

        Returns:
            GridWorldConfig: an object that describes the environment
            configuration
        """
        return self.__initialise_section(GridWorldConfig())
