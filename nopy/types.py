"""All the composite types used within the package."""

from typing import Union

import nopy.props.db_props as dbp
import nopy.props.page_props as pgp
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

PageProps = Union[
    pgp.PCheckbox,
    pgp.PCreatedTime,
    pgp.PCreatedby,
    pgp.PDate,
    pgp.PEmail,
    pgp.PFiles,
    pgp.PFormula,
    pgp.PLastEditedBy,
    pgp.PLastEditedTime,
    pgp.PMultiselect,
    pgp.PNumber,
    pgp.PPeople,
    pgp.PPhonenumber,
    pgp.PRelation,
    pgp.PRichtext,
    pgp.PRollup,
    pgp.PSelect,
    pgp.PStatus,
    pgp.PUrl,
]
"""All the page properties."""

# This is going to include page properties when they're implemented as well.
Props = Union[DBProps, PageProps, ObjectProperty]
"""All the properties."""
