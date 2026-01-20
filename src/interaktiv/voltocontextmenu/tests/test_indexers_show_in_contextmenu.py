import unittest

import plone.api as api
from plone.app.testing import TEST_USER_ID, setRoles

from interaktiv.voltocontextmenu.indexers.show_in_contextmenu import (
    ShowInContextmenuIndexer,
)
from interaktiv.voltocontextmenu.registry.contextmenu import IContextmenuSchema
from interaktiv.voltocontextmenu.setuphandlers import add_contextmenu_behavior
from interaktiv.voltocontextmenu.testing import (
    INTERAKTIV_VOLTOCONTEXTMENU_FUNCTIONAL_TESTING,
)


class TestShowInContextmenuIndexer(unittest.TestCase):
    layer = INTERAKTIV_VOLTOCONTEXTMENU_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager", "Site Administrator"])

    def test_indexer_show_in_contextmenu__default(self):
        # setup
        document_a = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
        )
        indexer = ShowInContextmenuIndexer(document_a)

        # do it
        result = indexer.callable(document_a)

        # postcondition
        self.assertEqual(result, True)

    def test_indexer_show_in_contextmenu__default__not_in_contextmenu(self):
        # setup
        document_a = api.content.create(
            container=self.portal,
            type="Document",
            id="document_a",
            title="Document A",
            description="a Document",
            show_in_contextmenu=False,
        )
        indexer = ShowInContextmenuIndexer(document_a)

        # do it
        result = indexer.callable(document_a)

        # postcondition
        self.assertEqual(result, False)

    def test_indexer_show_in_contextmenu__not_default(self):
        # setup
        add_contextmenu_behavior(["Image"])

        image_a = api.content.create(
            container=self.portal,
            type="Image",
            id="image_a",
            title="Image A",
            description="an Image",
        )
        indexer = ShowInContextmenuIndexer(image_a)

        # do it
        result = indexer.callable(image_a)

        # postcondition
        self.assertEqual(result, False)

    def test_indexer_show_in_contextmenu__not_default__in_contextmenu(self):
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
        indexer = ShowInContextmenuIndexer(image_a)

        # do it
        result = indexer.callable(image_a)

        # postcondition
        self.assertEqual(result, True)

    def test_indexer_show_in_contextmenu__default__registry_update(self):
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
        indexer = ShowInContextmenuIndexer(image_a)

        # do it
        result = indexer.callable(image_a)

        # postcondition
        self.assertEqual(result, True)
