# library imports
import sqlalchemy as sa
from sqlalchemy import URL

# local imports
from entities.Product import Product
from entities.ProductCategory import ProductCategory
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
            Product(name="Spinach", imageUrl="https://unsplash.com/photos/a-bunch-of-green-leaves-with-drops-of-water-on-them-Um2DgUUxIn4", unit=Unit.KILOGRAM, unitPrice=2.5, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Spinach").first().id),
            Product(name="Kale", imageUrl="https://unsplash.com/photos/a-bunch-of-green-leafy-vegetables-with-drops-of-water-on-them-fQcn2rbmkIA", unit=Unit.KILOGRAM, unitPrice=3.5, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Kale").first().id),
            Product(name="Carrot", imageUrl="https://unsplash.com/photos/carrots-on-table-eFFnKMiDMGc", unit=Unit.PIECE, unitPrice=1.5, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Carrot").first().id),
            Product(name="Beetroot", imageUrl="https://unsplash.com/photos/onion-on-white-plate-TmjyLCUpcDY", unit=Unit.PIECE, unitPrice=1.8, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Beetroot").first().id),
            Product(name="Peas", imageUrl="https://unsplash.com/photos/a-pink-plate-filled-with-green-beans-and-peas-hf0esLbFAMA", unit=Unit.KILOGRAM, unitPrice=4.0, stock=50, categoryId=session.query(ProductCategory).filter_by(name="Peas").first().id),
            Product(name="Beans", imageUrl="https://unsplash.com/photos/a-pile-of-red-beans-sitting-next-to-each-other-dU9CwN0CD6I", unit=Unit.KILOGRAM, unitPrice=3.8, stock=60, categoryId=session.query(ProductCategory).filter_by(name="Beans").first().id),
            Product(name="Orange", imageUrl="https://unsplash.com/photos/orange-fruit-in-brown-basket-QI5nFAUXWvM", unit=Unit.PIECE, unitPrice=0.9, stock=200, categoryId=session.query(ProductCategory).filter_by(name="Orange").first().id),
            Product(name="Lemon", imageUrl="https://unsplash.com/photos/bunch-of-lemons-on-wooden-rack-7woHBtwCgTQ", unit=Unit.PIECE, unitPrice=0.5, stock=150, categoryId=session.query(ProductCategory).filter_by(name="Lemon").first().id),
            Product(name="Strawberry", imageUrl="https://unsplash.com/photos/red-raspberries-IeEFsajuORc", unit=Unit.KILOGRAM, unitPrice=6.0, stock=40, categoryId=session.query(ProductCategory).filter_by(name="Strawberry").first().id),
            Product(name="Blueberry", imageUrl="https://unsplash.com/photos/blueberries-on-white-ceramic-container-4qujjbj3srs", unit=Unit.KILOGRAM, unitPrice=8.0, stock=30, categoryId=session.query(ProductCategory).filter_by(name="Blueberry").first().id),
            Product(name="Watermelon", imageUrl="https://unsplash.com/photos/three-slices-of-watermelon-on-a-cutting-board-cDcXinZpW7Q", unit=Unit.PIECE, unitPrice=3.0, stock=25, categoryId=session.query(ProductCategory).filter_by(name="Watermelon").first().id),
            Product(name="Honeydew", imageUrl="https://unsplash.com/photos/a-cut-in-half-kiwi-fruit-on-a-purple-and-pink-background-ZtyIiKna9I0", unit=Unit.PIECE, unitPrice=3.2, stock=20, categoryId=session.query(ProductCategory).filter_by(name="Honeydew").first().id),

        ])
        session.commit()

        print("Demo data inserted")

if __name__ == "__main__":
    main()