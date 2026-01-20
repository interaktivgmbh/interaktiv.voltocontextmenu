from typing import Any, TypedDict

import plone.api as api
from Acquisition import aq_base, aq_parent
from plone.app.contentlisting.catalog import CatalogContentListingObject
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.dexterity.content import DexterityContent
from plone.restapi.services import Service


class ContextmenuItemData(TypedDict):
    uid: str
    id: str
    title: str
    description: str
    portal_type: str
    url: str
    is_active: bool
    children: list["ContextmenuItemData"]


class ContentmenuData(TypedDict):
    items: list[ContextmenuItemData]


class ContextmenuGet(Service):
    """Returns a content menu."""

    def reply(self) -> ContentmenuData | dict:
        show_contextmenu = self._show_contextmenu()
        if not show_contextmenu:
            return {}

        contextmenu = self._get_context_menu()
        return contextmenu

    def _show_contextmenu(self) -> bool:
        if INavigationRoot.providedBy(self.context):
            return False

        context_base = aq_base(self.context)
        context_show_contextmenu = getattr(context_base, "show_contextmenu", False)
        if not context_show_contextmenu:
            return False

        return True

    def _get_context_menu(self) -> ContentmenuData:
        parent = aq_parent(self.context)
        context = self.context

        contextmenu = {
            "items": self._get_context_menu_items(parent, context),
        }

        return contextmenu

    @staticmethod
    def _get_item_data(brain: CatalogContentListingObject) -> ContextmenuItemData:
        data = {
            "uid": brain.UID,
            "id": brain.id,
            "title": brain.Title,
            "description": brain.Description,
            "portal_type": brain.portal_type,
            "url": brain.getURL(),
            "is_active": False,
            "children": [],
        }
        return data

    @staticmethod
    def _get_query(query_context: DexterityContent) -> dict[str, Any]:
        query = {
            "sort_on": "getObjPositionInParent",
            "path": {"query": "/".join(query_context.getPhysicalPath()), "depth": 1},
            "show_in_contextmenu": True,
        }
        return query

    def _get_children(self, context: DexterityContent) -> list[ContextmenuItemData]:
        children = []
        catalog = api.portal.get_tool("portal_catalog")

        query = self._get_query(context)

        for brain in catalog(query):
            children.append(self._get_item_data(brain))

        return children

    def _get_context_menu_items(
        self, parent: DexterityContent, context: DexterityContent
    ) -> list[ContextmenuItemData]:
        items = []
        catalog = api.portal.get_tool("portal_catalog")
        context_uid = context.UID()
        context_found = False

        query = self._get_query(parent)
        for brain in catalog(query):
            item_data = self._get_item_data(brain)

            if brain.UID == context_uid:
                item_data["is_active"] = True
                item_data["children"] = self._get_children(context)
                context_found = True

            items.append(item_data)

        if not context_found:
            items = self._insert_active_context(items, parent, context)

        return items

    def _insert_active_context(
        self,
        items: list[ContextmenuItemData],
        parent: DexterityContent,
        context: DexterityContent,
    ) -> list[ContextmenuItemData]:

        parent_ids = parent.objectIds()
        if context.id not in parent_ids:
            return items

        context_position = parent.getObjectPosition(context.getId())
        ids_before = parent_ids[:context_position]

        items_before = [item for item in items if item["id"] in ids_before]
        items_after = [item for item in items if item["id"] not in ids_before]

        active_item: ContextmenuItemData = {
            "uid": context.UID(),
            "id": context.getId(),
            "title": context.Title(),
            "description": context.Description(),
            "portal_type": context.portal_type,
            "url": context.absolute_url(),
            "is_active": True,
            "children": self._get_children(context),
        }

        return items_before + [active_item] + items_after
