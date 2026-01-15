import unittest

# noinspection PyUnresolvedReferences
from Products.CMFPlone.utils import get_installer
from interaktiv.voltocontextmenu.behaviors.contextmenu import IContextmenuBehavior
from interaktiv.voltocontextmenu.interfaces import IInteraktivVoltoContextmenuLayer
from interaktiv.voltocontextmenu.testing import INTERAKTIV_VOLTOCONTEXTMENU_INTEGRATION_TESTING
from plone.browserlayer import utils
from plone.dexterity.fti import DexterityFTI
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import getUtility


class TestUninstall(unittest.TestCase):
    layer = INTERAKTIV_VOLTOCONTEXTMENU_INTEGRATION_TESTING
    product_name = 'interaktiv.voltocontextmenu'

    def setUp(self):
        super(TestUninstall, self).setUp()

        self.installer = get_installer(self.layer["portal"], self.layer["request"])

    def test_uninstall_removes_browserlayer(self):
        # do it
        self.installer.uninstall_product(self.product_name)

        # postcondition
        self.assertNotIn(IInteraktivVoltoContextmenuLayer, utils.registered_layers())

    def test_uninstall_unsets_contextmenu_behavior(self):
        # setup
        contextmenu_behavior = IContextmenuBehavior.__identifier__
        portal_types_to_unset = ['Document']

        # do it
        self.installer.uninstall_product(self.product_name)

        # postcondition
        for portal_type in portal_types_to_unset:
            fti: DexterityFTI = getUtility(IDexterityFTI, name=portal_type)

            self.assertNotIn(contextmenu_behavior, fti.behaviors)
