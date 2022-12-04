from datetime import datetime
from typing import Optional, Union, Any
from dateutil import parser as date_parser
from notion.properties.db_props import *

from notion.properties.common import File, Emoji, RichText

# TODO: Update 'people' once User is implemented



def get_time(time: Optional[str]) -> Union[datetime, None]:

    if not time:
        return None
    
    return date_parser.parse(time)

def get_file(file_dict: dict[str, Any]) -> File:
    
    file_type = file_dict["type"]
    expiry_time_str = file_dict[file_type].get("expiry_time", None)
    expiry_time = get_time(expiry_time_str)

    return File(file_dict[file_type]["url"], file_type, expiry_time)

def get_icon(icon_dict: Optional[dict[str, Any]]) -> Union[File, Emoji,None]:

    if not icon_dict:
        return None
    
    if icon_dict["type"] == "emoji":
        return Emoji(icon_dict["emoji"])
    
    return get_file(icon_dict)

def get_rich_text(rich_text_dict: dict[str, Any]) -> RichText:

    return RichText()