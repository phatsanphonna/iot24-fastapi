from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from database import Base
from model.menu import Menu


class Order(Base):
    __tablename__ = 'order'
    
    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(ForeignKey('menu.id'), index=True)
    menu = relationship('Menu')
    quantity = Column(Integer, index=True)
    is_paid = Column(Boolean, index=True)
