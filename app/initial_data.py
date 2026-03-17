from decimal import Decimal

from sqlalchemy import select, func

from app.database import SessionLocal
from app.models import Restaurant, MenuItem


def seed_data():
    db = SessionLocal()
    try:
        count = db.execute(select(func.count(Restaurant.id))).scalar_one()
        if count == 0:
            restaurant1 = Restaurant(
                name="Bangkok Spice",
                address="123 Sukhumvit Rd, Bangkok",
                phone="+66-2-123-4567",
                opening_hours="10:00 - 22:00",
            )
            restaurant2 = Restaurant(
                name="Chiang Mai Garden",
                address="45 Old City Rd, Chiang Mai",
                phone="+66-53-765-4321",
                opening_hours="11:00 - 23:00",
            )
            db.add_all([restaurant1, restaurant2])
            db.flush()

            items = [
                MenuItem(
                    name="Tom Yum Goong",
                    description="Spicy Thai shrimp soup",
                    price=Decimal("150.00"),
                    category="appetizer",
                    is_available=True,
                    restaurant_id=restaurant1.id,
                ),
                MenuItem(
                    name="Pad Thai",
                    description="Stir-fried rice noodles with shrimp",
                    price=Decimal("180.00"),
                    category="main",
                    is_available=True,
                    restaurant_id=restaurant1.id,
                ),
                MenuItem(
                    name="Green Curry",
                    description="Chicken green curry with coconut milk",
                    price=Decimal("190.00"),
                    category="main",
                    is_available=True,
                    restaurant_id=restaurant1.id,
                ),
                MenuItem(
                    name="Mango Sticky Rice",
                    description="Sweet mango with sticky rice",
                    price=Decimal("120.00"),
                    category="dessert",
                    is_available=True,
                    restaurant_id=restaurant1.id,
                ),
                MenuItem(
                    name="Thai Iced Tea",
                    description="Sweet iced tea with milk",
                    price=Decimal("80.00"),
                    category="drink",
                    is_available=True,
                    restaurant_id=restaurant1.id,
                ),
                MenuItem(
                    name="Khao Soi",
                    description="Northern Thai curry noodle soup",
                    price=Decimal("170.00"),
                    category="main",
                    is_available=True,
                    restaurant_id=restaurant2.id,
                ),
                MenuItem(
                    name="Sai Ua",
                    description="Chiang Mai spicy sausage",
                    price=Decimal("140.00"),
                    category="appetizer",
                    is_available=True,
                    restaurant_id=restaurant2.id,
                ),
                MenuItem(
                    name="Nam Prik Ong",
                    description="Northern Thai chili dip with pork",
                    price=Decimal("130.00"),
                    category="appetizer",
                    is_available=True,
                    restaurant_id=restaurant2.id,
                ),
                MenuItem(
                    name="Coconut Ice Cream",
                    description="Homemade coconut ice cream",
                    price=Decimal("90.00"),
                    category="dessert",
                    is_available=True,
                    restaurant_id=restaurant2.id,
                ),
                MenuItem(
                    name="Lemongrass Tea",
                    description="Hot lemongrass herbal tea",
                    price=Decimal("70.00"),
                    category="drink",
                    is_available=True,
                    restaurant_id=restaurant2.id,
                ),
            ]
            db.add_all(items)
            db.commit()
    finally:
        db.close()

