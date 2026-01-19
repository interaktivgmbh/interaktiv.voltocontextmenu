import unittest

import plone.api as api
from plone.app.testing import TEST_USER_ID, setRoles
from plone.app.uuid.utils import uuidToCatalogBrain
from plone.dexterity.fti import DexterityFTI
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import getUtility

from interaktiv.voltocontextmenu.behaviors.contextmenu import IContextmenuBehavior
from interaktiv.voltocontextmenu.services.contextmenu.get import ContextmenuGet
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
