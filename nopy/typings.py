from dataclasses import InitVar
from typing import Any
from typing import Iterable
from typing import Optional
from typing import Union

from .properties import common_properties as cp
from .properties import db_properties as dbp
from .properties import page_properties as pgp

OptionalDict = Optional[dict[str, Any]]

# Type to properly parse properties, title, description.
IterableInitVars = InitVar[Optional[Iterable[dict[str, Any]]]]

Parents = Union[
    cp.DatabaseParent, cp.PageParent, cp.BlockParent, cp.WorkspaceParent, cp.Parent
]
"""All Parent types."""

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
"""All database property types."""

PageProps = Union[
    pgp.PProp,
    pgp.PTitle,
    pgp.PText,
    pgp.PPhoneNumber,
    pgp.PMultiSelect,
    pgp.PSelect,
    pgp.PDate,
    pgp.PFormula,
    pgp.PFile,
    pgp.PCheckbox,
    pgp.PUrl,
    pgp.PEmail,
    pgp.PCreatedTime,
    pgp.PLastEditedTime,
]
"""All page property types."""

Props = Union[DBProps, PageProps]
"""All database AND page property types."""
