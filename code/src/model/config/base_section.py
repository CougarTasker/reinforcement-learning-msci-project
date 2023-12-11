from typing import Any

from schema import Schema


class BaseConfigSection(object):
    """Base class for all config section views."""

    def __init__(
        self,
        section_name: str,
        schema: Schema,
    ) -> None:
        """Instantiate the basic data required for a config section.

        Args:
            section_name (str): the name of the section as it should appear in
                the config file
            schema (Schema): the schema to validate the data within this
                section.
        """
        self.schema = schema
        self.section_name = section_name

    def initialise(self, configuration: Any) -> None:
        """Populate section with data.

        This method lets the configuration reader to populate the view with
        data, it also performs validation at this stage, it will through an
        error if the data is not valid for this section

        Raises:
            Exception: thrown when the configuration file data is incorrect

        Args:
            configuration (Any): the raw configuration data to be used thought
                the application
        """
        self.configuration = self.schema.validate(configuration)
