import pathlib
from chameleon.zpt.loader import TemplateLoader
from knappe.ui import SlotExpr, UI, Layout 

ui = UI(
    templates = TemplateLoader(
        str(pathlib.Path(__file__).parent / "./templates"),
        default_extension=".pt"
    )
)

ui.layout = Layout(ui.templates["layout"])