# Welcome to NoPy

NoPy is an unofficial client for the Notion API.

## Features

- object-oriented interface
- update and interact with databases and pages in a user-friendly manner

## Quickstart

```python

    from nopy import NotionClient

    NOTION_TOKEN = "your-secret-integration-token"
    client = NotionClient(NOTION_TOKEN)

    DB_ID = "your-db-id"
    db = client.retrieve_db(DB_ID)

    db_title = db.title # the database title
    db_cover = db.cover # the cover image of the database

    for page in db.get_pages():
        print(page.title) # prints the title of each page within the database

```
