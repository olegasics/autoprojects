from flask_migrate import Migrate

# from apps.chat.views import MessageAPIView, RoomAPIView, MainAPIView
# from apps.auth.views import UserAPIView, AuthAPIView, RegAPIView
# # from apps.fluidbusiness.views import OrderAPIView, ManagerAPIView, ProjectAPIView, LogistAPIView
from db_config import app, db

migrate = Migrate(app, db)


# def register_api(view, endpoint, url, pk='id', pk_type='int'):
#     view_func = view.as_view(endpoint)
#     app.add_url_rule(url, defaults={pk: None},
#                      view_func=view_func, methods=['GET'],)
#     app.add_url_rule(url, view_func=view_func, methods=['POST'])
#     app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
#                      methods=['GET', 'PUT', 'DELETE', 'POST'])


# register_api(UserAPIView, 'user_api', '/users/')
# register_api(MessageAPIView, 'message_api', '/messages/', pk='message_text', pk_type='string')
# register_api(RoomAPIView, 'room_api', '/rooms/', pk='room_id')
# register_api(OrderAPIView, 'order_api', '/orders/', pk='order_id')
# register_api(LogistAPIView, 'logist_api', '/logists/')


# view_func_auth = AuthAPIView.as_view('auth_api')
# app.add_url_rule('/login/', view_func=view_func_auth, methods=['GET', 'POST'])

# view_func = RegAPIView.as_view('reg_api')
# app.add_url_rule('/reg/', view_func=view_func, methods=['GET'])

# view_func_fluid = ManagerAPIView.as_view('manager_api')
# app.add_url_rule('/managers/', view_func=view_func_fluid, methods=['GET', 'POST', 'UPDATE', 'DELETE'])

# view_func_fluid = ProjectAPIView.as_view('project_api')
# app.add_url_rule('/projects/', view_func=view_func_fluid, methods=['GET', 'POST', 'UPDATE', 'DELETE'])

db.drop_all()
if __name__ == '__main__':
    app.run(debug=True)
    db.drop_all()