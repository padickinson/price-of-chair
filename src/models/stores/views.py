import uuid
import src.models.users.decorators as user_decorators
from flask import Blueprint, url_for, json
from flask import render_template
from flask import request
from werkzeug.utils import redirect

from src.models.stores.store import Store

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/')
def index():
    stores = Store.get_store_list()
    return render_template('stores/store_index.jinja2', stores=stores)


@store_blueprint.route('/store/<string:store_id>')
def store_page(store_id):
    return render_template('stores/store.jinja2', store=Store.get_by_id(uuid.UUID(store_id)))


@store_blueprint.route('/new', methods=['GET', 'POST'])
def create_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])
        Store(name, url_prefix, tag_name, query).save_to_mongo()
        return redirect(url_for('.index'))
    return render_template('stores/new_store.jinja2')


@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@user_decorators.requires_admin_permissions
def edit_store(store_id):
    store = Store.get_by_id(uuid.UUID(store_id))
    if request.method == 'POST':
        store.name = request.form['name']
        store.url_prefix = request.form['url_prefix']
        store.tag_name = request.form['tag_name']
        store.query = json.loads(request.form['query'])
        store.save_to_mongo()
        return redirect(url_for('.index'))
    return render_template('stores/edit_store.jinja2', store=store)


@store_blueprint.route('/delete/<string:store_id>')
@user_decorators.requires_admin_permissions
def delete_store(store_id):
    Store.get_by_id(uuid.UUID(store_id)).delete()
    return redirect(url_for('.index'))
