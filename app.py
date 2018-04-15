import os
from flask import Flask, url_for, redirect, render_template, request, abort
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
import random
import json
from collections import defaultdict


# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


    can_edit = False
    create_modal = True
    can_export = True

class CustomView(MyModelView):
    column_editable_list = ['email']
    can_view_details = True
    view_details_modal = True
    column_searchable_list = ['email']
    column_exclude_list = ['password']

# Flask views
@app.route('/')
def index():
    return render_template('index.html')
	
@app.route('/toggleNode')
def toggleNode():
    # here we want to get the value of user (i.e. ?user=some-value)
    node = request.args.get('node')
    print(node)

    with open('nodestatus.txt', 'a+') as f:
        print ('Writing ', node, 'to file')
        f.write(str(node))
        f.write('\n')
        f.close()
    return("success")

@app.route('/changeEnergyMode')
def toggleMode():
    newMode = request.args.get('mode')
    with open('modestatus.txt', 'w') as f:
        f.write(newMode)
        f.close()
    return("success")	
	
@app.route('/getCurrentEnergyUsedAndProduced')
def getEnergyUsedAndProduced():
	metrics = dict()
	# TO DO
	# Fill up with real values
	metrics['energyProduced'] = random.randint(2000,11000)
	metrics['energyConsumed'] = random.randint(4000,10000)
	return json.dumps(metrics)
    
@app.route('/getCurrentNodePowerValues')
def getNodePowerValues():
	# status:power
	with open('powerusagestatus.txt', 'r') as f:
		line = f.readlines()[-1]
        f.close()
	return line
	
# Create admin
admin = flask_admin.Admin(
    app,
    'Dashboard Example',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

# Add model views
admin.add_view(MyModelView(Role, db.session))
admin.add_view(CustomView(User, db.session))
#admin.add_view(LocationVerticalView(category='Locations'))

if __name__ == '__main__':
    # Start app
    app.run(debug=True)
