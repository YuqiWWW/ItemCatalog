from models import Base, Item, Category
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import json

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

cs = session.query(Category).all()
for c in cs:
    session.delete(c)
    session.commit()
items = session.query(Item).all()
for i in items:
    session.delete(i)
    session.commit()

c = Category(id = 1, name = "Snowboarding")
session.add(c)
session.commit()
i = Item(name = "Snowboard", description = "Best for any terrain and conditions. All-mountain snowboards perform anywhere on a mountain groomed runs...", 
         category_id = 1)
session.add(i)
session.commit()

