import sqlalchemy as sa
from sqlalchemy import URL
from entities.Product import Product
from entities.ProductCategory import ProductCategory

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
    Product.metadata.drop_all(db)
    ProductCategory.metadata.drop_all(db)
    print("Creating tables")
    Product.metadata.create_all(db)
    ProductCategory.metadata.create_all(db)
    

    with Session() as session:
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
            Product(name="Spinach", imageUrl="https://images.unsplash.com/photo-1601750624501-0b1b0b1b1b1b", unit="kg", unitPrice=2.5, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Spinach").first().id),
            Product(name="Kale", imageUrl="https://images.unsplash.com/photo-1601750624501-0b1b0b1b1b1b", unit="kg", unitPrice=3.5, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Kale").first().id),
            Product(name="Carrot", imageUrl="https://images.unsplash.com/photo-1601750624501-0b1b0b1b1b1b", unit="kg", unitPrice=1.5, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Carrot").first().id),
        ])

        print("Demo data inserted")

if __name__ == "__main__":
    main()