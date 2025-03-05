from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.model import Product
from faker import Faker
import random

fake = Faker()

def seed_data():
    db: Session = next(get_db())

    # Xóa dữ liệu cũ (nếu cần)
    db.query(Product).delete()

    for _ in range(100):
        product = Product(
            name=fake.word().capitalize(),
            category=fake.random_element([
                "Electronics", "Clothing", "Food", "Toys", "Furniture",
                "Books", "Beauty", "Sports", "Automotive"
            ]),
            colors=[fake.color_name() for _ in range(random.randint(1, 3))],
            price=round(random.uniform(100, 500), 2)
        )
        db.add(product)

    db.commit()
    db.close()
    print("Sinh dữ liệu thành công!")

if __name__ == "__main__":
    seed_data()
