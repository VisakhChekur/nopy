from dataclasses import InitVar
from typing import Any
from typing import Iterable
from typing import Optional
from typing import Union

from notion.properties.common_properties import BlockParent
from notion.properties.common_properties import DatabaseParent
from notion.properties.common_properties import PageParent
from notion.properties.common_properties import Parent
from notion.properties.common_properties import WorkspaceParent
from notion.properties.db_properties import DBCheckbox
from notion.properties.db_properties import DBCreatedBy
from notion.properties.db_properties import DBCreatedTime
from notion.properties.db_properties import DBDate
from notion.properties.db_properties import DBEmail
from notion.properties.db_properties import DBFiles
from notion.properties.db_properties import DBFormula
from notion.properties.db_properties import DBLastEditedBy
from notion.properties.db_properties import DBLastEditedTime
from notion.properties.db_properties import DBMultiSelect
from notion.properties.db_properties import DBNumber
from notion.properties.db_properties import DBPhoneNumber
from notion.properties.db_properties import DBProp
from notion.properties.db_properties import DBSelect
from notion.properties.db_properties import DBStatus
from notion.properties.db_properties import DBText
from notion.properties.db_properties import DBTitle
from notion.properties.db_properties import DBUrl

OptionalDict = Optional[dict[str, Any]]

# Type to properly parse properties, title, description.
IterableInitVars = InitVar[Optional[Iterable[dict[str, Any]]]]

# The ORDER MATTERS!! The base class MUST be the last one.
# Refer: https://pydantic-docs.helpmanual.io/usage/model_config/#smart-union
Parents = Union[DatabaseParent, PageParent, BlockParent, WorkspaceParent, Parent]
DBProps = Union[
    DBTitle,
    DBText,
    DBNumber,
    DBSelect,
    DBMultiSelect,
    DBDate,
    DBFiles,
    DBCheckbox,
    DBUrl,
    DBEmail,
    DBPhoneNumber,
    DBFormula,
    DBCreatedTime,
    DBCreatedBy,
    DBLastEditedTime,
    DBLastEditedBy,
    DBStatus,
    DBProp,
]
