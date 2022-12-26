from abc import ABC
from typing import Dict, Any


class MediaContent(ABC):
    """
    Abstract class that inherits to the content classes
    ...
    Attributes
    ----------
    id: Any
        Identity number of the content, retrieved from the database
    name: str
        Name of the content
    """
    def __init__(self, name: str, id: int = None):
        self.id = id
        self.__name = name

    def __eq__(self, other):
        if isinstance(other, MediaContent):
            # compare the attribute value dictionaries
            return self.get_attr_value_mappings() == other.get_attr_value_mappings()
        else:
            return False

    def get_attr_value_mappings(self) -> Dict[str, Any]:
        """
        A dictionary that maps string attribute_names to attribute_values in order to facilitate database operations
        i.e. {attribute_name: attribute_value, ...}
        :return: {attribute_name: attribute_value, ...} dictionary
        """

        def remove_classname_prefix(text: str) -> str:
            """
            Remove the prefix from "__ClassName_attribute_name" or "__ParentClassName_attribute_name" and convert it to "attribute_name"
            :param text: string name of the attribute
            :return: plain string name of the attribute
            """
            text = text.replace(f"_{self.__class__.__name__}__", "") # remove the child class name prefix from the attribute
            text = text.replace(f"_{self.__class__.__bases__[0].__name__}__", "") # remove the parent class name prefix from the attribute
            return text

        return {remove_classname_prefix(key): value for key, value in self.__getattribute__("__dict__").items()}

    def get_name(self):
        return self.__name

    def edit_name(self, new_name: str):
        self.__name = new_name

    def get_content_type(self) -> str:
        """
        get the name of the class as text in order to map the class names into db tables for SQL db or document name for NoSQL db.
        :return: lowercase class name
        """
        return str.lower(self.__class__.__name__)
