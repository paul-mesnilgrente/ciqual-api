from app import app, db

from app.models import Group, SubGroup, SubSubGroup
from app.models import Food, Component, FoodComponent
from app.models import Source, User

@app.shell_context_processor
def make_shell_context():
    return {
    	'db': db,
    	'User': User,
    	'Group': Group,
    	'SubGroup': Group,
    	'SubSubGroup': Group,
    	'Food': Food,
    	'Component': Component,
		'FoodComponent': FoodComponent,
		'Source': Source,
    }