from plone.app.registry.browser import controlpanel
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.z3cform import layout
from zope.component import adapter
from zope.interface import Interface

from interaktiv.voltocontextmenu import _
from interaktiv.voltocontextmenu.registry.contextmenu import IContextmenuSchema


class ContextmenuSettingsControlPanelForm(controlpanel.RegistryEditForm):
    schema = IContextmenuSchema
    label = _(
        "trans_label_controlpanel_contextnavigation_settings",
        default="Context navigation",
    )


class ContextmenuSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ContextmenuSettingsControlPanelForm


@adapter(Interface, Interface)
class ContextmenuSettingsConfigletPanel(RegistryConfigletPanel):
    schema = IContextmenuSchema
    schema_prefix = (
        "interaktiv.voltocontextmenu.registry.contextmenu.IContextmenuSchema"
    )
    configlet_id = "contextmenu-settings"
    configlet_category_id = "Products"
    title = "Context navigation"
    group = "Products"


ContextmenuSettingsView = layout.wrap_form(
    ContextmenuSettingsControlPanelForm, ControlPanelFormWrapper
)
