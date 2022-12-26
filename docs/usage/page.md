# Working with Notion pages

Notion pages are represented by the [`Page`][page] class.

## Retrieiving a page

!!! note

    It's best practice to use the [`NotionClient`][notion-client] in a context manager. This will help clean up any resources left after the usage of client is finished. Alternatively, you can use the client without a context manager, but just remember to close the client with `client.close()`.

```py

with NotionClient() as client:

    page = client.retrieve_page("your-page-id")
```

## Creating a page

To create a page, create a new instance of [`Page`][page] and serialize it and pass the serialized dictionary to the client.

```py
from nopy.objects import Page
from nopy.props import PageParent, Text

page = Page(
    rich_tite=[Text(plain_text="page Title")]
)

# Adding a parent is a MUST.
page.parent = PageParent("page-id")

with NotionClient() as client:

    serialized_page = page.serialize()
    created_page = client.create_page(serialized_page)
```

## Editing a page

To edit a page, simply edit the attributes available on a [`Page`][page] instance. Once you're done with your edits, call the [`update()`][objects.page.Page.update] method on the instance to actually update Notion with the new details regarding the page. Any changes made before the call to [`update()`][objects.page.Page.update] will be reflected.

```py
from nopy.props import File, Emoji

# Retrieiving page.
...

# Editing the page title.
page.title = "New title"

# Setting a new cover.
page.cover = File(url="url-to-cover-image")

# Setting a new icon.
page.icon = Emoji(emoji="😎")

# Updating Notion.
updated_page = page.update()

# Alternatively, you can update the page in place
page.update(in_place=True)
```
