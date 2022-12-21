from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any
from typing import Literal
from typing import Optional
from typing import Type

from nopy.enums import ObjectTypes
from nopy.enums import UserTypes
from nopy.objects.notion_object import BaseObject

if TYPE_CHECKING:
    from nopy.client import NotionClient


@dataclass
class User(BaseObject):
    """The base class for a user in Notion."""

    name: Optional[str] = None
    avatar_url: Optional[str] = None

    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = ObjectTypes.USER
        self._user_type = UserTypes.UNSPPORTED

    @property
    def user_type(self):
        return self._user_type

    @classmethod
    def from_dict(cls: Type[User], args: dict[str, Any]) -> User:

        # This means it's a partial user as returned
        # in `created_by` etc.
        if "type" not in args:
            return User(args["id"])

        if args["type"] == "person":
            return Person.from_dict(args)
        return Bot.from_dict(args)


@dataclass
class Person(User):
    """A 'person' user in Notion.

    Attributes:
        name: The name of the user as displayed in Notion, if provided.
        avatar_url: The URL to the avatar, if any.
        email: The email of the user.
        user_type (UserType):
            The type of the user which will always be
            `UserTypes.PERSON`.
    """

    email: Optional[str] = None

    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._user_type = UserTypes.PERSON

    @classmethod
    def from_dict(cls: Type[Person], args: dict[str, Any]) -> Person:

        new_args: dict[str, Any] = {
            "id": args["id"],
            "name": args.get("name", None),
            "avatar_url": args.get("avatar_url", None),
        }
        person = args.get(UserTypes.PERSON.value, None)
        if person:
            new_args["email"] = person.get("email", None)

        return Person(**new_args)


@dataclass
class Bot(User):
    """A 'bot' user in Notion.

    Attributes:
        name: The name of the bot as displayed in Notion, if provided.
        avatar_url: The URL to the avatar, if any.
        owner:
            The owner of the bot which can be `user` or `workspace`.
        workspace_name:
            The workspace that owns the bot. This is only present if the
            bot's owner is `workspace`.
    """

    owner: Literal["workspace", "user"] = "user"
    workspace_name: Optional[str] = None

    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._user_type = UserTypes.BOT

    @classmethod
    def from_dict(cls: Type[Bot], args: dict[str, Any]) -> Bot:

        new_args: dict[str, Any] = {
            "id": args["id"],
            "name": args.get("name", None),
            "avatar_url": args.get("avatar_url", None),
        }
        bot = args.get(UserTypes.BOT.value, None)
        if bot:
            new_args["owner"] = bot["owner"]["type"]
            new_args["workspace_name"] = bot.get("workspace_name", None)

        return Bot(**new_args)
