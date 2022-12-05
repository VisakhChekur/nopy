from dataclasses import InitVar
from typing import Any
from typing import Iterable
from typing import Optional
from typing import Union

import notion.properties.common_properties as cp
import notion.properties.db_properties as dbp

OptionalDict = Optional[dict[str, Any]]

# Type to properly parse properties, title, description.
IterableInitVars = InitVar[Optional[Iterable[dict[str, Any]]]]

Parents = Union[cp.DatabaseParent, cp.PageParent, cp.BlockParent, cp.WorkspaceParent, cp.Parent]
DBProps = Union[
    dbp.DBTitle,
    dbp.DBText,
    dbp.DBNumber,
    dbp.DBSelect,
    dbp.DBMultiSelect,
    dbp.DBDate,
    dbp.DBFiles,
    dbp.DBCheckbox,
    dbp.DBUrl,
    dbp.DBEmail,
    dbp.DBPhoneNumber,
    dbp.DBFormula,
    dbp.DBCreatedTime,
    dbp.DBCreatedBy,
    dbp.DBLastEditedTime,
    dbp.DBLastEditedBy,
    dbp.DBStatus,
    dbp.DBProp,
]
