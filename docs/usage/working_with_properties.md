# Working with Properties On Notion Objects

All properties on any `Database` or `Page` instance can be accessed via the `properties` attribute on them. The `properties` attribute is an instance of `Properties` class. While the examples below are shown with a database, the same applies for pages as well.


!!! info

    The `Properties` class implements the [Collection](https://docs.python.org/3/library/collections.abc.html#collections.abc.Collection) abstract base class. This means it implements `__contains__`, `__iter__`, and `__len__` dunder methods.

## Basics of Properties Class


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

## Accessing a Property

Properties can be accessed similar to how values from dictionaries are accessed i.e. using the square notation. They can also be accessed using the `get()` method. The properties can be accessed using it's name or key.

!!! warning

    While properties can be accessed using the square notation, new properties can NOT be added in the same manner.

    ```py
        db.properties["property-name-or-id"] = prop # raises an error
    ```

```python

    # Retrieving a database
    ...

    # Accessing with square notation
    prop_one = db.properties["property-name-or-the-id"]

    # Accessing with the `get()` method
    prop_two = db.properties.get("propertty-name-or-the-id")
```

## Creating a New Property


TODO: Add the reference to add() and Property
To create a new property, simply use the `add()` method on an instance of a `Property` class.



```python

    from nopy.properties import db_properties as dbp

    # Retrieve a database
    ...

    # Creating a new text property on the database
    text_prop = dbp.DBText("Name of property")

    # Adding the property
    db.properties.add(text_prop)

    # Updating the database
    db.update()
```

!!! danger "Adding Properties with Same Name"

    Adding properties with the same name or id is not currently supported.

## Deleting a Property

Properties can be deleted from a Notion database/page by simply removing the property from the `properties` attribute. Properties can be deleted using it's name or id. If the property is not found a `PropertyNotFoundError` is raised.


```python

    # Retrieve a database
    ...

    # Deleting with name or id
    deleted_prop = db.properties.pop("property-name-or-id")

    # Updating the database
    db.update()
```

## Editing a Property

To edit an existing property on a database/page, simply mutate the attributes of the property instance directly. However, if you wish to edit the name of the property you **MUST** first delete/pop the property, change the name of the property and then add it again.

```python

    # Retrieving a database
    ...

    # Editing the expression in a formula property
    formula_prop = db.properties["property-name-or-id"]
    formula_prop.expression = "add(1, 1)"

    # Editing the name of a text property
    text_prop = db.properties.pop("property-name-or-id")
    text_prop.name = "New name"
    db.properties.add(text_prop)

    # Updating the database
    db.update()
```
