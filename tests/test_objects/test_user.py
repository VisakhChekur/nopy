from typing import Any

from nopy.enums import ObjectType
from nopy.enums import UserType
from nopy.objects.user import Bot
from nopy.objects.user import Person
from nopy.objects.user import User


def test_person_fd():

    args: dict[str, Any] = {
        "object": "user",
        "id": "user-id",
        "name": "Guacs",
        "avatar_url": "some url",
        "type": "person",
        "person": {"email": "guacs@awesome.com"},
    }
    person = User.from_dict(args)

    assert isinstance(person, Person)
    assert person.type == ObjectType.USER
    assert person.user_type == UserType.PERSON
    assert person.name == "Guacs"
    assert person.avatar_url == "some url"
    assert person.email == "guacs@awesome.com"


def test_bot_fd():

    args: dict[str, Any] = {
        "object": "user",
        "id": "bot-id",
        "name": "Python",
        "avatar_url": None,
        "type": "bot",
        "bot": {
            "owner": {"type": "workspace", "workspace": True},
            "workspace_name": "Pythonic Notion",
        },
    }
    bot = User.from_dict(args)

    assert isinstance(bot, Bot)
    assert bot.type == ObjectType.USER
    assert bot.user_type == UserType.BOT
    assert bot.name == "Python"
    assert bot.avatar_url is None
    assert bot.owner == "workspace"
    assert bot.workspace_name == "Pythonic Notion"
