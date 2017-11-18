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
             price="$2000", url="https://www.amazon.com/ASUS-ROG-G752VS-XB78K-17-3-Inch-i7-6820HK/dp/B01K1JW3PO/ref=sr_1_3?s=pc&ie=UTF8&qid=1511044114&sr=1-3&keywords=asus+rog", ctg_id=1, user_id=1)
session.add(item1)
session.commit()

#Item 2
item2 = Item(title="Acer Computer", description="Mid Range Computer tower!",
             price="$1000", url="https://www.amazon.com/Acer-Performance-Dual-Core-Processor-Refurbished/dp/B07489YZ9T/ref=sr_1_7?s=electronics&ie=UTF8&qid=1511044132&sr=1-7&keywords=acer+computer", ctg_id=1, user_id=1)
session.add(item2)
session.commit()

#Item 3
item3 = Item(title="Alienware Laptop", description="Top gaming laptop from the future!",
             price="$2500", url="https://www.amazon.com/Alienware-AW17R4-7352SLV-PUS-Laptop-Generation-256SSD/dp/B01N0THPHM/ref=sr_1_2?s=electronics&ie=UTF8&qid=1511044148&sr=1-2&keywords=alienware+laptop", ctg_id=1, user_id=1)
session.add(item3)
session.commit()

# Create 2nd Tech Category
cat1 = Categories(ctg_id=2, name="Smartphones and Tablets")
session.add(cat1)
session.commit()

# Create Items for this Category

#Item 1
item1 = Item(title="iPhone X", description="The newest iPhone 2017!",
             price="$1358", url="https://www.amazon.com/Apple-iPhone-Fully-Unlocked-5-8/dp/B075QN8NDH/ref=sr_1_3?s=electronics&ie=UTF8&qid=1511044174&sr=1-3&keywords=iphone+x", ctg_id=2, user_id=1)
session.add(item1)
session.commit()

#Item 2
item2 = Item(title="Google Pixel 2", description="New Smartphone from Google!",
             price="$850", url="https://www.amazon.com/Google-Pixel-Unlocked-128gb-CDMA/dp/B0766HPGYP/ref=sr_1_4?s=electronics&ie=UTF8&qid=1511044217&sr=1-4&keywords=google+pixel+2", ctg_id=2, user_id=1)
session.add(item2)
session.commit()

#Item 3
item3 = Item(title="Amazon Fire HD 10", description="Top Tablet from Amazon!",
             price="$229", url="https://www.amazon.com/Amazon-Fire-HD-10-10-Inch-Tablet-16GB-Black/dp/B00VKIY9RG/ref=sr_1_1?s=electronics&ie=UTF8&qid=1511044242&sr=1-1&keywords=amazon+fire+hd+10", ctg_id=2, user_id=1)
session.add(item3)
session.commit()

# Create 3rd Tech Category
cat1 = Categories(ctg_id=3, name="Games and Movies")
session.add(cat1)
session.commit()

# Create Items for this Category

#Item 1
item1 = Item(title="Skyrim VR", description="The latest skyrim game in VR",
             price="$69", url="https://www.amazon.com/Elder-Scrolls-Skyrim-PS4-PlayStation-4/dp/B0773TKQLG/ref=sr_1_cc_7?s=aps&ie=UTF8&qid=1511044260&sr=1-7-catcorr&keywords=skyrim+vr", ctg_id=3, user_id=1)
session.add(item1)
session.commit()

#Item 2
item2 = Item(title="Hunger Games", description="The first movie of Hunger Games",
             price="$7", url="https://www.amazon.com/Hunger-Games-Jennifer-Lawrence/dp/B008Y7N7JW/ref=sr_1_3?ie=UTF8&qid=1511044300&sr=8-3&keywords=hunger+games+movie", ctg_id=3, user_id=1)
session.add(item2)
session.commit()

#Item 3
item3 = Item(title="Cuphead", description="The latest hit game!",
             price="$19", url="https://www.amazon.com/Cuphead-Xbox-Windows-Digital-Code/dp/B073ZR63P8/ref=sr_1_1?ie=UTF8&qid=1511044326&sr=8-1&keywords=cuphead", ctg_id=3, user_id=1)
session.add(item3)
session.commit()

print "Populated Database Successfully!"
