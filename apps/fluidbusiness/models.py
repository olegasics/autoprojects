from sqlalchemy_serializer import SerializerMixin

from db_config import db

order_project = db.Table(
    'order_project',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
)

order_invoice = db.Table(
    'order_invoice',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('invoice_id', db.Integer, db.ForeignKey('invoice.id'), primary_key=True)
)

provider_project = db.Table(
    'provider_project',
    db.Column('provider_id', db.Integer, db.ForeignKey('provider.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True)
)

order_document = db.Table(
    'order_doc_number',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('doc_number_id', db.Integer, db.ForeignKey('document.id'), primary_key=True),

)


class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    small_name = db.Column(db.String(10), nullable=False)
    number_phone = db.Column(db.String(30))
    projects = db.relationship('Project')


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'), nullable=True)
    customer = db.Column(db.String(100), nullable=False)
    manager = db.relationship(Manager, lazy='joined', innerjoin=True)
    providers = db.relationship('Provider', secondary='provider_project', lazy='joined',
                                backref=db.backref('projects', lazy=True))
    

class Ttn(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))
    provider = db.relationship('Provider', lazy='joined')



class Order(db.Model, SerializerMixin):
    serialize_only = (
        'id',
        'state_order',
        'sender',
        'receiver',
        'total_sum',
        'date_delivery'
    )
    
    id = db.Column(db.Integer, primary_key=True)
    state_order = db.Column(db.String(50))
    sender = db.Column(db.String(100))
    receiver = db.Column(db.String(100))
    carrier = db.Column(db.String(100), nullable=False)
    total_sum = db.Column(db.Float)
    cargo = db.Column(db.String(300))
    date_delivery = db.Column(db.String(100))
    date_send = db.Column(db.String(100))
    city_send = db.Column(db.String(50))
    city_delivery = db.Column(db.String(50))
    weight =  db.Column(db.String(10))
    volume =  db.Column(db.String(10))
    ttn = db.relationship('Ttn', backref='order', lazy='joined', uselist=False)
    projects = db.relationship('Project', secondary='order_project', lazy='joined',
                               backref=db.backref('orders', lazy='joined'))

    invoices = db.relationship('Invoice', secondary='order_invoice', lazy='joined',
                                backref=db.backref('orders', lazy=True))

    payments = db.relationship('Payment', lazy='joined')
    doc_numbers = db.relationship('Document', secondary='order_doc_number', lazy='joined',
                                backref=db.backref('orders', lazy=True))
    

class Payment(db.Model, SerializerMixin):
    serialize_only = {
        'doc_number',
        'date',
        'sum_',
        'weight',
        'volume',
        'doc_uid',
        'state'
    }
    id = db.Column(db.Integer, primary_key=True)
    doc_number = db.Column(db.String(30))
    date = db.Column(db.String(50))
    sum_ = db.Column(db.String(10))
    weight =  db.Column(db.String(10))
    volume =  db.Column(db.String(10))
    doc_uid = db.Column(db.String(100), unique=True)
    state = db.Column(db.String(50))
    order = db.relationship('Order', lazy='joined')
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)
    file_pp = db.Column(db.String(500))
    file_ttn = db.Column(db.String(500))
    file_invoice_cargo = db.Column(db.String(500), nullable=True)


class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    invoices = db.relationship('Invoice', lazy='joined')


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.relationship('Order', lazy='joined')
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)
    doc_number = db.Column(db.String(30), nullable=False)
