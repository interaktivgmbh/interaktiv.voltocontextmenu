from interaktiv.voltocontextmenu import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapts
from zope.interface import provider, implementer


@provider(IFormFieldProvider)
class IContextmenuBehavior(model.Schema):
    model.fieldset(
        'contextmenu',
        label=_('label_contextmenu_fieldset', default='Contextmenu'),
        fields=('show_contextmenu', 'show_in_contextmenu'),
    )

    show_contextmenu = schema.Bool(
        title=_('label_show_contextmenu', default='Show Contextmenu'),
        description=_(
            'help_show_contextmenu',
            default='If selected, the Contextmenu will be rendered for this page',
        ),
        default=True,
        required=False,
    )

    show_in_contextmenu = schema.Bool(
        title=_('label_show_in_contextmenu', default='Show In Contextmenu'),
        description=_(
            'help_show_in_contextmenu',
            default='If selected, the item will be listed in Contextmenus',
        ),
        required=False,
    )


@implementer(IContextmenuBehavior)
class ContextmenuBehavior(object):
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context
