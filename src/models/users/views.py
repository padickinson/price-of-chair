from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
import src.models.users.errors as UserErrors
from src.models.users.user import User
import src.models.users.decorators as user_decorators

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['POST', 'GET'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                session['user_id'] = User.get_by_email(email)._id
                return redirect(url_for(".user_alerts"))
        except (UserErrors.UserNotExistsError, UserErrors.IncorrectPasswordError) as e:
            return e.message

    return render_template("/users/login.jinja2")  # Send the user an error if invalid login


@user_blueprint.route('/register', methods=['POST', 'GET'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.register_user(email, password):
                session['email'] = email
                session['user_id'] = User.get_by_email(email)._id
                return redirect(url_for(".user_alerts"))
        except (UserErrors.UserError) as e:
            return e.message

    return render_template("/users/register.jinja2")  # Send the user an error if invalid login


@user_blueprint.route('/alerts')
@user_decorators.requires_login
def user_alerts():
    user = User.get_by_id(session['user_id'])
    alerts = user.get_alerts()
    return render_template('users/alerts.jinja2',alerts=alerts, logged_in_user_email=user.email)


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    session['user_id'] = None
    return redirect(url_for("home"))


@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass
