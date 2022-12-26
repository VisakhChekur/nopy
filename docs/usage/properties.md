# Working with Properties

Properties on a database or page can be interacted with by using an instance of [`Properties`][properties]. All database and page instances have a `properties` attribute.

!!! info

    The below examples use a database, but all of them are applicable to pages as well unless specifically stated otherwise.

## Database and Page Properties

There are three kinds of properties:

- [common properties][common-properties]
- [database properties][database-properties]
- [page properties][page-properties]

!!! note

    Common properties aren't exactly properties, but rather they are common objects that are used within the database and page properties. Some of them such as `File` are also used directly within the metadata of Notion objects.

All database properties (prefixed with `DB`) and page properties (prefixed with `P`) have a `type` on them which is the property type. All the available property types can be found [here][nopy.enums.PropTypes]. Furthermore, they all have a `name` and an `id`.

## Basics of `Properties`

Finding the number of properties in a databse/page:

```py
    num_of_props = len(db.properties)
```

Checking if a property exists:

```py

    # Checking with the instance of a property
    prop in db.properties

    # Checking with the name/id of a property
    "property-name-or-id" in db.properties
```

Iterating through all the properties:

```py

    for prop in db.properties:
        ... # Work with the property
```


## Getting Properties from a Database/Page

```py

prop = db.properties.get("prop-id-or-name")

# Access like a dictionary
prop = db.properties["prop-id-or-name"]
```

## Adding Properties To a Database/Page

To add a property, simply use the `add()` method on a `Properties` instance.

```py
# Retrieving a database
...

new_prop = DBNumber(name="Number prop")
db.properties.add(new_prop)
db.update()
```
!!! warning

    While properties can be accessed using the square notation like in dictionaries, they can NOT be set using square notations. That is, the following WILL raise an errror:

        db.properties[some-key] = prop

## Deleting Existing Properties

Simply use the `pop()` method on a `Properties` instance.

```py

# Retrieving a database
...

deleted_prop = db.properties.pop("prop-id-or-name-or-prop-instance")
db.update()
```

!!! warning

    Deleting properties like this only works on databases. Deleting a property like this on a page does nothing.


## Editing Existing Properties

To edit a property, directly edit the property instance.

```py

# Retrieving a database
...

existing_select_prop = db.properties.get("prop-id-or-name")
existing_options = existing_select_prop.options # A list of Option instances

# Removing last option
existing_options.pop()

db.update()
```

The above method can **NOT** be used to edit the names of properties. To edit the names, first pop the property from the database properties, edit the name and then add it back again.

```py

# Retrieving a database
...

prop = db.properties.pop("prop-id-or-name-prop-instance")
prop.name = "New property name"
db.properties.add(prop)
```
