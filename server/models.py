from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey, Integer, String, Column
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)

    # Relationship
    pizzas = association_proxy('restaurant_pizzas', 'pizza')

    # Serialization rules
    serialize_rules = ('-restaurant_pizzas.restaurant',)

    def __repr__(self):
        return f'<Restaurant {self.name}>'


class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    ingredients = Column(String)

    # Relationship
    restaurants = association_proxy('restaurant_pizzas', 'restaurant')

    # Serialization rules
    serialize_rules = ('-restaurant_pizzas.pizza',)

    def __repr__(self):
        return f'<Pizza {self.name}, {self.ingredients}>'


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id', ondelete='CASCADE'))
    pizza_id = Column(Integer, ForeignKey('pizzas.id', ondelete='CASCADE'))
    price = Column(Integer, nullable=False)

    # Relationships
    restaurant = relationship('Restaurant', backref=db.backref('restaurant_pizzas', cascade='all, delete-orphan'))
    pizza = relationship('Pizza', backref=db.backref('restaurant_pizzas', cascade='all, delete-orphan'))

    # Serialization rules
    serialize_only = ('id', 'price', 'restaurant_id', 'pizza_id', 'restaurant.name', 'pizza.name', 'pizza.ingredients')

    # Validation
    @validates('price')
    def validate_price(self, key, price):
        if not 1 <= price <= 30:
            raise ValueError("Price must be between 1 and 30")
        return price

    def __repr__(self):
        return f'<RestaurantPizza ${self.price}>'

