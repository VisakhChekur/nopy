from notion.properties.common import RichText
from notion.properties.db_props import DBProp
from notion.objects.properties import Properties

def get_plain_text(rich_texts: list[RichText]) -> str:

    return " ".join((txt.plain_text for txt in rich_texts))

def get_properties_dict(properties: list[DBProp]) -> Properties:

    props = Properties()
    print(properties)
    for prop in properties:
        if prop == "Person":
            continue
        print(prop)
        props.set(prop.name, prop)
    return props