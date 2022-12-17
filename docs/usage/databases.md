All Notion databases are mapped to instances of the [`Database`][database] class.

## Retrieving a Database

```python

    client = NotionClient()

    # retrieving a database
    db = client.retrieve_db("your-db-id")
```

## Editing a Database

To edit a database, simply edit the attributes available on the `Database` instance. Once you're done with your edits, call the `update()` method on the instance to actually update Notion with the new details regarding the database. Any changes made before the call to `update()` will be reflected.


!!! info

    We will see how to edit and create properties later in the [Working with Properties][working-with-properties] section.

```python

    from nopy import NotionClient
    from nopy.properties import common_properties as cp

    client = NotionClient()

    # retrieving a database
    db = client.retrieve_db("your-db-id")

    # Adding a new cover image to the database
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
!!! warning

    When editing any text with styling, such as title, editing the text attribute directly will remove any styling that may be applied on it. If you want to have styling, edit the corresponding `rich_*` attribute instead.


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
        ... # do whatever it is that you want to do with the page
```

If you want all the pages in a list, replicate the following:

```python

    # Retrieving a database
    ...

    pages: list[Page] = [page for page in db.get_pages()]
```

### Filtering and Sorting Pages

For filtering and sorting pages, use the [`query()`][objects.db.Database.query] method on the database which requires an instance of a [`Query`][query.query.Query] class.

Add filters to the [`Query`][query.query.Query] instance using the various filters available which can be seen [here][query.filters-classes].

Add sorts to the [`Query`][query.query.Query] instance using the sorts available which can be seen [here][add sorts link]

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
