from flask import Flask, request
from flask_migrate import Migrate
from .config import Config
from logging import getLogger
from logging.config import fileConfig
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import configure_mappers
from .extensions import db, admin
from .models import *
from .index import index

#Get logging configuration
fileConfig("logging.config")
logger=getLogger(__name__)

def create_app():
    app = Flask(__name__)
    #Configuration from object, file config.py
    app.config.from_object(Config)

    #Initialize db
    db.init_app(app)
    app.register_blueprint(index, url_prefix='/')
    admin.name='IPAM Requests'
    admin.init_app(app)
    configure_mappers()
    admin.add_view(MGMTModelView(Management,db.session,category="Aanvragen"))
    admin.add_view(RealModelView(Real,db.session,category="Aanvragen"))
    admin.add_view(HostModelView(Host,db.session,category="Aanvragen"))
    admin.add_view(IegisidModelView(Iegisid,db.session,category="Tabellen"))
    admin.add_view(TenantsModelView(Tenants,db.session,category="Tabellen"))
    migrate=Migrate(app, db)
    logger.debug("Application started")
    return app

def init_db():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.app_context().push()
    db.create_all()