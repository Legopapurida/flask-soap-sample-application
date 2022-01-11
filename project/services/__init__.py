from flask import Blueprint
from zeep.client import Client

site = Blueprint('site', __name__, url_prefix='/')

from . import client