from sqlite3 import Timestamp
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import CreateClientForm, LoginForm, CreateOrderForm, UpdateOrderForm
from app.models import User, Client, Order,StatusesEnum
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        print(current_user.username)
        return redirect(url_for('clients'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        login_user(user)
        #next_page = request.args.get('next')
        #if not next_page or url_parse(next_page).netloc != '':
        #    next_page = url_for('index')
        return redirect(url_for('clients'))
    return render_template('index.html', title='Sign In', form=form)

@app.route('/clients', methods=['GET'])
def clients():
    page = request.args.get('page',1,type = int)  
    clients = Client.query.order_by(Client.id.asc()).paginate(page,app.config['POSTS_PER_PAGE'],False)
    if clients.has_next:
        next_url = url_for('clients', page=clients.next_num)
    else:
        next_url = None
    if clients.has_prev:
        prev_url = url_for('clients', page=clients.prev_num)
    else:
        prev_url = None
    return render_template('clients.html', title='Clients',clients = clients.items,
        next_url=next_url, prev_url=prev_url)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/clients/create", methods = ['GET','POST'])
@login_required
def createClient():
    form = CreateClientForm()
    if form.validate_on_submit():
        client = Client(name=form.name.data, firstName = form.firstName.data,
            lastName = form.lastName.data, nip = form.nip.data,
            phoneNumber=form.phoneNumber.data, email=form.email.data,
            balance = 0,startDate = datetime.today())
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('clients'))
    return render_template('clientscreate.html', title='Create Client', form=form)

@app.route("/orders/create", methods = ['GET','POST'])
@login_required
def createOrder():
    form = CreateOrderForm()
    if form.validate_on_submit():
        order = Order(
            subject=form.subject.data, 
            price = form.price.data,
            description = form.description.data, comment = form.comment.data,
            status=form.status.data, client= Client.query.filter_by(name=form.client.data).first_or_404()  ,
            startDate = datetime.today())
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('orders'))
    return render_template('orderscreate.html', title='Create Order', form=form)


@app.route("/clients/<id>", methods = ['GET'])
@login_required
def viewClient(id):
    page = request.args.get('page',1,type = int)  
    client = Client.query.filter_by(id=id).first_or_404()
    orders = client.ordered.order_by(Order.startDate.desc()).paginate(page,app.config['POSTS_PER_PAGE'],False)
    if orders.has_next:
        next_url = url_for('viewClient', id = client.id, page=orders.next_num)
    else:
        next_url = None
    if orders.has_prev:
        prev_url = url_for('viewClient',id = client.id, page=orders.prev_num)
    else:
        prev_url = None
    return render_template('client.html', client=client, orders=orders.items
        ,next_url=next_url,prev_url=prev_url )

@app.route("/orders/<id>", methods = ['GET','POST'])
@login_required
def viewOrder(id):
    order = Order.query.filter_by(id=id).first_or_404()
    form = UpdateOrderForm(obj = order)
    
    
    if request.method=="POST":
        form.populate_obj(order)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('orders'))

    form.status.default = order.status.name
    form.process()
    return render_template('order.html',order = order, form = form)

@app.route("/orders",methods = ['GET'])
@login_required
def orders():
    page = request.args.get('page',1,type = int)  
    orders = Order.query.order_by(Order.id.asc()).paginate(page,app.config['POSTS_PER_PAGE'],False)   
    if orders.has_next:
        next_url = url_for('orders', page=orders.next_num)
    else:
        next_url = None
    if orders.has_prev:
        prev_url = url_for('orders', page=orders.prev_num)
    else:
        prev_url = None
    return render_template('orders.html', title='Orders',orders = orders.items,
        next_url=next_url, prev_url=prev_url)

