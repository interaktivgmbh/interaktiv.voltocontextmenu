import unittest

import plone.api as api
from plone.browserlayer import utils
from plone.dexterity.fti import DexterityFTI
from plone.dexterity.interfaces import IDexterityFTI

# noinspection PyUnresolvedReferences
from Products.CMFPlone.utils import get_installer
from zope.component import getUtility
from zope.interface.interfaces import ComponentLookupError

from interaktiv.voltocontextmenu import DEFAULT_CONTEXTMENU_TYPES
from interaktiv.voltocontextmenu.behaviors.contextmenu import IContextmenuBehavior
from interaktiv.voltocontextmenu.interfaces import IInteraktivVoltoContextmenuLayer
from interaktiv.voltocontextmenu.registry.contextmenu import IContextmenuSchema
from interaktiv.voltocontextmenu.testing import (
    INTERAKTIV_VOLTOCONTEXTMENU_INTEGRATION_TESTING,
)


class TestSetup(unittest.TestCase):
    layer = INTERAKTIV_VOLTOCONTEXTMENU_INTEGRATION_TESTING
    product_name = "interaktiv.voltocontextmenu"

    def test_product_installed(self):
        # setup
        installer = get_installer(self.layer["portal"], self.layer["request"])

        # do it
        result = installer.is_product_installed(self.product_name)

        # postcondition
        self.assertTrue(result)

    def test_browserlayer_installed(self):
        # postcondition
        self.assertIn(IInteraktivVoltoContextmenuLayer, utils.registered_layers())

    def test_contextmenu_behavior_set(self):
        # setup
        contextmenu_behavior = IContextmenuBehavior.__identifier__

        # postcondition
        for portal_type in DEFAULT_CONTEXTMENU_TYPES:
            try:
                fti: DexterityFTI = getUtility(IDexterityFTI, name=portal_type)
            except ComponentLookupError:
                continue

            self.assertIn(contextmenu_behavior, fti.behaviors)

    def test_contextmenu_registry_record_created(self):
        default_shown_types = api.portal.get_registry_record(
            name="default_portal_types", interface=IContextmenuSchema
        )

        expected_types = ["Document"]
        self.assertListEqual(default_shown_types, expected_types)
