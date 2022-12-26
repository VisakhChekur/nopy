# Suppported Features

The supported features by the library can be found here. More features such as blocks and comments will be added in future releases.

## Notion Objects

The Notion objects that are currently supported are:

- databases
- pages
- users

## Supported Endpoints

### Databases

- retrieving a database
- creating a database
- updating a database
- querying a database

### Page

- retrieving a page
- creating a page
- updating a page
- retrieving a page property

!!! warning "Retrieving a Page Property"

    This currently does NOT return a property property object, but instead returns the raw response returned by the Notion API.

### Users

- retrieve user
- list users
- retrieve me (the bot associated with the given integration token)
