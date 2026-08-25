import unittest
from datetime import datetime, timedelta

import plone.api as api
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, login, logout, setRoles
from plone.app.uuid.utils import uuidToCatalogBrain
from plone.dexterity.fti import DexterityFTI
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFCore.permissions import AccessInactivePortalContent
from zope.component import getUtility

from interaktiv.voltocontextmenu.behaviors.contextmenu import IContextmenuBehavior
from interaktiv.voltocontextmenu.services.contextmenu.get import ContextmenuGet
from interaktiv.voltocontextmenu.setuphandlers import add_contextmenu_behavior
from interaktiv.voltocontextmenu.testing import (
    INTERAKTIV_VOLTOCONTEXTMENU_FUNCTIONAL_TESTING,
)


class TestContextmenuGet(unittest.TestCase):
    layer = INTERAKTIV_VOLTOCONTEXTMENU_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager", "Site Administrator"])

        self.service = ContextmenuGet()

        contextmenu_behavior = IContextmenuBehavior.__identifier__
        fti: DexterityFTI = getUtility(IDexterityFTI, name="Document")

        if contextmenu_behavior not in fti.behaviors:
            behaviors = list(fti.behaviors)
            behaviors.append(contextmenu_behavior)

            # noinspection PyProtectedMember
            fti._updateProperty("behaviors", tuple(behaviors))

    def test_contextmenu__show_context_menu(self):
        # setup
        document = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
        )
        self.service.context = document

        # do it
        result = self.service._show_contextmenu()

        # postcondition
        self.assertTrue(result)

    def test_contextmenu__show_context_menu__false(self):
        # setup
        document = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
            show_contextmenu=False,
        )
        self.service.context = document

        # do it
        result = self.service._show_contextmenu()

        # postcondition
        self.assertFalse(result)

    def test_contextmenu__show_context_menu__navroot__false(self):
        # setup
        self.service.context = self.portal

        # do it
        result = self.service._show_contextmenu()

        # postcondition
        self.assertFalse(result)

    def test_contextmenu__get_item_data(self):
        # setup
        document = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
        )
        brain = uuidToCatalogBrain(document.UID())

        # do it
        result = self.service._get_item_data(brain)

        # postcondition
        expected_result = {
            "uid": document.UID(),
            "portal_type": "Document",
            "id": "document_a",
            "title": "Document A",
            "description": "a Document",
            "url": document.absolute_url(),
            "is_active": False,
            "children": [],
        }
        self.assertDictEqual(result, expected_result)

    def test_contextmenu__get_query(self):
        # setup
        document = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
        )

        # do it
        result = self.service._get_query(document)

        # postcondition
        expected_result = {
            "sort_on": "getObjPositionInParent",
            "path": {"query": "/".join(document.getPhysicalPath()), "depth": 1},
            "show_in_contextmenu": True,
        }
        self.assertDictEqual(result, expected_result)

    def test_contextmenu__get_children(self):
        # setup
        document = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
        )
        sub_document = api.content.create(
            container=document,
            type="Document",
            id="sub_document_a",
            title="Sub Document A",
            description="a Sub Document",
        )
        api.content.create(
            container=sub_document,
            type="Document",
            id="sub_sub_document_a",
            title="Sub Sub Document A",
            description="a Sub Sub Document",
        )

        # do it
        result = self.service._get_children(document)

        # postcondition
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

        expected_data = {
            "uid": sub_document.UID(),
            "portal_type": "Document",
            "id": "sub_document_a",
            "title": "Sub Document A",
            "description": "a Sub Document",
            "url": sub_document.absolute_url(),
            "is_active": False,
            "children": [],
        }
        self.assertDictEqual(result[0], expected_data)

    def test_contextmenu__get_children__do_not_show_in_contextmenu(self):
        # setup
        document = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
        )
        api.content.create(
            container=document,
            type="Image",
            id="image_a",
            title="Image A",
            description="an Image",
        )

        # do it
        result = self.service._get_children(document)

        # postcondition
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_contextmenu__get_children__show_in_contextmenu(self):
        # setup
        document = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
        )
        image = api.content.create(
            container=document,
            type="Image",
            id="image_a",
            title="Image A",
            description="an Image",
            show_in_contextmenu=True,
        )

        # do it
        result = self.service._get_children(document)

        # postcondition
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

        expected_data = {
            "uid": image.UID(),
            "portal_type": "Image",
            "id": "image_a",
            "title": "Image A",
            "description": "an Image",
            "url": image.absolute_url(),
            "is_active": False,
            "children": [],
        }
        self.assertDictEqual(result[0], expected_data)

    def test_contextmenu__insert_active_context(self):
        # setup
        document_a = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
        )
        image = api.content.create(
            container=self.portal,
            type="Image",
            id="image_a",
            title="Image A",
            description="an Image",
        )

        items = [
            {"id": document_a.id},
            {"id": "someotherid"},
        ]

        # do it
        result = self.service._insert_active_context(
            items=items,
            parent=self.portal,
            context=image,
        )

        # postcondition
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)

        self.assertEqual(result[0]["id"], "document_a")
        self.assertEqual(result[1]["id"], "image_a")
        self.assertEqual(result[2]["id"], "someotherid")

        expected_data = {
            "uid": image.UID(),
            "portal_type": "Image",
            "id": "image_a",
            "title": "Image A",
            "description": "an Image",
            "url": image.absolute_url(),
            "is_active": True,
            "children": [],
        }
        self.assertDictEqual(result[1], expected_data)

    def test_contextmenu__insert_active_context__not_in_parent(self):
        # setup
        document_a = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
        )
        image = api.content.create(
            container=document_a,
            type="Image",
            id="image_a",
            title="Image A",
            description="an Image",
        )

        items = [
            {"id": document_a.id},
            {"id": "someotherid"},
        ]

        # do it
        result = self.service._insert_active_context(
            items=items,
            parent=self.portal,
            context=image,
        )

        # postcondition
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

        self.assertEqual(result[0]["id"], "document_a")
        self.assertEqual(result[1]["id"], "someotherid")

    def test_contextmenu__get_context_menu_items(self):
        # setup
        document_a = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
        )
        sub_document_a = api.content.create(
            container=document_a,
            type="Document",
            id="sub_document_a",
            title="Sub Document A",
            description="a Sub Document",
        )
        document_b = api.content.create(
            container=self.portal,
            type="Document",
            id="document_b",
            title="Document B",
            description="a Document",
        )
        api.content.create(
            container=document_b,
            type="Document",
            id="sub_document_b",
            title="Sub Document B",
            description="a Sub Document",
        )

        # do it
        result = self.service._get_context_menu_items(self.portal, document_a)

        # postcondition
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

        expected_data_a = {
            "uid": document_a.UID(),
            "portal_type": "Document",
            "id": "document_a",
            "title": "Document A",
            "description": "a Document",
            "url": document_a.absolute_url(),
            "is_active": True,
            "children": [
                {
                    "uid": sub_document_a.UID(),
                    "portal_type": "Document",
                    "id": "sub_document_a",
                    "title": "Sub Document A",
                    "description": "a Sub Document",
                    "url": sub_document_a.absolute_url(),
                    "is_active": False,
                    "children": [],
                }
            ],
        }
        self.assertDictEqual(result[0], expected_data_a)

        expected_data_b = {
            "uid": document_b.UID(),
            "portal_type": "Document",
            "id": "document_b",
            "title": "Document B",
            "description": "a Document",
            "url": document_b.absolute_url(),
            "is_active": False,
            "children": [],
        }
        self.assertDictEqual(result[1], expected_data_b)

    def test_contextmenu__get_context_menu_items__do_not_show_in_contextmenu(self):
        # setup
        document_a = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
        )
        api.content.create(
            container=self.portal,
            type="Image",
            id="image_a",
            title="Image A",
            description="an Image",
        )

        # do it
        result = self.service._get_context_menu_items(self.portal, document_a)

        # postcondition
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

        expected_data_a = {
            "uid": document_a.UID(),
            "portal_type": "Document",
            "id": "document_a",
            "title": "Document A",
            "description": "a Document",
            "url": document_a.absolute_url(),
            "is_active": True,
            "children": [],
        }
        self.assertDictEqual(result[0], expected_data_a)

    def test_contextmenu__get_context_menu_items__show_in_contextmenu(self):
        # setup
        document_a = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
        )
        image = api.content.create(
            container=self.portal,
            type="Image",
            id="image_a",
            title="Image A",
            description="an Image",
            show_in_contextmenu=True,
        )

        # do it
        result = self.service._get_context_menu_items(self.portal, document_a)

        # postcondition
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

        expected_data_a = {
            "uid": document_a.UID(),
            "portal_type": "Document",
            "id": "document_a",
            "title": "Document A",
            "description": "a Document",
            "url": document_a.absolute_url(),
            "is_active": True,
            "children": [],
        }
        self.assertDictEqual(result[0], expected_data_a)

        expected_data_b = {
            "uid": image.UID(),
            "portal_type": "Image",
            "id": "image_a",
            "title": "Image A",
            "description": "an Image",
            "url": image.absolute_url(),
            "is_active": False,
            "children": [],
        }
        self.assertDictEqual(result[1], expected_data_b)

    def test_contextmenu__get_context_menu_items__do_not_show_but_context(self):
        # setup
        add_contextmenu_behavior(["Image"])

        document_a = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
        )
        image = api.content.create(
            container=self.portal,
            type="Image",
            id="image_a",
            title="Image A",
            description="an Image",
        )

        # do it
        result = self.service._get_context_menu_items(self.portal, image)

        # postcondition
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

        expected_data_a = {
            "uid": document_a.UID(),
            "portal_type": "Document",
            "id": "document_a",
            "title": "Document A",
            "description": "a Document",
            "url": document_a.absolute_url(),
            "is_active": False,
            "children": [],
        }
        self.assertDictEqual(result[0], expected_data_a)

        expected_data_b = {
            "uid": image.UID(),
            "portal_type": "Image",
            "id": "image_a",
            "title": "Image A",
            "description": "an Image",
            "url": image.absolute_url(),
            "is_active": True,
            "children": [],
        }
        self.assertDictEqual(result[1], expected_data_b)

    def test_contextmenu__get_context_menu(self):
        # setup
        document_a = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
        )
        sub_document_a = api.content.create(
            container=document_a,
            type="Document",
            id="sub_document_a",
            title="Sub Document A",
            description="a Sub Document",
        )
        document_b = api.content.create(
            container=self.portal,
            type="Document",
            id="document_b",
            title="Document B",
            description="a Document",
        )
        api.content.create(
            container=document_b,
            type="Document",
            id="sub_document_b",
            title="Sub Document B",
            description="a Sub Document",
        )
        self.service.context = document_a

        # do it
        result = self.service._get_context_menu()

        # postcondition
        self.assertIsInstance(result, dict)
        self.assertIn("items", result)

        contextmenu_items = result["items"]
        self.assertEqual(len(contextmenu_items), 2)

        expected_data_a = {
            "uid": document_a.UID(),
            "portal_type": "Document",
            "id": "document_a",
            "title": "Document A",
            "description": "a Document",
            "url": document_a.absolute_url(),
            "is_active": True,
            "children": [
                {
                    "uid": sub_document_a.UID(),
                    "portal_type": "Document",
                    "id": "sub_document_a",
                    "title": "Sub Document A",
                    "description": "a Sub Document",
                    "url": sub_document_a.absolute_url(),
                    "is_active": False,
                    "children": [],
                }
            ],
        }
        self.assertDictEqual(contextmenu_items[0], expected_data_a)

        expected_data_b = {
            "uid": document_b.UID(),
            "portal_type": "Document",
            "id": "document_b",
            "title": "Document B",
            "description": "a Document",
            "url": document_b.absolute_url(),
            "is_active": False,
            "children": [],
        }
        self.assertDictEqual(contextmenu_items[1], expected_data_b)

    # --------- expired items ---------

    def _create_expired_sibling_setup(self):
        parent = api.content.create(
            container=self.portal,
            type="Document",
            id="parent",
            show_contextmenu=True,
            show_in_contextmenu=True,
        )
        active = api.content.create(
            container=parent,
            type="Document",
            id="active",
            show_contextmenu=True,
            show_in_contextmenu=True,
        )
        expired = api.content.create(
            container=parent,
            type="Document",
            id="expired",
            show_contextmenu=True,
            show_in_contextmenu=True,
        )
        expired.setExpirationDate(datetime.now() - timedelta(days=1))
        expired.reindexObject()
        return parent, active

    def _contextmenu_ids_as(self, username, context):
        logout()
        login(self.portal, username)
        try:
            service = ContextmenuGet()
            service.context = context
            service.request = self.request
            return sorted(item["id"] for item in service.reply()["items"])
        finally:
            logout()
            login(self.portal, TEST_USER_NAME)

    def test_contextmenu__expired_sibling__hidden_without_inactive_permission(self):
        # setup: a reader without "Access inactive portal content"
        parent, active = self._create_expired_sibling_setup()
        api.user.create(
            email="reader@example.com", username="reader", password="secret123!"
        )
        api.user.grant_roles(username="reader", roles=["Reader"], obj=parent)

        # do it
        result = self._contextmenu_ids_as("reader", active)

        # postcondition: the catalog's default handling of inactive content applies
        self.assertEqual(result, ["active"])

    def test_contextmenu__expired_sibling__local_role_with_inactive_permission(self):
        # setup: permission granted to a role that the user only holds locally on the
        # parent. The catalog's path-based permission check only sees the path when the
        # query is passed as keyword arguments — this guards the call style.
        parent, active = self._create_expired_sibling_setup()
        self.portal.manage_permission(
            AccessInactivePortalContent,
            roles=["Manager", "Site Administrator", "Owner", "Editor"],
            acquire=True,
        )
        api.user.create(
            email="editor@example.com", username="local_editor", password="secret123!"
        )
        api.user.grant_roles(username="local_editor", roles=["Editor"], obj=parent)

        # do it
        result = self._contextmenu_ids_as("local_editor", active)

        # postcondition
        self.assertEqual(result, ["active", "expired"])
