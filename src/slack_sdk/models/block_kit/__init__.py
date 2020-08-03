import copy
import logging
import re
import warnings
from abc import ABCMeta
from typing import Dict, List, Optional, Set, Union

from slack_sdk.models import (
    JsonObject,
    JsonValidator,
    show_unknown_key_warning,
    EnumValidator,
)
from slack_sdk.models.messages import Link

ButtonStyles = {"danger", "primary"}
DynamicSelectElementTypes = {"channels", "conversations", "users"}


class TextObject(JsonObject):
    attributes = {"text", "type", "emoji"}
    logger = logging.getLogger(__name__)

    def _subtype_warning(self):
        warnings.warn(
            "subtype is deprecated since slackclient 2.6.0, use type instead",
            DeprecationWarning,
        )

    @property
    def subtype(self) -> Optional[str]:
        return self.type

    @classmethod
    def parse(
        cls, text: Union[str, dict, "TextObject"], default_type: str = "mrkdwn"
    ) -> Optional["TextObject"]:
        if not text:
            return None
        elif isinstance(text, str):
            if default_type == PlainTextObject.type:
                return PlainTextObject.from_str(text)
            else:
                return MarkdownTextObject.from_str(text)
        elif isinstance(text, dict):
            d = copy.copy(text)
            t = d.pop("type")
            if t == PlainTextObject.type:
                return PlainTextObject(**d)
            else:
                return MarkdownTextObject(**d)
        elif isinstance(text, TextObject):
            return text
        else:
            cls.logger.warning(
                f"Unknown type ({type(text)}) detected when parsing a TextObject"
            )
            return None

    def __init__(
        self,
        text: str,
        type: Optional[str] = None,
        subtype: Optional[str] = None,
        emoji: Optional[bool] = None,
        **kwargs,
    ):
        """
        Super class for new text "objects" used in Block kit
        """
        if subtype:
            self._subtype_warning()

        self.text = text
        self.type = type if type else subtype
        self.emoji = emoji


class PlainTextObject(TextObject):
    type = "plain_text"

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"emoji"})

    def __init__(self, *, text: str, emoji: Optional[bool] = None):
        """A plain text object, meaning markdown characters will not be parsed as
        formatting information.
        https://api.slack.com/reference/block-kit/composition-objects#text
        """
        super().__init__(text=text, type=self.type)
        self.emoji = emoji

    @staticmethod
    def from_str(text: str) -> "PlainTextObject":
        return PlainTextObject(text=text, emoji=True)

    @staticmethod
    def direct_from_string(text: str) -> dict:
        """
        Transforms a string into the required object shape to act as a PlainTextObject
        """
        return PlainTextObject.from_str(text).to_dict()


class MarkdownTextObject(TextObject):
    type = "mrkdwn"

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"verbatim"})

    def __init__(self, *, text: str, verbatim: Optional[bool] = None):
        """A Markdown text object, meaning markdown characters will be parsed as
        formatting information.
        https://api.slack.com/reference/block-kit/composition-objects#text
        """
        super().__init__(text=text, type=self.type)
        self.verbatim = verbatim

    @staticmethod
    def from_str(text: str) -> "MarkdownTextObject":
        """Transforms a string into the required object shape to act as a MarkdownTextObject
        """
        return MarkdownTextObject(text=text)

    @staticmethod
    def direct_from_string(text: str) -> dict:
        """Transforms a string into the required object shape to act as a MarkdownTextObject
        """
        return MarkdownTextObject.from_str(text).to_dict()

    @staticmethod
    def from_link(link: Link, title: str = "") -> "MarkdownTextObject":
        """Transform a Link object directly into the required object shape to act as a MarkdownTextObject
        """
        if title:
            title = f": {title}"
        return MarkdownTextObject(text=f"{link}{title}")

    @staticmethod
    def direct_from_link(link: Link, title: str = "") -> dict:
        """Transform a Link object directly into the required object shape to act as a MarkdownTextObject
        """
        return MarkdownTextObject.from_link(link, title).to_dict()


class Option(JsonObject):
    """Option object used in dialogs, legacy message actions, and blocks
    JSON must be retrieved with an explicit option_type - the Slack API has
    different required formats in different situations
    """

    attributes = {}  # no attributes because to_dict has unique implementations
    logger = logging.getLogger(__name__)

    label_max_length = 75
    value_max_length = 75

    def __init__(
        self,
        *,
        value: str,
        label: Optional[str] = None,
        text: Optional[Union[str, dict, TextObject]] = None,  # Block Kit
        description: Optional[str] = None,
        url: Optional[str] = None,
        **others: dict,
    ):
        """
        An object that represents a single selectable item in a block element (
        SelectElement, OverflowMenuElement) or dialog element
        (StaticDialogSelectElement)

        Blocks:
        https://api.slack.com/reference/block-kit/composition-objects#option

        Dialogs:
        https://api.slack.com/dialogs#select_elements

        Legacy interactive attachments:
        https://api.slack.com/legacy/interactive-message-field-guide#option_fields

        Args:
            label: A short, user-facing string to label this option to users.
                Cannot exceed 75 characters.
            value: A short string that identifies this particular option to your
                application. It will be part of the payload when this option is selected
                . Cannot exceed 75 characters.
            description: A user-facing string that provides more details about
                this option. Only supported in legacy message actions, not in blocks or
                dialogs.
        """
        if text:
            self._text: Optional[TextObject] = TextObject.parse(text)
            self._label: Optional[str] = None
        else:
            self._text: Optional[TextObject] = None
            self._label: Optional[str] = label

        # for backward-compatibility with version 2.0-2.5, the following fields return str values
        self.text: Optional[str] = self._text.text if self._text else None
        self.label: Optional[str] = self._label

        self.value: str = value
        self.description: Optional[str] = description
        # A URL to load in the user's browser when the option is clicked.
        # The url attribute is only available in overflow menus.
        # Maximum length for this field is 3000 characters.
        # If you're using url, you'll still receive an interaction payload
        # and will need to send an acknowledgement response.
        self.url: Optional[str] = url
        show_unknown_key_warning(self, others)

    @JsonValidator(f"label attribute cannot exceed {label_max_length} characters")
    def _validate_label_length(self):
        return self._label is None or len(self._label) <= self.label_max_length

    @JsonValidator(f"text attribute cannot exceed {label_max_length} characters")
    def _validate_text_length(self):
        return (
            self._text is None
            or self._text.text is None
            or len(self._text.text) <= self.label_max_length
        )

    @JsonValidator(f"value attribute cannot exceed {value_max_length} characters")
    def _validate_value_length(self):
        return len(self.value) <= self.value_max_length

    @classmethod
    def parse_all(
        cls, options: Optional[List[Union[dict, "Option"]]]
    ) -> List["Option"]:
        if options is None:
            return None
        option_objects: List[Option] = []
        for o in options:
            if isinstance(o, dict):
                d = copy.copy(o)
                option_objects.append(Option(**d))
            elif isinstance(o, Option):
                option_objects.append(o)
            else:
                cls.logger.warning(f"Unknown option object detected and skipped ({o})")
        return option_objects

    def to_dict(self, option_type: str = "block") -> dict:
        """
        Different parent classes must call this with a valid value from OptionTypes -
        either "dialog", "action", or "block", so that JSON is returned in the
        correct shape.
        """
        self.validate_json()
        if option_type == "dialog":
            return {"label": self.label, "value": self.value}
        elif option_type == "action":
            json = {"text": self.label, "value": self.value}
            if self.description is not None:
                json["description"] = self.description
            return json
        else:  # if option_type == "block"; this should be the most common case
            text: TextObject = self._text or PlainTextObject.from_str(self.label)
            json: dict = {
                "text": text.to_dict(),
                "value": self.value,
            }
            if self.description:
                json["description"] = self.description
            if self.url:
                json["url"] = self.url
            return json

    @staticmethod
    def from_single_value(value_and_label: str):
        """
        Creates a simple Option instance with the same value and label
        """
        return Option(value=value_and_label, label=value_and_label)


class OptionGroup(JsonObject):
    """
    JSON must be retrieved with an explicit option_type - the Slack API has
    different required formats in different situations
    """

    attributes = {}  # no attributes because to_dict has unique implementations
    label_max_length = 75
    options_max_length = 100
    logger = logging.getLogger(__name__)

    def __init__(
        self,
        *,
        label: Optional[Union[str, dict, TextObject]] = None,
        options: List[Union[dict, Option]],
        **others: dict,
    ):
        """
        Create a group of Option objects - pass in a label (that will be part of the
        UI) and a list of Option objects.

        Blocks:
        https://api.slack.com/reference/block-kit/composition-objects#option-group

        Dialogs:
        https://api.slack.com/dialogs#select_elements

        Legacy interactive attachments:
        https://api.slack.com/legacy/interactive-message-field-guide#option_groups_to_place_within_message_menu_actions

        Args:
            label: Text to display at the top of this group of options.
            options: A list of no more than 100 Option objects.
        """  # noqa prevent flake8 blowing up on the long URL
        # default_type=PlainTextObject.type is for backward-compatibility
        self._label: Optional[TextObject] = TextObject.parse(
            label, default_type=PlainTextObject.type
        )
        self.label: Optional[str] = self._label.text if self._label else None
        self.options = Option.parse_all(options)  # compatible with version 2.5
        show_unknown_key_warning(self, others)

    @JsonValidator(f"label attribute cannot exceed {label_max_length} characters")
    def _validate_label_length(self):
        return self.label is None or len(self.label) <= self.label_max_length

    @JsonValidator(f"options attribute cannot exceed {options_max_length} elements")
    def _validate_options_length(self):
        return self.options is None or len(self.options) <= self.options_max_length

    @classmethod
    def parse_all(
        cls, option_groups: Optional[List[Union[dict, "OptionGroup"]]]
    ) -> Optional[List["OptionGroup"]]:
        if option_groups is None:
            return None
        option_group_objects = []
        for o in option_groups:
            if isinstance(o, dict):
                d = copy.copy(o)
                option_group_objects.append(OptionGroup(**d))
            elif isinstance(o, OptionGroup):
                option_group_objects.append(o)
            else:
                cls.logger.warning(
                    f"Unknown option group object detected and skipped ({o})"
                )
        return option_group_objects

    def to_dict(self, option_type: str = "block") -> dict:
        self.validate_json()
        dict_options = [o.to_dict(option_type) for o in self.options]
        if option_type == "dialog":
            return {
                "label": self.label,
                "options": dict_options,
            }
        elif option_type == "action":
            return {
                "text": self.label,
                "options": dict_options,
            }
        else:  # if option_type == "block"; this should be the most common case
            dict_label: dict = self._label.to_dict()
            return {
                "label": dict_label,
                "options": dict_options,
            }


class ConfirmObject(JsonObject):
    attributes = {}  # no attributes because to_dict has unique implementations

    title_max_length = 100
    text_max_length = 300
    confirm_max_length = 30
    deny_max_length = 30

    @classmethod
    def parse(cls, confirm: Union["ConfirmObject", dict]):
        if confirm:
            if isinstance(confirm, ConfirmObject):
                return confirm
            elif isinstance(confirm, dict):
                return ConfirmObject(**confirm)
            else:
                # TODO: warning
                return None

    def __init__(
        self,
        *,
        title: Union[str, dict, PlainTextObject],
        text: Union[str, dict, TextObject],
        confirm: Union[str, dict, PlainTextObject] = "Yes",
        deny: Union[str, dict, PlainTextObject] = "No",
        style: str = None,
    ):
        """
        An object that defines a dialog that provides a confirmation step to any
        interactive element. This dialog will ask the user to confirm their action by
        offering a confirm and deny button.
        https://api.slack.com/reference/block-kit/composition-objects#confirm
        """
        self._title = TextObject.parse(title, default_type=PlainTextObject.type)
        self._text = TextObject.parse(text, default_type=MarkdownTextObject.type)
        self._confirm = TextObject.parse(confirm, default_type=PlainTextObject.type)
        self._deny = TextObject.parse(deny, default_type=PlainTextObject.type)
        self._style = style

        # for backward-compatibility with version 2.0-2.5, the following fields return str values
        self.title = self._title.text if self._title else None
        self.text = self._text.text if self._text else None
        self.confirm = self._confirm.text if self._confirm else None
        self.deny = self._deny.text if self._deny else None
        self.style = self._style

    @JsonValidator(f"title attribute cannot exceed {title_max_length} characters")
    def title_length(self):
        return self._title is None or len(self._title.text) <= self.title_max_length

    @JsonValidator(f"text attribute cannot exceed {text_max_length} characters")
    def text_length(self):
        return self._text is None or len(self._text.text) <= self.text_max_length

    @JsonValidator(f"confirm attribute cannot exceed {confirm_max_length} characters")
    def confirm_length(self):
        return (
            self._confirm is None or len(self._confirm.text) <= self.confirm_max_length
        )

    @JsonValidator(f"deny attribute cannot exceed {deny_max_length} characters")
    def deny_length(self):
        return self._deny is None or len(self._deny.text) <= self.deny_max_length

    @JsonValidator('style for confirm must be either "primary" or "danger"')
    def _validate_confirm_style(self):
        return self._style is None or self._style in ["primary", "danger"]

    def to_dict(self, option_type: str = "block") -> dict:
        if option_type == "action":
            # deliberately skipping JSON validators here - can't find documentation
            # on actual limits here
            json = {
                "ok_text": self._confirm.text
                if self._confirm and self._confirm.text != "Yes"
                else "Okay",
                "dismiss_text": self._deny.text
                if self._deny and self._deny.text != "No"
                else "Cancel",
            }
            if self._title:
                json["title"] = self._title.text
            if self._text:
                json["text"] = self._text.text
            return json

        else:
            self.validate_json()
            json = {}
            if self._title:
                json["title"] = self._title.to_dict()
            if self._text:
                json["text"] = self._text.to_dict()
            if self._confirm:
                json["confirm"] = self._confirm.to_dict()
            if self._deny:
                json["deny"] = self._deny.to_dict()
            if self._style:
                json["style"] = self._style
            return json


# -------------------------------------------------
# Block Elements
# -------------------------------------------------


class BlockElement(JsonObject, metaclass=ABCMeta):
    """Block Elements are things that exists inside of your Blocks.
    https://api.slack.com/reference/block-kit/block-elements
    """

    attributes = {"type"}
    logger = logging.getLogger(__name__)

    def _subtype_warning(self):
        warnings.warn(
            "subtype is deprecated since slackclient 2.6.0, use type instead",
            DeprecationWarning,
        )

    @property
    def subtype(self) -> Optional[str]:
        return self.type

    def __init__(
        self,
        *,
        type: Optional[str] = None,
        subtype: Optional[str] = None,
        **others: dict,
    ):
        if subtype:
            self._subtype_warning()
        self.type = type if type else subtype
        show_unknown_key_warning(self, others)

    @classmethod
    def parse(
        cls, block_element: Union[dict, "BlockElement"]
    ) -> Optional["BlockElement"]:
        if block_element is None:
            return None
        elif isinstance(block_element, dict):
            if "type" in block_element:
                d = copy.copy(block_element)
                t = d.pop("type")
                if t == PlainTextObject.type:
                    return PlainTextObject(**d)
                elif t == MarkdownTextObject.type:
                    return MarkdownTextObject(**d)
                elif t == ImageElement.type:
                    return ImageElement(**d)
                elif t == ButtonElement.type:
                    return ButtonElement(**d)
                elif t == StaticSelectElement.type:
                    return StaticSelectElement(**d)
                elif t == StaticMultiSelectElement.type:
                    return StaticMultiSelectElement(**d)
                elif t == ExternalDataSelectElement.type:
                    return ExternalDataSelectElement(**d)
                elif t == ExternalDataMultiSelectElement.type:
                    return ExternalDataMultiSelectElement(**d)
                elif t == UserSelectElement.type:
                    return UserSelectElement(**d)
                elif t == UserMultiSelectElement.type:
                    return UserMultiSelectElement(**d)
                elif t == ConversationSelectElement.type:
                    return ConversationSelectElement(**d)
                elif t == ConversationMultiSelectElement.type:
                    return ConversationMultiSelectElement(**d)
                elif t == ChannelSelectElement.type:
                    return ChannelSelectElement(**d)
                elif t == ChannelMultiSelectElement.type:
                    return ChannelMultiSelectElement(**d)
                elif t == PlainTextInputElement.type:
                    return PlainTextInputElement(**d)
                elif t == RadioButtonsElement.type:
                    return RadioButtonsElement(**d)
                elif t == CheckboxesElement.type:
                    return CheckboxesElement(**d)
                elif t == OverflowMenuElement.type:
                    return OverflowMenuElement(**d)
                elif t == DatePickerElement.type:
                    return DatePickerElement(**d)
                else:
                    cls.logger.warning(
                        f"Unknown element detected and skipped ({block_element})"
                    )
                    return None
            else:
                cls.logger.warning(
                    f"Unknown element detected and skipped ({block_element})"
                )
                return None
        elif isinstance(block_element, (TextObject, BlockElement)):
            return block_element
        else:
            cls.logger.warning(
                f"Unknown element detected and skipped ({block_element})"
            )
            return None

    @classmethod
    def parse_all(
        cls, block_elements: List[Union[dict, "BlockElement"]]
    ) -> List["BlockElement"]:
        return [cls.parse(e) for e in block_elements or []]


# -------------------------------------------------
# Interactive Block Elements
# -------------------------------------------------


class InteractiveElement(BlockElement):
    action_id_max_length = 255

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"alt_text", "action_id"})

    def __init__(
        self,
        *,
        action_id: Optional[str] = None,
        type: Optional[str] = None,
        subtype: Optional[str] = None,
        **others: dict,
    ):
        if subtype:
            self._subtype_warning()
        super().__init__(type=type or subtype)
        show_unknown_key_warning(self, others)

        self.action_id = action_id

    @JsonValidator(
        f"action_id attribute cannot exceed {action_id_max_length} characters"
    )
    def _validate_action_id_length(self):
        return (
            self.action_id is None or len(self.action_id) <= self.action_id_max_length
        )


class InputInteractiveElement(InteractiveElement, metaclass=ABCMeta):
    placeholder_max_length = 150

    attributes = {"type", "action_id", "placeholder", "confirm"}

    def _subtype_warning(self):
        warnings.warn(
            "subtype is deprecated since slackclient 2.6.0, use type instead",
            DeprecationWarning,
        )

    @property
    def subtype(self) -> Optional[str]:
        return self.type

    def __init__(
        self,
        *,
        action_id: Optional[str] = None,
        placeholder: Union[str, TextObject] = None,
        type: Optional[str] = None,
        subtype: Optional[str] = None,
        confirm: Optional[Union[dict, ConfirmObject]] = None,
        **others: dict,
    ):
        """InteractiveElement that is usable in input blocks"""
        if subtype:
            self._subtype_warning()
        super().__init__(action_id=action_id, type=type or subtype)
        show_unknown_key_warning(self, others)

        self.placeholder = TextObject.parse(placeholder)
        self.confirm = ConfirmObject.parse(confirm)

    @JsonValidator(
        f"placeholder attribute cannot exceed {placeholder_max_length} characters"
    )
    def _validate_placeholder_length(self):
        return (
            self.placeholder is None
            or self.placeholder.text is None
            or len(self.placeholder.text) <= self.placeholder_max_length
        )


# -------------------------------------------------
# Button
# -------------------------------------------------


class ButtonElement(InteractiveElement):
    type = "button"
    text_max_length = 75
    url_max_length = 3000
    value_max_length = 2000

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"text", "url", "value", "style", "confirm"})

    def __init__(
        self,
        *,
        text: Union[str, dict, TextObject],
        action_id: Optional[str] = None,
        url: Optional[str] = None,
        value: Optional[str] = None,
        style: Optional[str] = None,  # primary, danger
        confirm: Optional[Union[dict, ConfirmObject]] = None,
        **others: dict,
    ):
        """An interactive element that inserts a button. The button can be a trigger for
        anything from opening a simple link to starting a complex workflow.
        https://api.slack.com/reference/block-kit/block-elements#button
        """
        super().__init__(action_id=action_id, type=self.type)
        show_unknown_key_warning(self, others)

        # NOTE: default_type=PlainTextObject.type here is only for backward-compatibility with version 2.5.0
        self.text = TextObject.parse(text, default_type=PlainTextObject.type)
        self.url = url
        self.value = value
        self.style = style
        self.confirm = ConfirmObject.parse(confirm)

    @JsonValidator(f"text attribute cannot exceed {text_max_length} characters")
    def _validate_text_length(self):
        return (
            self.text is None
            or self.text.text is None
            or len(self.text.text) <= self.text_max_length
        )

    @JsonValidator(f"url attribute cannot exceed {url_max_length} characters")
    def _validate_url_length(self):
        return self.url is None or len(self.url) <= self.url_max_length

    @JsonValidator(f"value attribute cannot exceed {value_max_length} characters")
    def _validate_value_length(self):
        return self.value is None or len(self.value) <= self.value_max_length

    @EnumValidator("style", ButtonStyles)
    def _validate_style_valid(self):
        return self.style is None or self.style in ButtonStyles


class LinkButtonElement(ButtonElement):
    def __init__(
        self,
        *,
        text: str,
        url: str,
        action_id: Optional[str] = None,
        style: Optional[str] = None,
        **others: dict,
    ):
        """A simple button that simply opens a given URL. You will still receive an
        interaction payload and will need to send an acknowledgement response.
        This is a helper class that makes creating links simpler.
        https://api.slack.com/reference/block-kit/block-elements#button
        """
        super().__init__(
            # NOTE: value must be always absent
            text=text,
            url=url,
            action_id=action_id,
            value=None,
            style=style,
        )
        show_unknown_key_warning(self, others)


# -------------------------------------------------
# Checkboxes
# -------------------------------------------------


class CheckboxesElement(InputInteractiveElement):
    type = "checkboxes"

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"options", "initial_options"})

    def __init__(
        self,
        *,
        action_id: Optional[str] = None,
        placeholder: Optional[str] = None,
        options: Optional[List[Union[dict, Option]]] = None,
        initial_options: Optional[List[Union[dict, Option]]] = None,
        confirm: Optional[Union[dict, ConfirmObject]] = None,
        **others: dict,
    ):
        """A checkbox group that allows a user to choose multiple items from a list of possible options.
        https://api.slack.com/reference/block-kit/block-elements#checkboxes
        """
        super().__init__(
            type=self.type,
            action_id=action_id,
            placeholder=TextObject.parse(placeholder, PlainTextObject.type),
            confirm=ConfirmObject.parse(confirm),
        )
        show_unknown_key_warning(self, others)

        self.options = Option.parse_all(options)
        self.initial_options = Option.parse_all(initial_options)


# -------------------------------------------------
# DatePicker
# -------------------------------------------------


class DatePickerElement(InputInteractiveElement):
    type = "datepicker"

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"initial_date"})

    def __init__(
        self,
        *,
        action_id: Optional[str] = None,
        placeholder: Optional[Union[str, dict, TextObject]] = None,
        initial_date: Optional[str] = None,
        confirm: Optional[Union[dict, ConfirmObject]] = None,
        **others: dict,
    ):
        """
        An element which lets users easily select a date from a calendar style UI.
        Date picker elements can be used inside of SectionBlocks and ActionsBlocks.
        https://api.slack.com/reference/block-kit/block-elements#datepicker
        """
        super().__init__(
            type=self.type,
            action_id=action_id,
            placeholder=TextObject.parse(placeholder, PlainTextObject.type),
            confirm=ConfirmObject.parse(confirm),
        )
        show_unknown_key_warning(self, others)

        self.initial_date = initial_date

    @JsonValidator("initial_date attribute must be in format 'YYYY-MM-DD'")
    def _validate_initial_date_valid(self):
        return self.initial_date is None or re.match(
            r"\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])", self.initial_date
        )


# -------------------------------------------------
# Image
# -------------------------------------------------


class ImageElement(BlockElement):
    type = "image"
    image_url_max_length = 3000
    alt_text_max_length = 2000

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"alt_text", "image_url"})

    def __init__(
        self,
        *,
        image_url: Optional[str] = None,
        alt_text: Optional[str] = None,
        **others: dict,
    ):
        """An element to insert an image - this element can be used in section and
        context blocks only. If you want a block with only an image in it,
        you're looking for the image block.
        https://api.slack.com/reference/block-kit/block-elements#image
        """
        super().__init__(type=self.type)
        show_unknown_key_warning(self, others)

        self.image_url = image_url
        self.alt_text = alt_text

    @JsonValidator(
        f"image_url attribute cannot exceed {image_url_max_length} characters"
    )
    def _validate_image_url_length(self):
        return len(self.image_url) <= self.image_url_max_length

    @JsonValidator(f"alt_text attribute cannot exceed {alt_text_max_length} characters")
    def _validate_alt_text_length(self):
        return len(self.alt_text) <= self.alt_text_max_length


# -------------------------------------------------
# Static Select
# -------------------------------------------------


class StaticSelectElement(InputInteractiveElement):
    type = "static_select"
    options_max_length = 100
    option_groups_max_length = 100

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"options", "option_groups", "initial_option"})

    def __init__(
        self,
        *,
        placeholder: Optional[Union[str, dict, TextObject]] = None,
        action_id: Optional[str] = None,
        options: Optional[List[Union[dict, Option]]] = None,
        option_groups: Optional[List[Union[dict, OptionGroup]]] = None,
        initial_option: Optional[Union[dict, Option]] = None,
        confirm: Optional[Union[dict, ConfirmObject]] = None,
        **others: dict,
    ):
        """This is the simplest form of select menu, with a static list of options passed in when defining the element.
        ps://api.slack.com/reference/block-kit/block-elements#static_select
        """
        super().__init__(
            type=self.type,
            action_id=action_id,
            placeholder=TextObject.parse(placeholder, PlainTextObject.type),
            confirm=ConfirmObject.parse(confirm),
        )
        show_unknown_key_warning(self, others)

        self.options = options
        self.option_groups = option_groups
        self.initial_option = initial_option

    @JsonValidator(f"options attribute cannot exceed {options_max_length} elements")
    def _validate_options_length(self):
        return self.options is None or len(self.options) <= self.options_max_length

    @JsonValidator(
        f"option_groups attribute cannot exceed {option_groups_max_length} elements"
    )
    def _validate_option_groups_length(self):
        return (
            self.option_groups is None
            or len(self.option_groups) <= self.option_groups_max_length
        )

    @JsonValidator("options and option_groups cannot both be specified")
    def _validate_options_and_option_groups_both_specified(self):
        return not (self.options is not None and self.option_groups is not None)

    @JsonValidator("options or option_groups must be specified")
    def _validate_neither_options_or_option_groups_is_specified(self):
        return self.options is not None or self.option_groups is not None


class StaticMultiSelectElement(InputInteractiveElement):
    type = "multi_static_select"
    options_max_length = 100
    option_groups_max_length = 100

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union(
            {"options", "option_groups", "initial_options", "max_selected_items"}
        )

    def __init__(
        self,
        *,
        placeholder: Optional[Union[str, dict, TextObject]] = None,
        action_id: Optional[str] = None,
        options: Optional[List[Option]] = None,
        option_groups: Optional[List[OptionGroup]] = None,
        initial_options: Optional[List[Option]] = None,
        confirm: Optional[Union[dict, ConfirmObject]] = None,
        max_selected_items: Optional[int] = None,
        **others: dict,
    ):
        """
        This is the simplest form of select menu, with a static list of options passed in when defining the element.
        https://api.slack.com/reference/block-kit/block-elements#static_multi_select
        """
        super().__init__(
            type=self.type,
            action_id=action_id,
            placeholder=TextObject.parse(placeholder, PlainTextObject.type),
            confirm=ConfirmObject.parse(confirm),
        )
        show_unknown_key_warning(self, others)

        self.options = Option.parse_all(options)
        self.option_groups = OptionGroup.parse_all(option_groups)
        self.initial_options = Option.parse_all(initial_options)
        self.max_selected_items = max_selected_items

    @JsonValidator(f"options attribute cannot exceed {options_max_length} elements")
    def _validate_options_length(self):
        return self.options is None or len(self.options) <= self.options_max_length

    @JsonValidator(
        f"option_groups attribute cannot exceed {option_groups_max_length} elements"
    )
    def _validate_option_groups_length(self):
        return (
            self.option_groups is None
            or len(self.option_groups) <= self.option_groups_max_length
        )

    @JsonValidator("options and option_groups cannot both be specified")
    def _validate_options_and_option_groups_both_specified(self):
        return self.options is None or self.option_groups is None

    @JsonValidator("options or option_groups must be specified")
    def _validate_neither_options_or_option_groups_is_specified(self):
        return self.options is not None or self.option_groups is not None


# SelectElement will be deprecated in version 3, use StaticSelectElement instead
class SelectElement(InputInteractiveElement):
    type = "static_select"
    options_max_length = 100
    option_groups_max_length = 100

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"options", "option_groups", "initial_option"})

    def __init__(
        self,
        *,
        action_id: Optional[str] = None,
        placeholder: Optional[str] = None,
        options: Optional[List[Option]] = None,
        option_groups: Optional[List[OptionGroup]] = None,
        initial_option: Optional[Option] = None,
        confirm: Optional[Union[dict, ConfirmObject]] = None,
        **others: dict,
    ):
        """This is the simplest form of select menu, with a static list of options passed in when defining the element.
        https://api.slack.com/reference/block-kit/block-elements#static_select
        """
        super().__init__(
            type=self.type,
            action_id=action_id,
            placeholder=TextObject.parse(placeholder, PlainTextObject.type),
            confirm=ConfirmObject.parse(confirm),
        )
        show_unknown_key_warning(self, others)

        self.options = options
        self.option_groups = option_groups
        self.initial_option = initial_option

    @JsonValidator(f"options attribute cannot exceed {options_max_length} elements")
    def _validate_options_length(self):
        return self.options is None or len(self.options) <= self.options_max_length

    @JsonValidator(
        f"option_groups attribute cannot exceed {option_groups_max_length} elements"
    )
    def _validate_option_groups_length(self):
        return (
            self.option_groups is None
            or len(self.option_groups) <= self.option_groups_max_length
        )

    @JsonValidator("options and option_groups cannot both be specified")
    def _validate_options_and_option_groups_both_specified(self):
        return not (self.options is not None and self.option_groups is not None)

    @JsonValidator("options or option_groups must be specified")
    def _validate_neither_options_or_option_groups_is_specified(self):
        return self.options is not None or self.option_groups is not None


# -------------------------------------------------
# External Data Source Select
# -------------------------------------------------


class ExternalDataSelectElement(InputInteractiveElement):
    type = "external_select"

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"min_query_length", "initial_option"})

    def __init__(
        self,
        *,
        action_id: Optional[str] = None,
        placeholder: Union[str, TextObject] = None,
        initial_option: Union[Optional[Option], Optional[OptionGroup]] = None,
        min_query_length: Optional[int] = None,
        confirm: Optional[Union[dict, ConfirmObject]] = None,
        **others: dict,
    ):
        """
        This select menu will load its options from an external data source, allowing
        for a dynamic list of options.
        https://api.slack.com/reference/block-kit/block-elements#external_select
        """
        super().__init__(
            type=self.type,
            action_id=action_id,
            placeholder=TextObject.parse(placeholder, PlainTextObject.type),
            confirm=ConfirmObject.parse(confirm),
        )
        show_unknown_key_warning(self, others)

        self.min_query_length = min_query_length
        self.initial_option = initial_option


class ExternalDataMultiSelectElement(InputInteractiveElement):
    type = "multi_external_select"

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union(
            {"min_query_length", "initial_options", "max_selected_items"}
        )

    def __init__(
        self,
        *,
        placeholder: Optional[Union[str, dict, TextObject]] = None,
        action_id: Optional[str] = None,
        min_query_length: Optional[int] = None,
        initial_options: Optional[List[Union[dict, Option]]] = None,
        confirm: Optional[Union[dict, ConfirmObject]] = None,
        max_selected_items: Optional[int] = None,
        **others: dict,
    ):
        """
        This select menu will load its options from an external data source, allowing
        for a dynamic list of options.
        https://api.slack.com/reference/block-kit/block-elements#external-select
        """
        super().__init__(
            type=self.type,
            action_id=action_id,
            placeholder=TextObject.parse(placeholder, PlainTextObject.type),
            confirm=ConfirmObject.parse(confirm),
        )
        show_unknown_key_warning(self, others)

        self.min_query_length = min_query_length
        self.initial_options = Option.parse_all(initial_options)
        self.max_selected_items = max_selected_items


# -------------------------------------------------
# Users Select
# -------------------------------------------------


class UserSelectElement(InputInteractiveElement):
    type = "users_select"

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"initial_user"})

    def __init__(
        self,
        *,
        placeholder: Optional[Union[str, dict, TextObject]] = None,
        action_id: Optional[str] = None,
        initial_user: Optional[str] = None,
        confirm: Optional[Union[dict, ConfirmObject]] = None,
        **others: dict,
    ):
        """
        This select menu will populate its options with a list of Slack users visible to
        the current user in the active workspace.
        https://api.slack.com/reference/block-kit/block-elements#users_select
        """
        super().__init__(
            type=self.type,
            action_id=action_id,
            placeholder=TextObject.parse(placeholder, PlainTextObject.type),
            confirm=ConfirmObject.parse(confirm),
        )
        show_unknown_key_warning(self, others)

        self.initial_user = initial_user


class UserMultiSelectElement(InputInteractiveElement):
    type = "multi_users_select"

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"initial_users", "max_selected_items"})

    def __init__(
        self,
        *,
        action_id: Optional[str] = None,
        placeholder: Optional[Union[str, dict, TextObject]] = None,
        initial_users: Optional[List[str]] = None,
        confirm: Optional[Union[dict, ConfirmObject]] = None,
        max_selected_items: Optional[int] = None,
        **others: dict,
    ):
        """
        This select menu will populate its options with a list of Slack users visible to
        the current user in the active workspace.
        https://api.slack.com/reference/block-kit/block-elements#users_multi_select
        """
        super().__init__(
            type=self.type,
            action_id=action_id,
            placeholder=TextObject.parse(placeholder, PlainTextObject.type),
            confirm=ConfirmObject.parse(confirm),
        )
        show_unknown_key_warning(self, others)

        self.initial_users = initial_users
        self.max_selected_items = max_selected_items


# -------------------------------------------------
# Conversations Select
# -------------------------------------------------


class ConversationFilter(JsonObject):
    attributes = {"include", "exclude_bot_users"}
    logger = logging.getLogger(__name__)

    def __init__(
        self,
        *,
        include: Optional[List[str]] = None,
        exclude_bot_users: Optional[bool] = None,
    ):
        self.include = include
        self.exclude_bot_users = exclude_bot_users

    @classmethod
    def parse(cls, filter: Union[dict, "ConversationFilter"]):
        if filter is None:
            return None
        elif isinstance(filter, ConversationFilter):
            return filter
        elif isinstance(filter, dict):
            d = copy.copy(filter)
            return ConversationFilter(**d)
        else:
            cls.logger.warning(
                f"Unknown conversation filter object detected and skipped ({filter})"
            )
            return None


class ConversationSelectElement(InputInteractiveElement):
    type = "conversations_select"

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union(
            {
                "initial_conversation",
                "response_url_enabled",
                "filter",
                "default_to_current_conversation",
            }
        )

    def __init__(
        self,
        *,
        placeholder: Optional[Union[str, dict, TextObject]] = None,
        action_id: Optional[str] = None,
        initial_conversation: Optional[str] = None,
        confirm: Optional[Union[dict, ConfirmObject]] = None,
        response_url_enabled: Optional[bool] = None,
        default_to_current_conversation: Optional[bool] = None,
        filter: Optional[ConversationFilter] = None,
        **others: dict,
    ):
        """
        This select menu will populate its options with a list of public and private
        channels, DMs, and MPIMs visible to the current user in the active workspace.
        https://api.slack.com/reference/block-kit/block-elements#conversation_select
        """
        super().__init__(
            type=self.type,
            action_id=action_id,
            placeholder=TextObject.parse(placeholder, PlainTextObject.type),
            confirm=ConfirmObject.parse(confirm),
        )
        show_unknown_key_warning(self, others)

        self.initial_conversation = initial_conversation
        self.response_url_enabled = response_url_enabled
        self.default_to_current_conversation = default_to_current_conversation
        self.filter = filter


class ConversationMultiSelectElement(InputInteractiveElement):
    type = "multi_conversations_select"

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union(
            {
                "initial_conversations",
                "max_selected_items",
                "default_to_current_conversation",
                "filter",
            }
        )

    def __init__(
        self,
        *,
        placeholder: Optional[Union[str, dict, TextObject]] = None,
        action_id: Optional[str] = None,
        initial_conversations: Optional[List[str]] = None,
        confirm: Optional[Union[dict, ConfirmObject]] = None,
        max_selected_items: Optional[int] = None,
        default_to_current_conversation: Optional[bool] = None,
        filter: Optional[Union[dict, ConversationFilter]] = None,
        **others: dict,
    ):
        """
        This multi-select menu will populate its options with a list of public and private channels,
        DMs, and MPIMs visible to the current user in the active workspace.
        https://api.slack.com/reference/block-kit/block-elements#conversation_multi_select
        """
        super().__init__(
            type=self.type,
            action_id=action_id,
            placeholder=TextObject.parse(placeholder, PlainTextObject.type),
            confirm=ConfirmObject.parse(confirm),
        )
        show_unknown_key_warning(self, others)

        self.initial_conversations = initial_conversations
        self.max_selected_items = max_selected_items
        self.default_to_current_conversation = default_to_current_conversation
        self.filter = ConversationFilter.parse(filter)


# -------------------------------------------------
# Channels Select
# -------------------------------------------------


class ChannelSelectElement(InputInteractiveElement):
    type = "channels_select"

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"initial_channel", "response_url_enabled"})

    def __init__(
        self,
        *,
        placeholder: Optional[Union[str, dict, TextObject]] = None,
        action_id: Optional[str] = None,
        initial_channel: Optional[str] = None,
        confirm: Optional[Union[dict, ConfirmObject]] = None,
        response_url_enabled: Optional[bool] = None,
        **others: dict,
    ):
        """
        This select menu will populate its options with a list of public channels
        visible to the current user in the active workspace.
        https://api.slack.com/reference/block-kit/block-elements#channel_select
        """
        super().__init__(
            type=self.type,
            action_id=action_id,
            placeholder=TextObject.parse(placeholder, PlainTextObject.type),
            confirm=ConfirmObject.parse(confirm),
        )
        show_unknown_key_warning(self, others)

        self.initial_channel = initial_channel
        self.response_url_enabled = response_url_enabled


class ChannelMultiSelectElement(InputInteractiveElement):
    type = "multi_channels_select"

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"initial_channels", "max_selected_items"})

    def __init__(
        self,
        *,
        placeholder: Optional[Union[str, dict, TextObject]] = None,
        action_id: Optional[str] = None,
        initial_channels: Optional[List[str]] = None,
        confirm: Optional[Union[dict, ConfirmObject]] = None,
        max_selected_items: Optional[int] = None,
        **others: dict,
    ):
        """
        This multi-select menu will populate its options with a list of public channels visible
        to the current user in the active workspace.
        https://api.slack.com/reference/block-kit/block-elements#channel_multi_select
        """
        super().__init__(
            type=self.type,
            action_id=action_id,
            placeholder=TextObject.parse(placeholder, PlainTextObject.type),
            confirm=ConfirmObject.parse(confirm),
        )
        show_unknown_key_warning(self, others)

        self.initial_channels = initial_channels
        self.max_selected_items = max_selected_items


# -------------------------------------------------
# Input Elements
# -------------------------------------------------


class PlainTextInputElement(InputInteractiveElement):
    type = "plain_text_input"

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union(
            {"initial_value", "multiline", "min_length", "max_length"}
        )

    def __init__(
        self,
        *,
        action_id: Optional[str] = None,
        placeholder: Optional[Union[str, dict, TextObject]] = None,
        confirm: Optional[Union[dict, ConfirmObject]] = None,
        initial_value: Optional[str] = None,
        multiline: Optional[bool] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        **others: dict,
    ):
        """
        An element which lets users easily select a date from a calendar style UI.
        Date picker elements can be used inside of SectionBlocks and ActionsBlocks.
        https://api.slack.com/reference/block-kit/block-elements#datepicker
        """
        super().__init__(
            type=self.type,
            action_id=action_id,
            placeholder=TextObject.parse(placeholder, PlainTextObject.type),
            confirm=ConfirmObject.parse(confirm),
        )
        show_unknown_key_warning(self, others)

        self.initial_value = initial_value
        self.multiline = multiline
        self.min_length = min_length
        self.max_length = max_length


# -------------------------------------------------
# Radio Buttons Select
# -------------------------------------------------


class RadioButtonsElement(InputInteractiveElement):
    type = "radio_buttons"

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"options", "initial_option"})

    def __init__(
        self,
        *,
        action_id: Optional[str] = None,
        placeholder: Optional[Union[str, dict, TextObject]] = None,
        options: Optional[List[Union[dict, Option]]] = None,
        initial_option: Optional[Union[dict, Option]] = None,
        confirm: Optional[Union[dict, ConfirmObject]] = None,
        **others: dict,
    ):
        """A radio button group that allows a user to choose one item from a list of possible options.
        https://api.slack.com/reference/block-kit/block-elements#radio
        """
        super().__init__(
            type=self.type,
            action_id=action_id,
            placeholder=TextObject.parse(placeholder, PlainTextObject.type),
            confirm=ConfirmObject.parse(confirm),
        )
        show_unknown_key_warning(self, others)

        self.options = options
        self.initial_option = initial_option


# -------------------------------------------------
# Overflow Menu Select
# -------------------------------------------------


class OverflowMenuElement(InteractiveElement):
    type = "overflow"
    options_min_length = 2
    options_max_length = 5

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"confirm", "options"})

    def __init__(
        self,
        *,
        action_id: Optional[str] = None,
        options: List[Union[Option]],
        confirm: Optional[Union[dict, ConfirmObject]] = None,
        **others: dict,
    ):
        """
        This is like a cross between a button and a select menu - when a user clicks
        on this overflow button, they will be presented with a list of options to
        choose from. Unlike the select menu, there is no typeahead field, and the
        button always appears with an ellipsis ("…") rather than customisable text.

        As such, it is usually used if you want a more compact layout than a select
        menu, or to supply a list of less visually important actions after a row of
        buttons. You can also specify simple URL links as overflow menu options,
        instead of actions.

        https://api.slack.com/reference/block-kit/block-elements#overflow
        """
        super().__init__(action_id=action_id, type=self.type)
        show_unknown_key_warning(self, others)

        self.options = options  # TODO
        self.confirm = ConfirmObject.parse(confirm)

    @JsonValidator(
        f"options attribute must have between {options_min_length} "
        f"and {options_max_length} items"
    )
    def _validate_options_length(self):
        return self.options_min_length <= len(self.options) <= self.options_max_length


# -------------------------------------------------
# Base Classes
# -------------------------------------------------


class Block(JsonObject):
    """Blocks are a series of components that can be combined
    to create visually rich and compellingly interactive messages.
    https://api.slack.com/reference/block-kit/blocks
    """

    attributes = {"block_id", "type"}
    block_id_max_length = 255
    logger = logging.getLogger(__name__)

    def _subtype_warning(self):
        warnings.warn(
            "subtype is deprecated since slackclient 2.6.0, use type instead",
            DeprecationWarning,
        )

    @property
    def subtype(self) -> Optional[str]:
        return self.type

    def __init__(
        self,
        *,
        type: Optional[str] = None,
        subtype: Optional[str] = None,  # deprecated
        block_id: Optional[str] = None,
    ):
        if subtype:
            self._subtype_warning()
        self.type = type if type else subtype
        self.block_id = block_id
        self.color = None

    @JsonValidator(f"block_id cannot exceed {block_id_max_length} characters")
    def _validate_block_id_length(self):
        return self.block_id is None or len(self.block_id) <= self.block_id_max_length

    @classmethod
    def parse(cls, block: Union[dict, "Block"]) -> Optional["Block"]:
        if block is None:
            return None
        elif isinstance(block, Block):
            return block
        else:
            if "type" in block:
                type = block["type"]
                if type == SectionBlock.type:
                    return SectionBlock(**block)
                elif type == DividerBlock.type:
                    return DividerBlock(**block)
                elif type == ImageBlock.type:
                    return ImageBlock(**block)
                elif type == ActionsBlock.type:
                    return ActionsBlock(**block)
                elif type == ContextBlock.type:
                    return ContextBlock(**block)
                elif type == InputBlock.type:
                    return InputBlock(**block)
                elif type == FileBlock.type:
                    return FileBlock(**block)
                else:
                    cls.logger.warning(f"Unknown block detected and skipped ({block})")
                    return None
            else:
                cls.logger.warning(f"Unknown block detected and skipped ({block})")
                return None

    @classmethod
    def parse_all(cls, blocks: List[Union[dict, "Block"]]) -> List["Block"]:
        return [cls.parse(b) for b in blocks or []]


# -------------------------------------------------
# Block Classes
# -------------------------------------------------


class SectionBlock(Block):
    type = "section"
    fields_max_length = 10
    text_max_length = 3000

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"text", "fields", "accessory"})

    def __init__(
        self,
        *,
        block_id: Optional[str] = None,
        text: Union[str, dict, TextObject] = None,
        fields: List[Union[str, dict, TextObject]] = None,
        accessory: Optional[Union[dict, BlockElement]] = None,
        **others: dict,
    ):
        """A section is one of the most flexible blocks available.
        https://api.slack.com/reference/block-kit/blocks#section
        """
        super().__init__(type=self.type, block_id=block_id)
        show_unknown_key_warning(self, others)

        self.text = TextObject.parse(text)
        field_objects = []
        for f in fields or []:
            if isinstance(f, str):
                field_objects.append(MarkdownTextObject.from_str(f))
            elif isinstance(f, TextObject):
                field_objects.append(f)
            elif isinstance(f, dict) and "type" in f:
                d = copy.copy(f)
                t = d.pop("type")
                if t == MarkdownTextObject.type:
                    field_objects.append(MarkdownTextObject(**d))
                else:
                    field_objects.append(PlainTextObject(**d))
            else:
                self.logger.warning(f"Unsupported filed detected and skipped {f}")
        self.fields = field_objects
        self.accessory = BlockElement.parse(accessory)

    @JsonValidator("text or fields attribute must be specified")
    def _validate_text_or_fields_populated(self):
        return self.text is not None or self.fields

    @JsonValidator(f"fields attribute cannot exceed {fields_max_length} items")
    def _validate_fields_length(self):
        return self.fields is None or len(self.fields) <= self.fields_max_length

    @JsonValidator(f"text attribute cannot exceed {text_max_length} characters")
    def _validate_alt_text_length(self):
        return self.text is None or len(self.text.text) <= self.text_max_length


class DividerBlock(Block):
    type = "divider"

    def __init__(
        self, *, block_id: Optional[str] = None, **others: dict,
    ):
        """A content divider, like an <hr>, to split up different blocks inside of a message.
        https://api.slack.com/reference/block-kit/blocks#divider
        """
        super().__init__(type=self.type, block_id=block_id)
        show_unknown_key_warning(self, others)


class ImageBlock(Block):
    type = "image"

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"alt_text", "image_url", "title"})

    image_url_max_length = 3000
    alt_text_max_length = 2000
    title_max_length = 2000

    def __init__(
        self,
        *,
        image_url: str,
        alt_text: str,
        title: Optional[Union[str, dict, TextObject]] = None,
        block_id: Optional[str] = None,
        **others: dict,
    ):
        """A simple image block, designed to make those cat photos really pop.
        https://api.slack.com/reference/block-kit/blocks#image
        """
        super().__init__(type=self.type, block_id=block_id)
        show_unknown_key_warning(self, others)

        self.image_url = image_url
        self.alt_text = alt_text
        self.title = TextObject.parse(title)

    @JsonValidator(
        f"image_url attribute cannot exceed {image_url_max_length} characters"
    )
    def _validate_image_url_length(self):
        return len(self.image_url) <= self.image_url_max_length

    @JsonValidator(f"alt_text attribute cannot exceed {alt_text_max_length} characters")
    def _validate_alt_text_length(self):
        return len(self.alt_text) <= self.alt_text_max_length

    @JsonValidator(f"title attribute cannot exceed {title_max_length} characters")
    def _validate_title_length(self):
        return (
            self.title is None
            or self.title.text is None
            or len(self.title.text) <= self.title_max_length
        )


class ActionsBlock(Block):
    type = "actions"
    elements_max_length = 5

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"elements"})

    def __init__(
        self,
        *,
        elements: List[Union[dict, InteractiveElement]],
        block_id: Optional[str] = None,
        **others: dict,
    ):
        """A block that is used to hold interactive elements.
        https://api.slack.com/reference/block-kit/blocks#actions
        """
        super().__init__(type=self.type, block_id=block_id)
        show_unknown_key_warning(self, others)

        self.elements = elements

    @JsonValidator(f"elements attribute cannot exceed {elements_max_length} elements")
    def _validate_elements_length(self):
        return self.elements is None or len(self.elements) <= self.elements_max_length


class ContextBlock(Block):
    type = "context"
    elements_max_length = 10

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"elements"})

    def __init__(
        self,
        *,
        elements: List[Union[dict, ImageBlock, TextObject]],
        block_id: Optional[str] = None,
        **others: dict,
    ):
        """Displays message context, which can include both images and text.
        https://api.slack.com/reference/block-kit/blocks#context
        """
        super().__init__(type=self.type, block_id=block_id)
        show_unknown_key_warning(self, others)

        self.elements = BlockElement.parse_all(elements)

    @JsonValidator(f"elements attribute cannot exceed {elements_max_length} elements")
    def _validate_elements_length(self):
        return self.elements is None or len(self.elements) <= self.elements_max_length


class InputBlock(Block):
    type = "input"
    label_max_length = 2000
    hint_max_length = 2000

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"label", "hint", "element", "optional"})

    def __init__(
        self,
        *,
        label: Union[str, dict, PlainTextObject],
        element: Union[str, dict, InputInteractiveElement],
        block_id: Optional[str] = None,
        hint: Optional[Union[str, dict, PlainTextObject]] = None,
        optional: Optional[bool] = None,
        **others: dict,
    ):
        """A block that collects information from users - it can hold a plain-text input element,
        a select menu element, a multi-select menu element, or a datepicker.
        Important Note: Input blocks are only available in modals.
        https://api.slack.com/reference/block-kit/blocks#input
        """
        super().__init__(type=self.type, block_id=block_id)
        show_unknown_key_warning(self, others)

        self.label = TextObject.parse(label, default_type=PlainTextObject.type)
        self.element = BlockElement.parse(element)
        self.hint = TextObject.parse(hint, default_type=PlainTextObject.type)
        self.optional = optional

    @JsonValidator(f"label attribute cannot exceed {label_max_length} characters")
    def _validate_label_length(self):
        return (
            self.label is None
            or self.label.text is None
            or len(self.label.text) <= self.label_max_length
        )

    @JsonValidator(f"hint attribute cannot exceed {hint_max_length} characters")
    def _validate_hint_length(self):
        return (
            self.hint is None
            or self.hint.text is None
            or len(self.hint.text) <= self.label_max_length
        )

    @JsonValidator(
        (
            "element attribute must be a string, select element, multi-select element, "
            "or a datepicker. (Sub-classes of InputInteractiveElement)"
        )
    )
    def _validate_element_type(self):
        return self.element is None or isinstance(
            self.element, (str, InputInteractiveElement)
        )


class FileBlock(Block):
    type = "file"

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"external_id", "source"})

    def __init__(
        self,
        *,
        external_id: str,
        source: str = "remote",
        block_id: Optional[str] = None,
        **others: dict,
    ):
        """Displays a remote file.
        https://api.slack.com/reference/block-kit/blocks#file
        """
        super().__init__(type=self.type, block_id=block_id)
        show_unknown_key_warning(self, others)

        self.external_id = external_id
        self.source = source


class CallBlock(Block):
    type = "call"

    @property
    def attributes(self) -> Set[str]:
        return super().attributes.union({"call_id", "api_decoration_available", "call"})

    def __init__(
        self,
        *,
        call_id: str,
        api_decoration_available: Optional[bool] = None,
        call: Optional[Dict[str, Dict[str, any]]] = None,
        block_id: Optional[str] = None,
        **others: dict,
    ):
        """Displays a call information
        https://api.slack.com/reference/block-kit/blocks#call
        """
        super().__init__(type=self.type, block_id=block_id)
        show_unknown_key_warning(self, others)

        self.call_id = call_id
        self.api_decoration_available = api_decoration_available
        self.call = call
