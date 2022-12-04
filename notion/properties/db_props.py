"""A module that implements all Database properties of Notion."""
from enum import Enum
from typing import Any

from dataclasses import dataclass, field
import dataclasses
from notion.properties.common import Option, StatusGroup
from notion.properties.types_enums import NumberFormats, PropTypes


@dataclass
class DBProp:
    """Base class for all database properties.
    
    Args:
        name: The name of the property as it appears in Notion.
        id: The id of the property. Not needed when creating a new property.
        type: The type of the property.
    """

    name: str
    _: dataclasses.KW_ONLY
    id: str = ""

    def __post_init__(self):

        self.type: PropTypes = PropTypes.UNSUPPORTED  

    def serialize(self) -> dict[str, Any]:  
        """Serializes instance to dictionary following Notion spec."""

        serialized: dict[str, Any] = {
            # It MUST be an empty dictionary if there are no configs
            # 'None' does NOT work
            self.type.value: {}
        }

        # Returning early if the type requires no configurations
        if hasattr(self, self.type.value):
            return serialized


        attrs = self.__dict__.copy()
        for key in ("name", "id", "type"):
            attrs.pop(key)

        type_configurations = serialized[self.type.value]
        for key, value in attrs.items():
            
            if isinstance(value, Enum):
                serialized_val = value.value
            elif getattr(value, "serialize", None):
                serialized_val = value.serialize()
            else:
                serialized_val = value
            type_configurations[key] = serialized_val

        return serialized

@dataclass
class DBTitle(DBProp):
    """Representation of a title property in a database."""

    def __post_init__(self):
        self.type: PropTypes = PropTypes.TITLE
        # TODO: Check if a None here works
        self.title = None

        

@dataclass
class DBText(DBProp):
    """Representation of a text property in a database."""

    def __post_init__(self):
        self.type: PropTypes = PropTypes.RICH_TEXT
        self.rich_text = None
    
@dataclass
class DBNumber(DBProp):
    
    format: NumberFormats = NumberFormats.NUMBER

    def __post_init__(self):
        self.type = PropTypes.NUMBER



@dataclass
class DBSelect(DBProp):

    options: list[Option] = field(default_factory=list)

    def __post_init__(self):
        self.type = PropTypes.SELECT
    
    def serialize(self) -> dict[str, Any]:

        serialized = super().serialize()
        serialized[self.type.value]["options"] = [opt.serialize() for opt in self.options]
        return serialized


@dataclass
class DBStatus(DBProp):

    options: list[Option] = field(default_factory=list)
    groups: list[StatusGroup] = field(default_factory=list)

    def __post_init__(self):
        self.type = PropTypes.STATUS

    def serialize(self) -> dict[str, Any]:

        serialized = super().serialize()
        serialized[self.type.value]["options"] = [opt.serialize() for opt in self.options]
        serialized[self.type.value]["groups"] = [group.serialize() for group in self.groups]
        return serialized

@dataclass
class DBMultiSelect(DBProp):

    options: list[Option] = field(default_factory=list)

    def __post_init__(self):
        self.type = PropTypes.MULTI_SELECT

    def serialize(self) -> dict[str, Any]:

        serialized = super().serialize()
        serialized[self.type.value]["options"] = [opt.serialize() for opt in self.options]
        return serialized
    
@dataclass
class DBDate(DBProp):

    def __post_init__(self):
        self.type = PropTypes.DATE
        self.date = None

@dataclass
class DBPeople(DBProp):

    def __post_init__(self):
        self.type = PropTypes.PEOPLE
        self.people = None

@dataclass
class DBFile(DBProp):


    def __post_init__(self):
        self.type = PropTypes.FILES

@dataclass
class DBCheckbox(DBProp):

    def __post_init__(self):
        self.type = PropTypes.CHECKBOX
        self.checkbox = None

@dataclass
class DBUrl(DBProp):

    def __post_init__(self):
        self.type = PropTypes.URL
        self.url = None

@dataclass
class DBEmail(DBProp):

    def __post_init__(self):
        self.type = PropTypes.EMAIL
        self.email = None

@dataclass
class DBPhoneNumber(DBProp):

    def __post_init__(self):
        self.type = PropTypes.PHONE_NUMBER
        self.phone_number = None

@dataclass
class DBFormula(DBProp):

    expression: str

    def __post_init__(self):
        self.type = PropTypes.FORMULA
    
@dataclass
class DBCreatedTime(DBProp):

    def __post_init__(self):
        self.type = PropTypes.CREATED_TIME
        self.created_time = None

@dataclass
class DBCreatedBy(DBProp):

    def __post_init__(self):
        self.type = PropTypes.CREATED_BY
        self.created_by = None

@dataclass
class DBLastEditedTime(DBProp):

    def __post_init__(self):
        self.type = PropTypes.LAST_EDITED_TIME
        self.last_edited_time = None

@dataclass
class DBLastEditedBy(DBProp):

    def __post_init__(self):
        self.type = PropTypes.LAST_EDITED_BY
        self.last_edited_by = None