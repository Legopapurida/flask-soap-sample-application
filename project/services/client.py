from ..auth.controllers import login_required
from . import site
from . import Client

from flask import request
from flask import render_template
from flask import g

@site.route('/')
@site.route('/home')
@site.route('/index')
@login_required
def index():
    url = request.host_url + '/soap/get_debt?wsdl'
    cl = Client(url)
    debt = cl.service.get_debt(g.user.id)
    if not debt:
        debt = g.user.debt
    return render_template('index.html', debt = debt)
