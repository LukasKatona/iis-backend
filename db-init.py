import sqlalchemy as sa
from sqlalchemy import URL
from entities.Product import ProductCategory, Product

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
    print("Inserting demo data")
    vegetables = ProductCategory(name="Vegetables")
    fruits = ProductCategory(name="Fruits")

    with Session() as session:
        session.add_all([vegetables, fruits])
        session.commit()
        print("Demo data inserted")

if __name__ == "__main__":
    main()