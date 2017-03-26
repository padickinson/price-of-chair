from flask import Blueprint
import uuid

from flask import render_template, request, session, url_for
from werkzeug.utils import redirect

from src.models.alerts.alert import Alert
from src.models.items.item import Item
import src.models.users.decorators as user_decorators

alert_blueprint = Blueprint('alerts', __name__)



@alert_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_login  # redirect the user to users/login if they aren't logged in.
def create_alert():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        price_limit = float(request.form['price_limit'])
        item = Item(name, url)
        item.save_to_mongo()
        alert = Alert(session['user_id'], price_limit, item._id)
        alert.do_price_check()  # saves to mongodb.
        return redirect(url_for('users.user_alerts'))

    return render_template('alerts/new_alert.jinja2')  # Send the user an error if invalid login

@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@user_decorators.requires_login  # redirect the user to users/login if they aren't logged in.
def edit_alert(alert_id):
    alert=Alert.get_by_id(uuid.UUID(alert_id))
    if request.method == 'POST':
        alert.price_limit = float(request.form['price_limit'])
        alert.do_price_check()  # saves to mongodb.
        return redirect(url_for('users.user_alerts'))

    return render_template('alerts/edit_alert.jinja2',alert=alert)  # Send the user an error if invalid login




@alert_blueprint.route('/deactivate/<string:alert_id>')
def deactivate_alert(alert_id):
    Alert.get_by_id(uuid.UUID(alert_id)).deactivate()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/activate/<string:alert_id>')
def activate_alert(alert_id):
    Alert.get_by_id(uuid.UUID(alert_id)).activate()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/delete/<string:alert_id>')
def delete_alert(alert_id):
    Alert.get_by_id(uuid.UUID(alert_id)).delete_from_db()
    return redirect(url_for('users.user_alerts'))



@alert_blueprint.route('/<string:alert_id>')
@user_decorators.requires_login
def get_alert_page(alert_id):
    alert = Alert.get_by_id(uuid.UUID(alert_id))
    return render_template('alerts/alert.jinja2', alert=alert)


@alert_blueprint.route('/for_user/<string:user_id>')
def get_alerts_for_user(user_id):
    pass

@alert_blueprint.route('/check_price/<string:alert_id>')
def check_price(alert_id):
    Alert.get_by_id(uuid.UUID(alert_id)).do_price_check()
    return redirect(url_for('.get_alert_page', alert_id=alert_id))