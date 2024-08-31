from .extensions import db
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from .config import Config
from wtforms.validators import DataRequired, Regexp

class Iegisid(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    description = db.Column(db.Text)
    mgmts=db.relationship('Management', backref='iegisid')
    reals=db.relationship('Real', backref='iegisid')

    def __repr__(self):
        return self.name 

class Tenants(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    description = db.Column(db.Text)
    reals=db.relationship('Real', backref='tenant')

    def __repr__(self):
        return self.name

class Management(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    vlan=db.Column(db.Integer)
    DMZ = db.Column(db.String(40), nullable=False)
    datacenter = db.Column(db.String(40), nullable=False)
    iegisid_id= db.Column(db.Integer,db.ForeignKey('iegisid.id'), nullable=False)
    vlanname = db.Column(db.String(40), unique=True, nullable=False)
    vlandescription=db.Column(db.Text, nullable=False)
    cidr= db.Column(db.Integer, nullable=False)
    user=db.Column(db.String(40), nullable=False)
    network=db.Column(db.String(50))
    errors = db.Column(db.Text)

class Real(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    vlan=db.Column(db.Integer)
    DMZ = db.Column(db.String(40), nullable=False)
    datacenter = db.Column(db.String(40), nullable=False)
    tenant_id= db.Column(db.Integer,db.ForeignKey('tenants.id'), nullable=False)
    iegisid_id= db.Column(db.Integer,db.ForeignKey('iegisid.id'), nullable=False)
    vlanname = db.Column(db.String(40), unique=True, nullable=False)
    vlandescription=db.Column(db.Text, nullable=False)
    cidr= db.Column(db.Integer, nullable=False)
    user=db.Column(db.String(40), nullable=False)
    network=db.Column(db.String(50))
    errors = db.Column(db.Text)

class Host(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(40), unique=True, nullable=False)
    vlan=db.Column(db.Integer, nullable=False)
    location=db.Column(db.Integer)
    addvlan=db.Column(db.Boolean)
    publishdns=db.Column(db.Boolean, default=True)
    user=db.Column(db.String(40), nullable=False)
    ipaddress=db.Column(db.String(20))
    hostname=db.Column(db.String(100))
    errors = db.Column(db.Text)

class TenantsModelView(ModelView):
    create_template = 'tenant_create.html'
    list_template = 'tenant_list.html'
    can_export = True
    form_columns = ['name', 'description']

class IegisidModelView(ModelView):
    create_template = 'iegisid_create.html'
    list_template = 'iegisid_list.html'
    can_export = True
    form_columns = ['name', 'description']

class MGMTModelView(ModelView):
    create_template = 'mgmt_create.html'
    list_template = 'mgmt_list.html'
    can_delete = False
    can_edit = False
    can_export = True
    column_searchable_list = ['vlanname', 'vlandescription']
    #form_excluded_columns = ['vlan','network']
    form_columns = ['datacenter', 'DMZ', 'vlanname', 'vlandescription','cidr','iegisid', 'user']
    form_choices = {
        'DMZ': Config.DMZ,
        'datacenter': Config.Datacenter,
        'cidr': Config.CIDR
    }
    form_args = {
    'vlanname': { 'label': 'VLAN Name' },
    'vlandescription': { 'label': 'VLAN Description' }
    }

class RealModelView(ModelView):
    create_template = 'real_create.html'
    list_template = 'real_list.html'
    can_delete = False
    can_edit = False
    can_export = True
    column_searchable_list = ['vlanname', 'vlandescription']
    #form_excluded_columns = ['vlan','network']
    form_columns = ['datacenter', 'DMZ', 'vlanname', 'vlandescription','cidr','tenant','iegisid', 'user']
    form_choices = {
        'DMZ': Config.DMZ,
        'datacenter': Config.Datacenter,
        'cidr': Config.CIDR
    }
    form_args = {
    'vlanname': { 'label': 'VLAN Name' },
    'vlandescription': { 'label': 'VLAN Description' }
    }

class HostModelView(ModelView):
    create_template = 'host_create.html'
    list_template = 'host_list.html'
    can_edit = False
    can_export = True
    column_searchable_list = ['name']
    form_columns = ['name', 'vlan', 'addvlan','location','publishdns', 'user']
    form_args = {
    'name': { 'validators': [Regexp('^[0-9a-zA-Z-]+$',message='Alleen letters, cijfers en - toegestaan')] },
    'vlan': { 'label': 'VLAN ID' },
    'addvlan': { 'label': 'Add VLAN to name' },
    'location': { 'label': 'Volgnummer in netwerk, leeg voor eerste vrije' },
    'publishdns': { 'label': 'Publish record in DNS' }
    }
