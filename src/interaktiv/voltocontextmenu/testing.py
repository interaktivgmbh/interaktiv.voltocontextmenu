from plone.app.testing import (
    FunctionalTesting,
    IntegrationTesting,
    PLONE_FIXTURE,
    PloneSandboxLayer,
)
from plone.testing.zope import WSGI_SERVER_FIXTURE


class InteraktivVoltoContextmenuLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configuration_context):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.volto
        self.loadZCML(package=plone.volto)

        # Load plone.restapi meta.zcml first for plone:service directive
        import plone.restapi
        from zope.configuration import xmlconfig
        xmlconfig.file("meta.zcml", plone.restapi, context=configuration_context)
        xmlconfig.file("configure.zcml", plone.restapi, context=configuration_context)

        import interaktiv.voltocontextmenu
        self.loadZCML(package=interaktiv.voltocontextmenu)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'interaktiv.voltocontextmenu:default')


INTERAKTIV_VOLTOCONTEXTMENU_FIXTURE = InteraktivVoltoContextmenuLayer()

INTERAKTIV_VOLTOCONTEXTMENU_INTEGRATION_TESTING = IntegrationTesting(
    bases=(INTERAKTIV_VOLTOCONTEXTMENU_FIXTURE,),
    name='InteraktivVoltoContextmenuLayer:IntegrationTesting',
)

INTERAKTIV_VOLTOCONTEXTMENU_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(INTERAKTIV_VOLTOCONTEXTMENU_FIXTURE, WSGI_SERVER_FIXTURE),
    name='InteraktivVoltoContextmenuLayer:FunctionalTesting',
)
