from typing import Any

import plone.api as api
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapts
from zope.interface import implementer, provider

from interaktiv.voltocontextmenu import _
from interaktiv.voltocontextmenu.registry.contextmenu import IContextmenuSchema


class IContextmenuBehaviorMarker(IDexterityContent):
    """Marker interface for content types with the contextmenu behavior."""


@provider(IFormFieldProvider)
class IContextmenuBehavior(model.Schema):
    model.fieldset(
        "contextmenu",
        label=_("label_contextmenu_fieldset", default="Contextmenu"),
        fields=("show_contextmenu", "show_in_contextmenu"),
    )

    show_contextmenu = schema.Bool(
        title=_("label_show_contextmenu", default="Show Contextmenu"),
        description=_(
            "help_show_contextmenu",
            default="If selected, the Contextmenu will be rendered for this page",
        ),
        default=True,
        required=False,
    )

    show_in_contextmenu = schema.Bool(
        title=_("label_show_in_contextmenu", default="Show In Contextmenu"),
        description=_(
            "help_show_in_contextmenu",
            default="If selected, the item will be listed in Contextmenus",
        ),
        required=False,
    )


@implementer(IContextmenuBehavior)
class ContextmenuBehavior:
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    def __getattr__(self, name: str) -> Any:
        if name in ("context",):
            raise AttributeError(name)
        return getattr(self.context, name)

    @property
    def show_in_contextmenu(self) -> bool:
        raw = getattr(self.context, "show_in_contextmenu", None)
        if raw is not None:
            return raw
        default_shown_types = api.portal.get_registry_record(
            name="default_portal_types",
            interface=IContextmenuSchema,
            default=["Document"],
        )
        return self.context.portal_type in default_shown_types

    @show_in_contextmenu.setter
    def show_in_contextmenu(self, value: bool) -> None:
        self.context.show_in_contextmenu = value
