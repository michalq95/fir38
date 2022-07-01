from flask import jsonify, request
from app import app, api
from flask_restx import Resource, Api
from app.models import Client,Order
from sqlalchemy import desc



@api.route('/clients')
class clients_api(Resource):
    def get(self):
        page = request.args.get('page',1,type=int)
        per_page = app.config['POSTS_PER_PAGE']
        data = Order.colAPI(Client.query.order_by(Client.id.asc()),page,per_page,'apis.clients_api') 
        return jsonify(data)


@api.route('/client/<string:id>')
class client_api(Resource):
    def get(self,id):
        client = Client.query.get_or_404(id)
        return jsonify(client.to_dict())
    

@api.route('/client/<string:id>/ordered')
class clients_ordered_api(Resource):
    def get(self,id):
        client = Client.query.get_or_404(id)
        page = request.args.get('page', 1, type=int)
        per_page = app.config['POSTS_PER_PAGE']
        data = Order.colAPI(Order.query.filter_by(client_id=client.id), \
            page,per_page,'apis.clients_ordered_api', id = id)
        return jsonify(data)

@api.route('/orders')
class orders_api(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = app.config['POSTS_PER_PAGE']        
        data = Order.colAPI(Order.query.order_by(Order.id.asc()),page,per_page,'apis.orders_api')
        return jsonify(data)

    

    