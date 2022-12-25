from nopy.props.common import RichText
from nopy.props.common import Text


class TextDescriptor:
    """Implementation of the descriptor protocol to handle attributes
    of classes that deal with arrays of `Text` properties."""

    def __init__(self, storage_name: str):

        # storage_name is the name of the attribute within
        # the class that holds the array which is to be used
        # when finding the plain text or vice versa
        self.storage_name = storage_name

    def __get__(self, instance: object, _):
        """Gets the combined plain text from a list of rich text."""

        rich_text: list[RichText] = instance.__dict__[self.storage_name]
        return " ".join(rt.plain_text for rt in rich_text)

    def __set__(self, instance: object, value: str):

        msg = f"value must be a string, use '{self.storage_name}' for adding text with style information"
        assert isinstance(value, str), msg

        instance.__dict__[self.storage_name] = [Text(value)]
