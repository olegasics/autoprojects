from flask_migrate import Migrate
from apps.fluidbusiness.views import ProjectsView, LogistsView, OrdersView, ManagersView, PaymentsView, ProvidersView
from apps.chat.views import RoomAPIView, MessageAPIView

from db_config import app, db

ProjectsView.register(app)
LogistsView.register(app)
OrdersView.register(app)
ManagersView.register(app)
PaymentsView.register(app)
ProvidersView.register(app)

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
