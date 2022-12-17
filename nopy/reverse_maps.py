from typing import Type

from .properties import common_properties as cp
from .properties import db_properties as dbp
from .properties import page_properties as pgp
from .typings import DBProps
from .typings import PageProps
from .typings import Parents

PARENT_REVERSE_MAP: dict[str, Type[Parents]] = {
    "database_id": cp.DatabaseParent,
    "page_id": cp.PageParent,
    "block_id": cp.BlockParent,
    "workspace": cp.WorkspaceParent,
}

DB_PROPS_REVERSE_MAP: dict[str, Type[DBProps]] = {
    "title": dbp.DBTitle,
    "rich_text": dbp.DBText,
    "number": dbp.DBNumber,
    "select": dbp.DBSelect,
    "multi_select": dbp.DBMultiSelect,
    "date": dbp.DBDate,
    "files": dbp.DBFiles,
    "checkbox": dbp.DBCheckbox,
    "url": dbp.DBUrl,
    "email": dbp.DBEmail,
    "phone_number": dbp.DBPhoneNumber,
    "formula": dbp.DBFormula,
    "created_time": dbp.DBCreatedTime,
    "created_by": dbp.DBCreatedBy,
    "last_edited_time": dbp.DBLastEditedTime,
    "last_edited_by": dbp.DBLastEditedBy,
    "status": dbp.DBStatus,
    "unsupported": dbp.DBProp,
}

PAGE_PROPS_REVERSE_MAP: dict[str, Type[PageProps]] = {
    "unsupported": pgp.PProp,
    "title": pgp.PTitle,
    "rich_text": pgp.PText,
    "number": pgp.PNumber,
    "select": pgp.PSelect,
    "multi_select": pgp.PMultiSelect,
    "date": pgp.PDate,
    "formula": pgp.PFormula,
    "files": pgp.PFile,
    "checkbox": pgp.PCheckbox,
    "url": pgp.PUrl,
    "email": pgp.PEmail,
    "phone_number": pgp.PPhoneNumber,
    "created_time": pgp.PCreatedTime,
    "last_edited_time": pgp.PLastEditedTime,
}
