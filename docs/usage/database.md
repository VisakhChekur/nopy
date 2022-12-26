# Working with Notion Databases

Notion databases are represented by the [`Database`][database] class.

## Retrieiving a Database

!!! note

    It's best practice to use the [`NotionClient`][notion-client] in a context manager. This will help clean up any resources left after the usage of client is finished. Alternatively, you can use the client without a context manager, but just remember to close the client with `client.close()`.

```py

with NotionClient() as client:

    db = client.retrieve_db("your-db-id")
```

## Creating a Database

To create a database, create a new instance of `Database` and serialize it and pass the serialized dictionary to the client.

```py
from nopy.objects import Database
from nopy.props import PageParent, Text

db = Database(
    rich_tite=[Text(plain_text="DB Title")]
)

# Adding a parent is a MUST.
db.parent = PageParent("page-id")

with NotionClient() as client:

    serialized_db = db.serialize()
    created_db = client.create_db(serialized_db)
```

## Editing a Database

To edit a database, simply edit the attributes available on a [`Database`][database] instance. Once you're done with your edits, call the [`update()`][objects.database.Database.update] method on the instance to actually update Notion with the new details regarding the database. Any changes made before the call to [`update()`][objects.database.Database.update] will be reflected.

```py
from nopy.props import File, Emoji

# Retrieiving database.
...

# Editing the database title.
db.title = "New title"

# Setting a new cover.
db.cover = File(url="url-to-cover-image")

# Setting a new icon.
db.icon = Emoji(emoji="😎")

# Updating Notion.
updated_db = db.update()

# Alternatively, you can update the database in place
db.update(in_place=True)
```

### A Note on Editing Rich Text Attributes

All the objects where there's a [rich text](https://developers.notion.com/reference/rich-text) attribute will have an attirbute which is the combined plain text as well as a `rich_*` version which is a list of [RichText][props.common.RichText] objects.

```py

db.description # The combined plain text.
db.rich_description # List of RichText objects.
```

Editing either will work, but there are a few differences. Editing the attribute with the combined plain text directly, will end up creating a simple text with no styling or extra features such as mentions etc. If you need those, edit the the corresponding `rich_*` attribute instead.

```py

# Creates no styling or anything of the sort in Notion.
db.description = "New description"

# This makes the 'New' in the description appear bold in Notion.
annotations = Annotations(bold=True)
txt_1 = Text(plain_text="New", annotations=annotations)
txt_2 = Text(plain_text="description")
db.rich_description = [txt_1, txt_2]
```

## Pages in a Database

### Retrieving Pages

For getting all the pages in database use the [`get_pages()`][objects.database.Database.get_pages] method on a [`Database`][database] instance. This returns a generator that yields a single page at a time.

!!! tip "Learn About Generators"

    Refer this excellent article on generators in Python to learn more about them: [Introduction To Python Generators](https://realpython.com/introduction-to-python-generators/)

```py

# Retrieving a database.
...

for page in db.get_pages():

    print(page.title) # Page title
```

To get a list of pages instead of a generator:

```py

# Using the list constructor
pages = list(db.get_pages())

# Or using list comprehensions
pages = [page for page in db.get_pages()]
```

### Creating Pages

To create a page in a database, use the [`create_page`][objects.database.Database.create_page] method on a [`Database`][database] instance.

```py
from nopy.objects import Page

# Retrieving a database
...

new_page = Page()
new_page.title = "New Page in DB"

created_page = db.create_page(new_page)
```

## Querying a Database

To query a database, use the [`query()`][objects.database.Database.query] method. The query method requires either a dictionary or a [`Query`][query] object.

```py
from nopy.filters import  Filter, NumberFilter, TextFilter
from nopy.sorts import PropertySort
from nopy.query import Query

# Retrieivng a database
...

# Creating the filters and sorts
filter_one = Filter(
    prop="prop-id-or-name-or-prop-instance",
    filter=TextFilter(contains="awesome"))
filter_two = Filter(
    prop="prop-id-or-name",
    filter=NumberFilter(less_than=4)
)
sort = PropertySort(
    property="prop-id-or-name-or-prop-instance",
    direction="ascending")

# Creating the query
query = Query(
    and_filters=[filter_one, filter_two],
    sorts=[sort]
)

for page in db.query(query):

    print(page.title)
```

All the possible filters and sorts can be found [here][query].
