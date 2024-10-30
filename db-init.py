# library imports
import sqlalchemy as sa
from sqlalchemy import URL

# local imports
from entities.Product import Product
from entities.ProductCategory import ProductCategory
from entities.User import User
from entities.UserEventRelation import UserEventRelation
from entities.Event import Event
from entities.Farmer import Farmer
from entities.Order import Order
from entities.OrderProductRelation import OrderProductRelation
from entities.Review import Review
from entities.NewCategoryRequest import NewCategoryRequest
from enums.Unit import Unit

connection_string = URL.create(
    'postgresql',
    username='admin',
    password='pgtvTuwoV5G7',
    host='ep-wild-mode-a2zrk2og.eu-central-1.pg.koyeb.app',
    database='koyebdb',
)

db = sa.create_engine(connection_string)
Session = sa.orm.sessionmaker(bind=db)
Base = sa.orm.declarative_base()

def main() -> None:
    print("Dropping tables")

    User.metadata.drop_all(db)
    Farmer.metadata.drop_all(db)

    ProductCategory.metadata.drop_all(db)
    NewCategoryRequest.metadata.drop_all(db)

    Product.metadata.drop_all(db)
    Order.metadata.drop_all(db)
    OrderProductRelation.metadata.drop_all(db)

    Event.metadata.drop_all(db)
    UserEventRelation.metadata.drop_all(db)

    Review.metadata.drop_all(db)

    print("Creating tables")

    User.metadata.create_all(db)
    Farmer.metadata.create_all(db)

    ProductCategory.metadata.create_all(db)
    NewCategoryRequest.metadata.create_all(db)

    Product.metadata.create_all(db)
    Order.metadata.create_all(db)
    OrderProductRelation.metadata.create_all(db)

    Event.metadata.create_all(db)
    UserEventRelation.metadata.create_all(db)

    Review.metadata.create_all(db)
    
    with Session() as session:
        print("Inserting users")
        



































        print("Inserting categories")
        vegetables = ProductCategory(name="Vegetables")
        fruits = ProductCategory(name="Fruits")
        session.add_all([vegetables, fruits])
        session.commit()

        print("Inserting sub categories")
        vegetables = session.query(ProductCategory).filter_by(name="Vegetables").first()
        fruits = session.query(ProductCategory).filter_by(name="Fruits").first()
        session.add_all([
            ProductCategory(name="Leafy", parentCategoryId=vegetables.id),
            ProductCategory(name="Root", parentCategoryId=vegetables.id),
            ProductCategory(name="Podded", parentCategoryId=vegetables.id),
            ProductCategory(name="Citrus", parentCategoryId=fruits.id),
            ProductCategory(name="Berry", parentCategoryId=fruits.id),
            ProductCategory(name="Melon", parentCategoryId=fruits.id),
        ])
        session.commit()

        print("Inserting sub sub categories")
        leafy = session.query(ProductCategory).filter_by(name="Leafy").first()
        root = session.query(ProductCategory).filter_by(name="Root").first()
        podded = session.query(ProductCategory).filter_by(name="Podded").first()
        citrus = session.query(ProductCategory).filter_by(name="Citrus").first()
        berry = session.query(ProductCategory).filter_by(name="Berry").first()
        melon = session.query(ProductCategory).filter_by(name="Melon").first()
        session.add_all([
            ProductCategory(name="Spinach", parentCategoryId=leafy.id),
            ProductCategory(name="Kale", parentCategoryId=leafy.id),
            ProductCategory(name="Carrot", parentCategoryId=root.id),
            ProductCategory(name="Beetroot", parentCategoryId=root.id),
            ProductCategory(name="Peas", parentCategoryId=podded.id),
            ProductCategory(name="Beans", parentCategoryId=podded.id),
            ProductCategory(name="Orange", parentCategoryId=citrus.id),
            ProductCategory(name="Lemon", parentCategoryId=citrus.id),
            ProductCategory(name="Strawberry", parentCategoryId=berry.id),
            ProductCategory(name="Blueberry", parentCategoryId=berry.id),
            ProductCategory(name="Watermelon", parentCategoryId=melon.id),
            ProductCategory(name="Honeydew", parentCategoryId=melon.id),
        ])
        session.commit()

        print("Inserting products")
        session.add_all([
            Product(name="Spinach", imageUrl="https://plus.unsplash.com/premium_photo-1701699718915-49b72f1a4b47?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fHNwaW5hY2h8ZW58MHx8MHx8fDA%3D", unit=Unit.KILOGRAM, unitPrice=2.5, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Spinach").first().id),
            Product(name="Kale", imageUrl="https://plus.unsplash.com/premium_photo-1702286619432-740a9d5e3ff0?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8a2FsZXxlbnwwfHwwfHx8MA%3D%3D", unit=Unit.KILOGRAM, unitPrice=3.5, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Kale").first().id),
            Product(name="Carrot", imageUrl="https://images.unsplash.com/photo-1445282768818-728615cc910a?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGNhcnJvdHxlbnwwfHwwfHx8MA%3D%3D", unit=Unit.PIECE, unitPrice=1.5, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Carrot").first().id),
            Product(name="Beetroot", imageUrl="https://images.unsplash.com/photo-1627738668643-1c166aecbf3d?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTV8fGJlZXRyb290fGVufDB8fDB8fHww", unit=Unit.PIECE, unitPrice=1.8, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Beetroot").first().id),
            Product(name="Peas", imageUrl="https://images.unsplash.com/photo-1668548205372-1becd11b5641?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8cGVhc3xlbnwwfHwwfHx8MA%3D%3D", unit=Unit.KILOGRAM, unitPrice=4.0, stock=50, categoryId=session.query(ProductCategory).filter_by(name="Peas").first().id),
            Product(name="Beans", imageUrl="https://images.unsplash.com/photo-1506620780696-e5cb6c54524e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTV8fGJlYW5zfGVufDB8fDB8fHww", unit=Unit.KILOGRAM, unitPrice=3.8, stock=60, categoryId=session.query(ProductCategory).filter_by(name="Beans").first().id),
            Product(name="Orange", imageUrl="https://images.unsplash.com/photo-1517161782303-6bee363b9d9a?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8b3Jhbmdlc3xlbnwwfHwwfHx8MA%3D%3D", unit=Unit.PIECE, unitPrice=0.9, stock=200, categoryId=session.query(ProductCategory).filter_by(name="Orange").first().id),
            Product(name="Lemon", imageUrl="https://images.unsplash.com/photo-1498060059232-54fd57716ac6?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8bGVtb25zfGVufDB8fDB8fHww", unit=Unit.PIECE, unitPrice=0.5, stock=150, categoryId=session.query(ProductCategory).filter_by(name="Lemon").first().id),
            Product(name="Strawberry", imageUrl="https://images.unsplash.com/photo-1543528176-61b239494933?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8c3RyYXdiZXJyaWVzfGVufDB8fDB8fHww", unit=Unit.KILOGRAM, unitPrice=6.0, stock=40, categoryId=session.query(ProductCategory).filter_by(name="Strawberry").first().id),
            Product(name="Blueberry", imageUrl="https://images.unsplash.com/photo-1498557850523-fd3d118b962e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Ymx1ZWJlcnJpZXN8ZW58MHx8MHx8fDA%3D", unit=Unit.KILOGRAM, unitPrice=8.0, stock=30, categoryId=session.query(ProductCategory).filter_by(name="Blueberry").first().id),
            Product(name="Watermelon", imageUrl="https://plus.unsplash.com/premium_photo-1663855531381-f9c100b3c48f?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8d2F0ZXJtZWxvbnxlbnwwfHwwfHx8MA%3D%3D", unit=Unit.PIECE, unitPrice=3.0, stock=25, categoryId=session.query(ProductCategory).filter_by(name="Watermelon").first().id),
            Product(name="Honeydew", imageUrl="https://images.unsplash.com/photo-1623125489492-6d3641414e37?q=80&w=1740&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", unit=Unit.PIECE, unitPrice=3.2, stock=20, categoryId=session.query(ProductCategory).filter_by(name="Honeydew").first().id),
        ])
        session.commit()

        print("Demo data inserted")

if __name__ == "__main__":
    main()