from sqlalchemy import Column, ForeignKey, Integer, String, func, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Categories(Base):
    __tablename__ = 'categories'

    ctg_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'ctg_id': self.ctg_id,
        }


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    date_created = Column(DateTime, server_default=func.now())
    last_modified = Column(DateTime, onupdate=func.current_timestamp())

    ctg_id = Column(Integer, ForeignKey('categories.ctg_id'))
    categories = relationship(Categories)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'ctg_id': self.ctg_id,
        }


engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)
