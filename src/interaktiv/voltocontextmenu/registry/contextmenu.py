from interaktiv.voltocontextmenu import _
from zope.interface import Interface
from plone import schema


class IContextmenuSchema(Interface):
    default_portal_types = schema.List(
        title=_('label_default_portal_types', default='Contextmenu Default Portal Types'),
        description=_(
            'help_default_portal_types',
            default='Types that are shown in Contextmenu by Default.'
        ),
        value_type=schema.Choice(source='plone.app.vocabularies.UserFriendlyTypes'),
        default=['Document'],
    )
