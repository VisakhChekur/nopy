"""Generates code for various reasons. ONLY use during development."""


def create_enum(types: list[str], enum_name: str) -> str:

    enum_str: list[str] = [f"class {enum_name}(Enum):\n"]
    for t in types:
        t_str = f'    {t.upper()} = "{t}"'
        enum_str.append(t_str)

    return "\n".join(enum_str)


def create_simple_db_prop(prop: str) -> str:

    class_name = create_class_name(prop)
    prop_str: str = f"class DB{class_name}(DBProp):\n\n"
    prop_str += "    def __post_init__(self):\n"
    prop_str += f"        self.type = PropTypes.{prop.upper()}"
    return prop_str


def create_class_name(name: str, sep: str = "_") -> str:

    return "".join((n.capitalize() for n in name.split(sep)))


if __name__ == "__main__":

    props = [
        "title",
        "rich_text",
        "number",
        "select",
        "multi_select",
        "date",
        "people",
        "files",
        "checkbox",
        "url",
        "email",
        "phone_number",
        "formula",
        "relation",
        "rollup",
        "created_time",
        "created_by",
        "last_edited_time",
        "last_edited_by",
        "status",
    ]

    props_cls = ["DB" + create_class_name(prop) for prop in props]

    string = ""
    for name, cls in zip(props, props_cls):
        string += f'    "{name}": {cls},\n'

    print(string)
