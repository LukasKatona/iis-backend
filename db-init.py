import sqlalchemy as sa
from sqlalchemy import URL
from entities.Product import ProductCategoryORM, ProductORM

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
    ProductORM.metadata.drop_all(db)
    ProductCategoryORM.metadata.drop_all(db)
    print("Creating tables")
    ProductORM.metadata.create_all(db)
    ProductCategoryORM.metadata.create_all(db)
    print("Inserting demo data")
    vegetables = ProductCategoryORM(name="Vegetables")
    fruits = ProductCategoryORM(name="Fruits")

    with Session() as session:
        session.add_all([vegetables, fruits])
        session.commit()
        print("Demo data inserted")

if __name__ == "__main__":
    main()