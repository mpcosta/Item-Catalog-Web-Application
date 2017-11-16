from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Categories, Base, Item, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create Dummy User
user1 = User(name="John Snow", email="johnSnow@winterfell.com",
             picture='http://www.animationxpress.com/wp-content/uploads/2015/11/Jon-Snow.jpg')
session.add(user1)
session.commit()

# Create 1st Tech Category
cat1 = Categories(ctg_id=1, name="Computers and Laptops")
session.add(cat1)
session.commit()

# Create Items for this Category

#Item 1
item1 = Item(title="Asus Laptop", description="An Asus Laptop, top of the range!",
             price="$2000", ctg_id=1, user_id=1)
session.add(item1)
session.commit()

#Item 2
item2 = Item(title="Acer Computer", description="Mid Range Computer tower!",
             price="$1000", ctg_id=1, user_id=1)
session.add(item2)
session.commit()

#Item 3
item3 = Item(title="Alienware Laptop", description="Top gaming laptop from the future!",
             price="$4500", ctg_id=1, user_id=1)
session.add(item3)
session.commit()

# Create 2nd Tech Category
cat1 = Categories(ctg_id=2, name="Smartphones and Tablets")
session.add(cat1)
session.commit()

# Create Items for this Category

#Item 1
item1 = Item(title="iPhone X", description="The newest iPhone 2017!",
             price="$1000", ctg_id=2, user_id=1)
session.add(item1)
session.commit()

#Item 2
item2 = Item(title="Google Pixel 2", description="New Smartphone from Google!",
             price="$850", ctg_id=2, user_id=1)
session.add(item2)
session.commit()

#Item 3
item3 = Item(title="Amazon Fire HD 10", description="Top Tablet from Amazon!",
             price="$200", ctg_id=2, user_id=1)
session.add(item3)
session.commit()

# Create 3rd Tech Category
cat1 = Categories(ctg_id=3, name="Games and Movies")
session.add(cat1)
session.commit()

# Create Items for this Category

#Item 1
item1 = Item(title="Skyrim VR", description="The latest skyrim game in VR",
             price="$65", ctg_id=3, user_id=1)
session.add(item1)
session.commit()

#Item 2
item2 = Item(title="Hunger Games", description="The first movie of Hunger Games",
             price="$30", ctg_id=3, user_id=1)
session.add(item2)
session.commit()

#Item 3
item3 = Item(title="Cuphead", description="The latest hit game!",
             price="$45", ctg_id=3, user_id=1)
session.add(item3)
session.commit()

print "Populated Database Successfully!"
