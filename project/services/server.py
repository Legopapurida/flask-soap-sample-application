from spyne import Iterable, rpc, Application, Service, Integer
from spyne.model import fault
from spyne.protocol.http import HttpRpc
from spyne.protocol.soap import Soap11
from spyne.protocol.soap import Soap11
from spyne.error import InternalError
from flask import Flask

from ..auth.models import User
from .. import get_db

class UnauthenticatedError(fault.Fault):
    __type_name__ = 'Exception'
    __namespace__ = 'spyne.services.finance'

    def __init__(self):
        fault.Fault.__init__(self,
                faultcode='Client.UnauthenticatedError',
                faultstring="user is not authenticated"
            )

class FininceService(Service):

    @rpc(Integer, _returns=Integer)
    def get_debt(
            ctx: Flask, 
            user_id: Integer
        ): 
        try:
            with ctx.udc.app.app_context():
                cursor = get_db().connection.cursor()
                check_user = User(**cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone())
                if check_user:
                    return int(check_user.debt)
            raise UnauthenticatedError()
        except InternalError as err:
            raise InternalError(err)


class UserDefinedContext(object):
    def __init__(self, app: Flask):
        self.config = app.config
        self.app = app


def create_soap(flask_app) -> Application:
    """Creates SOAP services application and distribute Flask config into
    user con defined context for each method call.
    """
    application = Application(
        [FininceService], 'spyne.services.finance',
        # The input protocol is set as HttpRpc to make our service easy to call.
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11(),
    )

    # Use `method_call` hook to pass flask config to each service method
    # context. But if you have any better ideas do it, make a pull request.
    # NOTE. I refuse idea to wrap each call into Flask application context
    # because in fact we inside Spyne app context, not the Flask one.
    def _flask_config_context(ctx):
        ctx.udc = UserDefinedContext(flask_app)
    application.event_manager.add_listener('method_call', _flask_config_context)

    return application