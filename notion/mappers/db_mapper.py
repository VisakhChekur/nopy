from notion.mappers.mapper import Mapper
from notion.objects.db import Database
from notion.properties.db_props import *
from notion.properties.common import *
import notion.mappers.helpers as helpers
from notion.properties.types_enums import NUMBER_FORMAT_REVERSE_MAP

class DBMapper(Mapper):
    """Maps the given dictionary to a Database instance."""

    # These are cases where there are type configurations.
    _SPECIAL_CASES = {"select", "multi_select", "status", "number"}
    # These are the properties without any type configurations.
    _DB_SIMPLE_PROP_TYPE_MAP: dict[str, type[DBProp]] = {
    "title": DBTitle,
    "rich_text": DBText,
    "date": DBDate,
    "checkbox": DBCheckbox,
    "url": DBUrl,
    "email": DBEmail,
    "files": DBFile,
    "phone_number": DBPhoneNumber,
    "created_time": DBCreatedTime,
    "created_by": DBCreatedBy,
    "last_edited_time": DBLastEditedTime,
    "last_edited_by": DBLastEditedBy,
}


    def map(self, obj_dict: Optional[dict[str, Any]]=None) -> Database: # type: ignore

        if obj_dict:
            self._obj = obj_dict

        props = self._map_props()
        print(props)
        created_time = helpers.get_time(self._obj.get("created_time", None))
        last_edited_time = helpers.get_time(self._obj.get("last_edited_time", None))
        icon = helpers.get_icon(self._obj.get("icon", None))
        cover = helpers.get_file(self._obj.get("cover", None))

        return Database(
            self._obj["title"],
            props,
            created_time=created_time,
            created_by=None,
            last_edited_time=last_edited_time,
            last_edited_by=None,
            db_description=self._obj.get("description", None),
            icon=icon,
            cover=cover,
            parent=self._obj.get("parent", None),
            url=self._obj.get("url", None),
            is_inline=self._obj.get("is_inline", False),
            client=self._client
        )
    
    def _map_props(self) -> list[DBProp]:

        props: list[DBProp] = []
        for prop in self._obj["properties"].values():

            # special cases - select, multi_select, status
            if prop["type"] in self._SPECIAL_CASES:
                prop_instance = self._handle_special_prop(prop)
            else:
                prop_class = self._DB_SIMPLE_PROP_TYPE_MAP.get(prop["type"], None)
                if prop_class is None:
                    prop_instance = DBProp(prop["name"], id=prop["id"])
                else:
                    prop_instance = prop_class(prop["name"], id=prop["id"])
            props.append(prop_instance)        

        return props
    
    def _map_title(self) -> list[RichText]:

        rich_texts: list[RIchText] = []
        for text in self._obj["title"]:
            rich_text = RichText(**text)
            rich_texts.append(RichText(**text))

    def _handle_special_prop(self, prop_dict: dict[str, Any]) -> DBProp:

    # _SPECIAL_CASES = {"select", "multi_select", "status", "files", "number"}
        prop_type = prop_dict["type"]

        if prop_type == "select":
            prop_options = prop_dict["select"]["options"]
            options = [Option(**opt) for opt in prop_options]
            return DBSelect(prop_dict["name"], options, id=prop_dict["id"])

        if prop_type == "multi_select":
            prop_options = prop_dict["multi_select"]["options"]
            options = [Option(**opt) for opt in prop_options]
            return DBMultiSelect(prop_dict["name"], options, id=prop_dict["id"])
            

        if prop_type == "status":
            prop_options = prop_dict["status"]["options"]
            options = [Option(**opt) for opt in prop_options]
            
            prop_groups = prop_dict["status"]["groups"]
            groups = [StatusGroup(**grp) for grp in prop_groups]

            return DBStatus(prop_dict["name"], options, groups, id=prop_dict["id"])

        # Number
        num_format = NUMBER_FORMAT_REVERSE_MAP[prop_dict["number"]["format"]]
        return DBNumber(prop_dict["name"], num_format, id=prop_dict["id"])