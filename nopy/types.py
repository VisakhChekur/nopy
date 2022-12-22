"""All the composite types used within the package."""

from typing import Union

import nopy.props.db_props as dbp
from nopy.props.base import ObjectProperty

DBProps = Union[
    dbp.DBText,
    dbp.DBNumber,
    dbp.DBSelect,
    dbp.DBStatus,
    dbp.DBMultiSelect,
    dbp.DBDate,
    dbp.DBPeople,
    dbp.DBFiles,
    dbp.DBCheckbox,
    dbp.DBUrl,
    dbp.DBEmail,
    dbp.DBPhoneNumber,
    dbp.DBFormula,
    dbp.DBRelation,
    dbp.DBRollup,
    dbp.DBCreatedBy,
    dbp.DBCreatedTime,
    dbp.DBLastEditedBy,
    dbp.DBLastEditedTime,
]
"""All the database properties."""

# This is going to include page properties when they're implemented as well.
Props = Union[DBProps, ObjectProperty]
"""All the properties."""
