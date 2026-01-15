from typing import TypedDict, List, Dict

import plone.api as api
from Acquisition import aq_parent, aq_base
from plone.app.contentlisting.catalog import CatalogContentListingObject
from plone.dexterity.content import DexterityContent
from plone.restapi.services import Service


class ContextmenuItemData(TypedDict):
    uid: str
    title: str
    description: str
    portal_type: str
    url: str
    is_active: bool
    children: list


class ContentmenuData(TypedDict):
    items: List[ContextmenuItemData]


class ContextmenuGet(Service):
    """Returns a content menu."""

    def reply(self) -> ContextmenuItemData:
        show_contextmenu = self._show_contextmenu()

        print('### ContextmenuGet', self.context, show_contextmenu) 


        if not show_contextmenu:
            return dict()

        contextmenu = self._get_context_menu()
        return contextmenu

    def _show_contextmenu(self):
        context_base = aq_base(self.context)
        context_show_contextmenu = getattr(context_base, 'show_contextmenu', False)
        if not context_show_contextmenu:
            return False

        return True

    def _get_context_menu(self) -> ContextmenuItemData:
        # TODO handle ROOT objects (?)
        parent = aq_parent(self.context)
        context = self.context

        contextmenu = {
            'items': self._get_context_menu_items(parent, context),
        }

        return contextmenu

    @staticmethod
    def _get_item_data(brain: CatalogContentListingObject) -> ContextmenuItemData:
        data = {
            'uid': brain.UID,
            'id': brain.id,
            'title': brain.Title,
            'description': brain.Description,
            'portal_type': brain.portal_type,
            'url': brain.getURL(),
            'is_active': False,
            'children': []
        }
        return data

    @staticmethod
    def _get_query(query_context: DexterityContent) -> Dict[str, any]:
        query = {
            'sort_on': 'getObjPositionInParent',
            'path': {
                'query': '/'.join(query_context.getPhysicalPath()),
                'depth': 1
            },
            'show_in_contextmenu': True
        }
        return query

    def _get_children(self, context: DexterityContent) -> List[ContextmenuItemData]:
        children = []
        catalog = api.portal.get_tool('portal_catalog')

        query = self._get_query(context)

        for brain in catalog(query):
            children.append(self._get_item_data(brain))

        return children

    def _get_context_menu_items(self, parent: DexterityContent, context: DexterityContent
                                ) -> List[ContextmenuItemData]:
        items = []
        catalog = api.portal.get_tool('portal_catalog')
        context_uid = context.UID()

        query = self._get_query(parent)
        for brain in catalog(query):
            item_data = self._get_item_data(brain)

            if brain.UID == context_uid:
                item_data['is_active'] = True
                item_data['children'] = self._get_children(context)

            items.append(item_data)

        return items
