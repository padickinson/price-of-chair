from functools import wraps

from flask import session, url_for, redirect, request

from src.app import app


def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session.keys() or session['user_id'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        return func(*args, **kwargs)

    return decorated_function


def requires_admin_permissions(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session.keys() or session['user_id'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        if session['email'] not in app.config['ADMINS']:
            return redirect(url_for('users.login_user', message="Only accessible to admins"))
        return func(*args, **kwargs)

    return decorated_function
