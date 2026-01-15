import plone.api as api
from interaktiv.voltocontextmenu.behaviors.contextmenu import IContextmenuBehavior
from interaktiv.voltocontextmenu.registry.contextmenu import IContextmenuSchema
from plone.dexterity.content import DexterityContent
from plone.indexer.decorator import indexer


@indexer(IContextmenuBehavior)
def ShowInContextmenuIndexer(obj: DexterityContent) -> bool:
    default_shown_types = api.portal.get_registry_record(
        name='default_portal_types',
        interface=IContextmenuSchema,
        default=['Document']
    )

    if obj.show_in_contextmenu:
        return True

    if obj.show_in_contextmenu is None:
        if obj.portal_type in default_shown_types:
            return True

    return False
