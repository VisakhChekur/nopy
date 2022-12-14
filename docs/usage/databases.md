All Notion databases are mapped to instances of the [`Database`][database] class.

## Retrieving a Database

```python

    client = NotionClient()

    # retrieving a database
    db = client.retrieve_db("your-db-id")
```

## Editing a Database


#### Editing the Metadata of Databases

```python

    from nopy import NotionClient
    from nopy.properties import common_properties as cp

    client = NotionClient()

    # retrieving a database
    db = client.retrieve_db("your-db-id")

    # Adding a new cover image to the database
    # NOTE: The Notion API does not support uploading local files
    # via the API.
    cover = cp.File("url-to-the-file")


    # Editing the title and adding styles

    # Setting up the styles
    bold_style = cp.Annotations(bold=True)
    bold_and_underline_style = cp.Annotations(bold=True, underline=True)

    # Creating the title segments
    title_segment_one = cp.Text("Habit", annotations=bold_style)
    title_segment_two = cp.Text("Tracker", annotations=bold_and_underline_style)

    db.rich_title = [title_segment_one, title_segment_two]
    db.update()
```

When editing titles, make changes to the `rich_title` attribute on `Database` instances. Edits to the `title` attribute WILL be ignored during updation of databases.

#### Editing the Properties of Databases

All properties on a database can be accessed and manipulated via the `properties` attribute on a `Database` instance.  This `properties` attribute has an API similar to a Python dictionary.

!!! warning

    Properties of a can be accessed using the square notations like in normal Python dictionaries, however they can not be set using the square notation.

    ```python

        # Works fine
        prop = db.properties["property-name-or-id"]

        # Raises error
        db.properties["property-name-or-id"] = prop
    ```

##### Creating Properties

For creating a new property on a database, simply add a new instance of a `DBProp` to the `properties` attribute on the `Database` instance.


```python

    from nopy.properties import db_properties as dbp

    # Retrieve database
    ...

    new_checkbox_prop = dbp.DBCheckbox("I'm a checkbox property")
    db.properties.add_prop(new_checkbox_prop)

    db.update()
```

The above code will create a new checkbox property on the database.

##### Editing Existing Properties

For editing existing properties, manipulate the property that already exists within the `property` attribute on the `Database` instance.

```python

    from nopy.properties import common_properties as cp
    from nopy.properties import Colors

    # Retrieve database
    ...

    existing_select_prop = db.property["property-name-or-id"]

    # Adding a new option
    new_option = cp.Option(name="Brand New Option", color=Colors.PURPLE)
    existing_select_prop.options.append(new_option)

    # Editing the title of an existing property
    existing_email_prop = db.propety["property-name-or-id"]
    existing_email_prop.name = "New property name"

    db.update()
```

## Creating a Database

PENDING

## Querying a Database

### Getting All the Pages in a Database

For getting all the pages in a database, use the [`get_pages()`][objects.db.Database.get_pages] method on the database. This returns a generator which yields each page in the database.

!!! tip "Learn About Generators"

    Refer this excellent article on generators in Python to learn more about them: [Introduction To Python Generators](https://realpython.com/introduction-to-python-generators/)

```python

    # Retrieving a database
    ...

    for page in db.get_pages():
        print(page.title) # prints the page's title
```

### Filtering and Sorting Pages

For filtering and sorting pages, use the [`query()`][objects.db.Database.query] method on the database which requires an instance of a [`Query`][query.query.Query] class.

Add filters to the `Query` instance using the various filters available which can be seen [here][query.filters-classes].

Add sorts to the `Query` instance using the sorts available which can be seen [here][add sorts link]

```python
    from notion.query import Query, TextFilter, CheckboxFilter, PropertySort

    # Retrieve the database
    ...

    # Creating the filters
    filter_text = TextFilter(contains="contain this text")
    checkbox_filter = CheckboxFilter(equals=True)

    # Creating the sort
    sort_condition = PropertySort("property-name", direction="ascending")

    # Creating the query
    # NOTE: The filters and sorts must be passed in as lists.
    query = Query(
        and_filters=[filter_text],
        or_filters=[checkbox_filter],
        sorts=[sort_condition]
    )

    for page in db.query(query):
        print(page.title)
```
