# Welcome to NoPy!

NoPy is an unofficial OOP interface for the [Notion API](https://developers.notion.com/reference/intro).

## Installation

TODO.

## Getting Started

Create an instance of a `NotionClient` and pass in your integration token. Refer the [docs](https://developers.notion.com/docs/authorization#set-up-the-auth-flow-for-an-internal-integration) to find out how to set up the integration token and more.

```python

from nopy import NotionClient

client = NotionClient("your-notion-integration-token")

db = client.retrieve_db("your-db-id")

print(db.title) # The database title.
print(db.description) # The database description.

# Getting all the pages in the database.
for page in db.get_pages():
    print(page.title) # The page title.

# Closing the client.
client.close()
```

**NOTE**: Instead of passing in the integration token, you could instead store the token in the environment variables with the key `NOTION_TOKEN`.
