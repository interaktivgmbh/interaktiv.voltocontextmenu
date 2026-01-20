import plone.api as api
from plone.dexterity.fti import DexterityFTI
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import getUtility
from zope.interface.interfaces import ComponentLookupError

from interaktiv.voltocontextmenu import DEFAULT_MENU_TYPES
from interaktiv.voltocontextmenu.behaviors.contextmenu import IContextmenuBehavior


def add_contextmenu_behavior(portal_types: list[str]) -> None:
    contextmenu_behavior = IContextmenuBehavior.__identifier__

    for portal_type in portal_types:
        try:
            fti: DexterityFTI = getUtility(IDexterityFTI, name=portal_type)
        except ComponentLookupError:
            continue

        if contextmenu_behavior not in fti.behaviors:
            behaviors = list(fti.behaviors) + [contextmenu_behavior]
            # noinspection PyProtectedMember
            fti._updateProperty("behaviors", tuple(behaviors))


def remove_contextmenu_behavior() -> None:
    contextmenu_behavior = IContextmenuBehavior.__identifier__

    portal_types_tool = api.portal.get_tool("portal_types")
    portal_types = portal_types_tool.listContentTypes()

    for portal_type in portal_types:
        try:
            fti: DexterityFTI = getUtility(IDexterityFTI, name=portal_type)
        except ComponentLookupError:
            continue

        if contextmenu_behavior in fti.behaviors:
            behaviors = [
                behavior
                for behavior in fti.behaviors
                if behavior != contextmenu_behavior
            ]
            # noinspection PyProtectedMember
            fti._updateProperty("behaviors", tuple(behaviors))


# noinspection PyUnusedLocal
def post_install(context):
    add_contextmenu_behavior(DEFAULT_MENU_TYPES)


# noinspection PyUnusedLocal
def post_uninstall(context):
    remove_contextmenu_behavior()
