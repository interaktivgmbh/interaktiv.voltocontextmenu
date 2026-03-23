from plone.dexterity.content import DexterityContent
from plone.indexer.decorator import indexer

from interaktiv.voltocontextmenu.behaviors.contextmenu import (
    IContextmenuBehavior,
    IContextmenuBehaviorMarker,
)


@indexer(IContextmenuBehaviorMarker)
def ShowInContextmenuIndexer(obj: DexterityContent) -> bool:
    return IContextmenuBehavior(obj).show_in_contextmenu
