from plone import schema
from zope.interface import Interface

from interaktiv.voltocontextmenu import _


class IContextmenuSchema(Interface):
    default_portal_types = schema.List(
        title=_(
            "label_default_portal_types", default="Content types in context navigation"
        ),
        description=_(
            "help_default_portal_types",
            default="Content of these types appears in the context navigation automatically. "
            'This can be changed per item with "Show in context navigation".',
        ),
        value_type=schema.Choice(source="plone.app.vocabularies.UserFriendlyTypes"),
        default=["Document"],
    )
