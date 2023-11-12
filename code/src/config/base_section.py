from schema import Schema
from typing import Any


class BaseConfigSection:
    """Base class for all config section views"""

    def __init__(
        self,
        section_name: str,
        schema: Schema,
    ) -> None:
        """Instantiates the basic data required for a config section

        Args:
            section_name (str): the name of the section as it should appear in
            the config file
            schema (Schema): the schema to validate the data within this
            section.
        """
        self.schema = schema
        self.section_name = section_name

    def initialise(self, data: Any) -> None:
        """This method lets the configuration reader to populate the view with
        data, it also performs validation at this stage, it will through an
        error if the data is not valid for this section

        Args:
            data (any): _description_
        """
        self.data = self.schema.validate(data)
