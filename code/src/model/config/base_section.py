from typing import Any, Dict, List

from schema import Schema


class BaseConfigSection(object):
    """Base class for all config section views."""

    def __init__(
        self,
        section_name: str,
        schema: Dict[str, Any],
        subsections: List["BaseConfigSection"],
    ) -> None:
        """Instantiate the basic data required for a config section.

        Args:
            section_name (str): the name of the section as it should appear in
                the config file
            schema (Dict): the schema to validate the data within this
                section.
            subsections (Dict[str, BaseConfigSection]): any subsections in this
                section.
        """
        self.schema = schema
        self.section_name = section_name
        self.subsections = subsections
        self.configuration: Any = None

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
        # add the keys for the subsection so they dont cause an error
        subsection_keys = {
            subsection.section_name: object for subsection in self.subsections
        }

        self.configuration = Schema(
            {**self.schema, **subsection_keys}
        ).validate(configuration)

        for subsection in self.subsections:
            sub_configuration = configuration[subsection.section_name]
            subsection.initialise(sub_configuration)
