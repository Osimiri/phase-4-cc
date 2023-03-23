from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here
class Pizza(db.model, SerializerMixin):
    __tablename__ = 'pizzas'

    serialize_rules = ('-restaurant_pizzas', '-restaurants.pizzas', '-created_at', '-updated_at')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    restaurant_pizzas = db.relationship('RestaurantPizza', backref = 'pizza')
    restaurants = association_proxy(restaurant_pizzas, 'restaurant')


class Restaurant(db.model, SerializerMixin):
    __tablename__ = 'restaurants'

    serialize_rules = ('-restaurant_pizzas', '-created_at', '-updated_at')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    restaurant_pizzas = db.relationship('RestaurantPizza', backref = 'restaurant')
    pizzas = association_proxy('restaurant_pizzas', 'pizza')

class RestaurantPizza(db.model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    @validates('price')
    def validate_price(self,key,value):
        if value and 1 < value < 30:
            return value 
        raise ValueError('Must have a price between 1 and 30 bozo')

