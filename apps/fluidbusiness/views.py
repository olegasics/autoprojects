import requests
import os
import webbrowser

from flask.views import MethodView, request
from flask_mail import Message
from flask import render_template, url_for, redirect, flash, session, send_from_directory
from flask_classy import FlaskView, route
from sqlalchemy.orm import  joinedload
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from base64 import b64decode

from apps.fluidbusiness.models import Order, Manager, Project, Invoice, Ttn, Payment, Provider, Document
from apps.auth.models import User, Role
from db_config import db, app, APP_KEY, SESSION_ID, ALLOWED_EXTENSIONS, mail



class OrdersView(FlaskView):

    # @cache.cached(timeout=3600)
    @login_required
    def get(self):
        ended = request.args.get('ended')
        query = db.session.query(Order).options(joinedload('invoices'))
        orders = query.filter(Order.state_order != 'Доставлен').all()

        if ended == '0':
            orders = query.all()
        elif ended == '1':
            orders = query.filter(Order.state_order != 'Доставлен').all()

        projects = db.session.query(Project).options(joinedload('manager')).all()

        return render_template('orders.html', orders=orders, projects=projects, ended=ended)

    
    def patch(self, order_id):
        project_name = request.form.get('name')
        ttn_name = request.form.get('ttn')
        invoice_name = request.form.get('invoice')
        cargo = request.form.get('cargo')
        # state = request.form.get('state')
        state_order_text = request.form.get('state_order_text_custom') # TODO value NULL
        state_order_text_dl = request.form.get('state_order_text_dl')

        order = Order.query.get(order_id)
        project = Project.query.filter_by(name=project_name.strip()).first()
        ttn = Ttn.query.filter_by(name=ttn_name.strip()).first()

        if project:
            order.projects.append(project)
        
        if ttn is None:
            ttn = Ttn(name=ttn_name.strip(), order_id=order_id)
            db.session.add(ttn)
            ttn = Ttn.query.filter_by(name=ttn_name.strip()).first()
            order.ttn = ttn
        else:
            order.ttn = ttn 

        if order.invoices:
            order.invoices[0].name = invoice_name
        else:
            invoice = Invoice(name=invoice_name, project_id=project.id)
            order.invoices.append(invoice)
        
        # if state:
        #     order.state_order = state
        if state_order_text:
            order.state_order = state_order_text
        elif state_order_text_dl:
            order.state_order = state_order_text_dl

        order.cargo = cargo.strip()
        db.session.commit()
        
        return order.to_dict()

    def post(self):
        project_name = request.form['name']
        cargo = request.form['cargo']
        status = request.form['status']
        sender = request.form['sender']
        receiver = request.form['receiver']
        document = request.form.get('document')
        carrier = request.form['carrier']
        ttn_name = request.form['ttn']
        send_city = request.form.get('send_city')
        delivery_city = request.form.get('delivery_city')
        send_date = request.form.get('send_date')
        delivery_date = request.form.get('delivery_date')
        weight = request.form.get('weight')
        volume = request.form.get('volume')
        sum_ = request.form.get('sum')
        project = Project.query.filter_by(name=project_name).first()

        try:
            invoice_name = request.form['invoice']
            if invoice_name == 'No invoice':
                invoice = Invoice.query.filter_by(name=invoice_name).first()
            invoice = Invoice(name=invoice_name.strip(), project_id=project.id)
        except Exception:
            invoice = Invoice.query.filter_by(name='No invoice').first()


        ttn = Ttn(name=ttn_name.strip())

        document = Document(doc_number=document.strip())
        
        order = Order(
            cargo=cargo,
            state_order=status, 
            sender=sender, 
            receiver=receiver, 
            carrier=carrier,
            ttn=ttn,
            city_send=send_city,
            city_delivery=delivery_city,
            date_send=send_date,
            date_delivery=delivery_date,
            weight=weight,
            volume=volume,
            total_sum=sum_
        )

        order.projects.append(project)
        order.invoices.append(invoice)
        order.doc_numbers.append(document)

        db.session.add(order)
        db.session.commit()
        
        return order.to_dict() 

    @route('/<project_id>')
    def search_by_project_name(self, project_id):
        query = db.session.query(Order).options(joinedload('invoices'))
        orders = query.filter(Order.projects).filter(Project.id == project_id).all()
        projects = db.session.query(Project).options(joinedload('manager')).filter_by(id=project_id).all()
        
        return render_template('orders_for_filter.html', orders=orders, projects=projects)

    @route('/managers/<manager_small_name>')
    def search_by_manager_small_name(self, manager_small_name):
        query = db.session.query(Order).options(joinedload('invoices'), joinedload('projects'))

        orders = query.\
        filter(Order.projects).\
        filter(Project.manager).\
        filter(Manager.small_name == manager_small_name).all()

        projects = db.session.query(Project).\
        options(joinedload('manager')).\
        filter(Manager.small_name == manager_small_name).all()

        return render_template('orders_for_filter.html', orders=orders, projects=projects)


class ManagersView(FlaskView):

    @login_required
    def get(self):
        managers = Manager.query.all()
        return render_template('manager.html', managers=managers)

    def post(self, endpoint='create'):
        name = request.form['name']
        small_name = request.form['small_name']
        number_phone = request.form['number_phone']
        manager = Manager(name=name.strip(), small_name=small_name.strip(), number_phone=number_phone.strip())
        db.session.add(manager)
        db.session.commit()
        managers = Manager.query.all()
        return redirect(url_for('ManagersView:get'))

    def update(self):
        pass

    def delete(self):
        pass

    @route('/<manager_id>')
    def get_by_id(self, manager_id):
        manager = Manager.query.get(manager_id)
        projects = db.session.query(Project).filter(Project.manager.__eq__(manager)).all()

        return render_template('info_manager.html', manager=manager, projects=projects)


class ProjectsView(FlaskView):  
    @login_required
    def get(self):
        projects = Project.query.all()
        managers = Manager.query.all()
        return render_template('project.html', projects=projects, managers=managers)

   
    def post(self, endpoint='create'):
        name = request.form['name']
        manager_small_name = request.form['manager_small_name']
        manager = Manager.query.filter_by(small_name=manager_small_name).first()
        customer = request.form['customer']
        
        project = Project(name=name.strip(), manager_id=manager.id, customer=customer.strip())
        manager.projects.append(project)

        db.session.add(project)
        db.session.commit()

        return redirect(url_for('ProjectsView:get'))

    @route('/<project_id>')
    def get_by_name(self, project_id):
        project = db.session.query(Project).filter_by(id=project_id).options(joinedload('manager')).first()
        query = db.session.query(Order).options(joinedload('invoices'))
        orders = query.filter(Order.projects).filter(Project.id == project_id).all()
        total_sum = 0
        total_weight_delivery = 0
        total_weight_send = 0
        for order in orders:

            total_sum += order.total_sum if order.total_sum else 0

            if order.receiver == 'ООО "КБ РУССКИЕ НАСОСЫ"':
               if order.weight:
                   total_weight_delivery += float(order.weight)
               else:
                   total_weight_delivery += 0
            elif order.sender == 'ООО "КБ РУССКИЕ НАСОСЫ"':
                if order.weight:
                    total_weight_send += float(order.weight)
                else:
                    total_weight_send += 0

            
        return render_template('info_project.html', total_weight_delivery=total_weight_delivery, total_weight_send=total_weight_send,
                               total_sum=total_sum, order=orders, project=project)


class LogistsView(FlaskView):
    route_base = '/logistics'

    @login_required
    # @cache.cached(timeout=3600)
    def get(self):
        ended = request.args.get('ended')

        query = db.session.query(Order).options(joinedload('invoices'))
        orders = query.filter(Order.state_order != 'Доставлен').all()

        if ended == '0':
            orders = query.all()
        elif ended == '1':
            orders = query.filter(Order.state_order != 'Доставлен').all()

        projects = db.session.query(Project).options(joinedload('manager')).all()
        return render_template('logist_settings.html', orders=orders, projects=projects, ended=ended)
    
    
    def post(self):
        response = requests.post('https://api.dellin.ru/v3/orders.json', json={
                "appkey": APP_KEY,
                "sessionID": SESSION_ID,
                "page": 1,
                "orderDatesExtended": True,
                "orderBy": "ordered_at"
            })

        carrier = 'Деловые линии'    
            
        for order in response.json()['orders']:

            state_order = order['stateName']
            sender = order['sender']['name']
            receiver = order['receiver']['name']
            total_sum = order['totalSum']
            date_delivery = order['stateDate']
            documents = order['documents']
            date_send = order['produceDate']
            city_send = order['derival']['city']
            city_delivery = order['arrival']['city']
            weight = order['freight']['weight']
            volume = order['freight']['volume']

            if state_order == 'Заказ завершен':
                state_order = 'Доставлен'

            if date_delivery is None:
                date_delivery = 'Не определна'

            for document in documents:
                doc_number = document.get('id')
                doc_number_obj = Document.query.filter_by(doc_number=str(doc_number)).first()
                order_check_new = Order.query.options(joinedload('doc_numbers')).filter(Order.doc_numbers).\
                    filter(Document.doc_number == str(doc_number)).first()
                if doc_number_obj is None:
                    doc_number_obj = Document(doc_number=doc_number)
                    db.session.add(doc_number_obj)
                    doc_number = Document.query.filter_by(doc_number=doc_number)

                order_check_old = Order.query.options(joinedload('doc_numbers')).filter(Order.doc_numbers).\
                    filter(Document.doc_number == str(documents[0].get('id'))).first()

                if order_check_new is None and order_check_old is None:
                    new_order = Order(
                        state_order=state_order,
                        sender=sender,
                        receiver=receiver,
                        total_sum=total_sum,
                        date_delivery=date_delivery,
                        carrier=carrier,
                        date_send=date_send,
                        city_send=city_send,
                        city_delivery=city_delivery,
                        weight=weight,
                        volume=volume
                    )

                    db.session.add(new_order)
                    if doc_number_obj is not None:
                        new_order.doc_numbers.append(doc_number_obj)

                elif order_check_old is not None:
                    if order['orderDates']['arrivalToReceiver']:
                        date_delivery = (order['orderDates']['arrivalToReceiver']).split(' ')[0]
                    order_check_old.weight = weight
                    order_check_old.volume = volume
                    order_check_old.doc_number = str(doc_number)
                    order_check_old.state_order = state_order
                    order_check_old.date_send=date_send
                    order_check_old.date_delivery = date_delivery
                    order_check_old.total_sum = total_sum
                    order_check_old.doc_numbers.append(doc_number_obj)

                db.session.commit()

        return redirect(url_for('LogistsView:get'))

    @route('/upload/<order_id>', methods=['GET', 'POST'])
    def upload(self, order_id):
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/invoices_logist', filename))
                order = Order.query.get(order_id)
                payment = Payment.query.filter_by(order_id=order.id).first()
                payment.file_invoice_cargo = app.config['UPLOAD_FOLDER'] + '/invoices_logist/' + str(filename)
                # order.file_invoice_cargo = app.config['UPLOAD_FOLDER'] + '/invoices_logist/' + str(filename)
                db.session.commit()
                return redirect(url_for('LogistsView:get'))

            return redirect(url_for('LogistsView:get'))

    @route('/download/<order_id>', methods=['GET'])
    def download(self, order_id):
        order = Order.query.get(order_id)
        directory = order.file_invoice_cargo
        directory_file_name_list = smash_file_name(directory)
        return send_from_directory(directory=directory_file_name_list[0] + '/', filename=directory_file_name_list[1], as_attachment=True)

class PaymentsView(FlaskView):
    route_base = '/payments'

    @login_required
    def get(self):
        query = Payment.query
        if current_user.position == 'Логист':
            payments = query.all()
            return render_template('payments.html', payments=payments)
        elif current_user.position == 'Директор':
            payments = query.filter_by(state='Ожидает согласования')
            return render_template('payments_director.html', payments=payments)
        elif current_user.position == 'Бухгалтер':
            payments = query.filter_by(state='Ожидает оплаты')
            return render_template('payments_buh.html', payments=payments, current_user=current_user)


    def post(self):
        order_id = request.form.get('order_id')
        order = Order.query.get(order_id)

        for doc in order.doc_numbers:
            payment = Payment(
                    doc_number=doc.doc_number,
                    weight=order.weight,
                    volume=order.volume,
                    sum_=order.total_sum,
                    state='Ожидает согласования',
                    order_id=order.id if order else None,

            )

            db.session.add(payment)
        db.session.commit()

        # Уведомление директору
        send_email_director()

        return order.to_dict()

    def patch(self):
        payment_id = request.form.get('payment_id')
        state_payment = request.form.get('state_payment')

        payment = Payment.query.get(payment_id)
        payment.state = state_payment

        db.session.commit()
        return ''


    @route('update', endpoint='update')
    def update(self):

        response = requests.post('https://api.dellin.ru/v1/customers/mutual_calculations.json', json={
                    "appkey": APP_KEY,
                    "sessionID": SESSION_ID,
                    "month": 6,
                    "year": 2020
        })

        for payment in response.json()['document']:
            if payment['docType'] == 'ДвижениеБанк':
                continue
            elif payment['docType'] == 'СчетЗаХранение':
                continue

            doc_uid = payment['docSQLuid']
            doc_number = payment['docID']
            weight = payment['weight']
            volume = payment['volume']
            sum_ = payment['sum']
            date = payment['date']
            payment_bool = payment['payment']
            order = Order.query.options(joinedload('doc_numbers')).filter(Order.doc_numbers). \
                filter(Document.doc_number == str(doc_number)).first()
            payment_check = Payment.query.filter_by(doc_number=str(doc_number)).first()

            filename = f'{"-".join([project.name for project in order.projects])}_invoice_{doc_number}' if order else f'not_project_invoice_{doc_number}'
            directory = os.path.join(app.config['UPLOAD_FOLDER'] + '/invoices_logist', filename)

            state_payment = 'Оплачен' if payment_bool else 'Ожидает согласования'

            if payment_check is None:
                payment = Payment(
                    doc_uid=doc_uid, 
                    doc_number=doc_number, 
                    weight=weight, 
                    volume=volume,
                    sum_=sum_,
                    date=date.split(' ')[0],
                    order_id=order.id if order is not None else None,
                    state=state_payment
                )
                if state_payment == 'Ожидает согласования':
                    send_email_director()

                db.session.add(payment)
                db.session.commit()

            else:
                payment_check.sum_ = sum_
                payment_check.order_id = order.id if order is not None else None
                if payment_check.state != 'Ожидает согласования' or payment_check.state != 'Ожидает оплаты':
                    payment_check.state = state_payment

                payment_check.date = date.split(' ')[0]
                payment_check.file_invoice_cargo = f'{directory}.pdf'

            if doc_uid:
                responseFile = requests.post('https://api.dellin.ru/v1/customers/orders/printable.json', json={
                    "appkey": APP_KEY,
                    "sessionID": SESSION_ID,
                    "docUid" : doc_uid,
                    "mode": "bill"
                })

                bytes = b64decode(responseFile.json()['pdf'], validate=True)
                with open(f'{directory}.pdf', 'wb') as f:
                    f.write(bytes)


        payment = Payment.query.filter_by(doc_number=str(doc_number)).first()
        payment.file_invoice_cargo = f'{directory}.pdf'
        db.session.commit()

        return redirect(url_for('PaymentsView:get'))

    @route('/approve/<payment_id>')
    def approve(self, payment_id):
        payment = Payment.query.get(payment_id)
        payment.state = "Ожидает оплаты"
        db.session.commit()

        send_email_buh(payment.doc_number, payment.sum_)

        return '200'

    @route('/upload/<payment_id>', methods=['GET', 'POST'])
    def upload(self, payment_id):
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/invoice_pp', filename))
                payment = Payment.query.get(payment_id)
                payment.file_pp = app.config['UPLOAD_FOLDER'] + '/invoice_pp/' + str(filename)
                payment.state = 'Оплачен'
                db.session.commit()
                # Уведомление логистам и директору об оплате
                if payment.order.projects:
                    projects = ", ".join([project.name for project in payment.order.projects])
                else:
                    projects = 'Без проекта'
                send_email_logist(doc_number=payment.doc_number, project=projects)

                return redirect(url_for('PaymentsView:get'))

            return redirect(url_for('PaymentsView:get'))

    @route('/download/<payment_id>/<file>', methods=['GET'])
    def download(self, payment_id, file):
        payment = Payment.query.get(payment_id)
        directory = 'aa'
        if file == '1':
            directory = payment.file_invoice_cargo
        elif file == '2':
            directory = payment.file_pp
        directory_file_name_list = smash_file_name(directory)
        return send_from_directory(directory=directory_file_name_list[0] + '/',
                                   filename=directory_file_name_list[1],
                                   as_attachment=False
                                   )


class ProvidersView(FlaskView):
    @login_required
    def get(self):
        project_id = request.args.get('project')
        project = Project.query.get(project_id)
        providers = db.session.query(Provider).options(joinedload('invoices'))

        return render_template('providers.html', project=project, providers=providers)

    def post(self):
        name = request.form.get('name')
        project_id = request.form.get('project_id')

        project = Project.query.get(project_id)

        provider = Provider(name=name)

        provider.projects.append(project)

        db.session.add(provider)
        db.session.commit()

        return redirect(url_for('ProvidersView:get'))

class DirectorsView(FlaskView):
    def get(self):
        pass

    def post(self):
        pass

class HomeView(FlaskView):
    def get(self):
        return render_template('home.html')

    def post(self):
        pass

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def smash_file_name(upload_file):
    return upload_file.rsplit('/', 1)

def send_email_director():
    msg = Message('Новый счет на согласование', sender=f'{current_user.email}',
                  recipients=['omaslo@fluidbusiness.ru'])
    msg.body = 'Новый счет на согласование. Доступен по ссылке - http://127.0.0.1:5000/payments/'
    mail.send(msg)


def send_email_buh(doc_number, sum):
    msg = Message('Новый счет на оплату от отдела логистики', sender=current_user.email,
                  recipients=['omaslo@fluidbusiness.ru'])
    msg.body = f'Счет {doc_number} на сумму {sum} рублей согласован и ждет оплаты. После оплаты,' \
               f' просим подтвердить оплату платежным поручением.' \
               f' Счет доступен по ссылке - http://127.0.0.1:5000/payments/'
    mail.send(msg)

def send_email_manager_new_order(project_name, email):
    msg = Message(f'{project_name} новая перевозка',
                  recipients=[email])
    msg.body = f'Добавлена перевозка по проекту  {project_name}'
    mail.send(msg)


def send_email_manager_change_status(project_name, old_status, new_status):
    msg = Message(f'{project_name} Статус груза изменился',
                  recipients=['omaslo@fluidbusiness.ru'])
    msg.body = f'Статус груза изменился с {old_status} на {new_status}'
    mail.send(msg)

def send_email_logist(doc_number, project):
    msg = Message(f'{project } счет {doc_number} оплачен',
                  recipients=['omaslo@fluidbusiness.ru'])
    msg.body = f'Счет {doc_number} оплачен. Посмотреть платежное поручение можно по ссылке - ' \
               f'http://127.0.0.1:5000/payments/'
    mail.send(msg)