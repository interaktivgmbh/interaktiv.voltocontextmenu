import unittest

import plone.api as api
from plone.app.testing import TEST_USER_ID, setRoles

from interaktiv.voltocontextmenu.behaviors.contextmenu import ContextmenuBehavior
from interaktiv.voltocontextmenu.registry.contextmenu import IContextmenuSchema
from interaktiv.voltocontextmenu.setuphandlers import add_contextmenu_behavior
from interaktiv.voltocontextmenu.testing import (
    INTERAKTIV_VOLTOCONTEXTMENU_FUNCTIONAL_TESTING,
)


class TestContextmenuBehavior(unittest.TestCase):
    layer = INTERAKTIV_VOLTOCONTEXTMENU_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager", "Site Administrator"])

    def test_show_in_contextmenu__none__default_type(self):
        # setup
        document_a = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
        )
        behavior = ContextmenuBehavior(document_a)

        # do it
        result = behavior.show_in_contextmenu

        # postcondition
        self.assertIsNotNone(result)
        self.assertEqual(result, True)

    def test_show_in_contextmenu__none__not_default_type(self):
        # setup
        add_contextmenu_behavior(["Image"])

        image_a = api.content.create(
            container=self.portal,
            type="Image",
            id="image_a",
            title="Image A",
            description="an Image",
        )
        behavior = ContextmenuBehavior(image_a)

        # do it
        result = behavior.show_in_contextmenu

        # postcondition
        self.assertIsNotNone(result)
        self.assertEqual(result, False)

    def test_show_in_contextmenu__explicit_true(self):
        # setup
        add_contextmenu_behavior(["Image"])

        image_a = api.content.create(
            container=self.portal,
            type="Image",
            id="image_a",
            title="Image A",
            description="an Image",
            show_in_contextmenu=True,
        )
        behavior = ContextmenuBehavior(image_a)

        # do it
        result = behavior.show_in_contextmenu

        # postcondition
        self.assertEqual(result, True)

    def test_show_in_contextmenu__explicit_false(self):
        # setup
        document_a = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
            show_in_contextmenu=False,
        )
        behavior = ContextmenuBehavior(document_a)

        # do it
        result = behavior.show_in_contextmenu

        # postcondition
        self.assertEqual(result, False)

    def test_show_in_contextmenu__none__registry_update(self):
        # setup
        add_contextmenu_behavior(["Image"])

        api.portal.set_registry_record(
            name="default_portal_types",
            interface=IContextmenuSchema,
            value=["Document", "Image"],
        )

        image_a = api.content.create(
            container=self.portal,
            type="Image",
            id="image_a",
            title="Image A",
            description="an Image",
        )
        behavior = ContextmenuBehavior(image_a)

        # do it
        result = behavior.show_in_contextmenu

        # postcondition
        self.assertEqual(result, True)

    def test_show_in_contextmenu__setter(self):
        # setup
        document_a = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
        )
        behavior = ContextmenuBehavior(document_a)

        # do it
        behavior.show_in_contextmenu = False

        # postcondition
        self.assertEqual(behavior.show_in_contextmenu, False)
        self.assertEqual(document_a.show_in_contextmenu, False)

    def test_show_contextmenu__delegates_to_context(self):
        # setup
        document_a = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
            show_contextmenu=False,
        )
        behavior = ContextmenuBehavior(document_a)

        # do it
        result = behavior.show_contextmenu

        # postcondition
        self.assertEqual(result, False)

    def test_show_contextmenu__delegates_to_context__default(self):
        # setup
        document_a = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
        )
        behavior = ContextmenuBehavior(document_a)

        # do it
        result = behavior.show_contextmenu

        # postcondition
        self.assertEqual(result, True)
