import colander
import deform
from knappe.meta import HTTPMethodEndpointMeta
from knappe.decorators import html
from knappe_deform import FormPage, trigger

def discord_handle(node, value):
    if type(value) is not str or not re.match(r'([.]+)#([0-9]{4})', value):
        raise colander.Invalid('Value is not a Discord handle')

class ProfileSchema(colander.Schema):
    username = colander.SchemaNode(
        colander.String(),
        title="Pseudo"
    )

    discord = colander.SchemaNode(
        colander.String(),
        title="Handle Discord",
        validator=discord_handle
    )

class Profile(FormPage):

    schema = ProfileSchema

    @trigger('save', title="Sauvegarder")
    def save(self, request):
        form = self.get_form(request)
        appstruct = form.validate(request.data.form)
        return Response.redirect('/profile')


    @html('profile')
    def GET(self, request):
        return {}
    