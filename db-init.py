# library imports
import sqlalchemy as sa
from sqlalchemy import URL
from datetime import datetime

# local imports
from constants.databaseURL import DATABASE_URL
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
from auth import get_password_hash

db = sa.create_engine(DATABASE_URL)
Session = sa.orm.sessionmaker(bind=db)
Base = sa.orm.declarative_base()

def main() -> None:
    print("Dropping tables")
    Review.metadata.drop_all(db)
    UserEventRelation.metadata.drop_all(db)
    Event.metadata.drop_all(db)
    OrderProductRelation.metadata.drop_all(db)
    Order.metadata.drop_all(db)
    Product.metadata.drop_all(db)
    NewCategoryRequest.metadata.drop_all(db)
    ProductCategory.metadata.drop_all(db)
    Farmer.metadata.drop_all(db)
    User.metadata.drop_all(db)

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
        session.add_all([
            # Admin
            User(name="John", surname="Doe", isAdmin=True, email="jd@gmail.com", password=get_password_hash("password"), phone="+421908111222", state="Slovenská republika", city="Bratislava", street="Mlynské nivy", streetNumber="45", zipCode="821 09"),
            # Moderator
            User(name="Emma", surname="Smith", isModerator=True, email="es@gmail.com", password=get_password_hash("password"), phone="+421908111223", state="Slovenská republika", city="Košice", street="Hlavná", streetNumber="1", zipCode="040 01"),
            # Farmers
            User(name="Sophia", surname="Williams", email="sw@gmail.com", password=get_password_hash("password"), phone="+420777111222", state="Česká republika", city="Brno", street="Náměstí Svobody", streetNumber="1", zipCode="602 00"),
            User(name="Amanda", surname="Welth", email="aw@gmail.com", password=get_password_hash("password"), phone="+420778111222", state="Česká republika", city="Brno", street="Česká", streetNumber="8", zipCode="602 00"),
            User(name="Michael", surname="Johnson", email="mj@gmail.com", password=get_password_hash("password"), phone="+420777111221", state="Česká republika", city="Brno", street="Koliště", streetNumber="8", zipCode="602 00"),
            # Customer
            User(name="James", surname="Brown", email="jb@gmail.com", password=get_password_hash("password"), phone="+420777111223", state="Česká republika", city="Praha", street="Václavské náměstí", streetNumber="1", zipCode="110 00"),
            # Inactive user
            User(name="Olivia", surname="Davis", isActive=False, email="od@gmail.com", password=get_password_hash("password"), phone="+420777111224", state="Česká republika", city="Ostrava", street="Masarykovo náměstí", streetNumber="1", zipCode="702 00"),
        ])
        session.commit()

        print("Inserting farmers")
        sophia = session.query(User).filter_by(email="sw@gmail.com").one()
        amanda = session.query(User).filter_by(email="aw@gmail.com").one()
        michael = session.query(User).filter_by(email="mj@gmail.com").one()
        session.add_all([
            Farmer(userId=sophia.id, farmName="Sophia's Farm", description="We are a small family farm located in the heart of Brno. We grow a variety of vegetables and fruits and we are proud to offer our customers the freshest produce.", CIN="12345680", VATIN="CZ12345680", VAT="CZ12345678", paysVat=True, bankCode="125", accountNumber="1234567892", state="Česká republika", city="Brno", street="Haškova", streetNumber="1", zipCode="602 00"),
            Farmer(userId=amanda.id, farmName="Amanda's Farm", description="We are a small family farm located in the heart of Brno. We grow a variety of vegetables and fruits and we are proud to offer our customers the freshest produce.", CIN="12345681", VATIN="CZ12345681", VAT="CZ12345679", paysVat=True, bankCode="126", accountNumber="1234567893", state="Česká republika", city="Brno", street="Haškova", streetNumber="2", zipCode="602 00"),
            Farmer(userId=michael.id, farmName="Michael's Farm", description="We are a small family farm located in the heart of Brno. We grow a variety of vegetables and fruits and we are proud to offer our customers the freshest produce.", CIN="12345682", VATIN="CZ12345682", VAT="CZ12345680", paysVat=True, bankCode="127", accountNumber="1234567894", state="Česká republika", city="Brno", street="Haškova", streetNumber="3", zipCode="602 00"),
        ])
        session.commit()

        print("Updating users with farmerId")
        sophiasFarm = session.query(Farmer).filter_by(userId=sophia.id).one()
        amandasFarm = session.query(Farmer).filter_by(farmName="Amanda's Farm").one()
        michaelsFarm = session.query(Farmer).filter_by(farmName="Michael's Farm").one()
        sophia.farmerId = sophiasFarm.id
        amanda.farmerId = amandasFarm.id
        michael.farmerId = michaelsFarm.id
        sophia.isFarmer = True
        amanda.isFarmer = True
        michael.isFarmer = True
        session.add_all([sophia, amanda, michael])
        session.commit()

        print("Inserting categories")
        vegetables = ProductCategory(name="Vegetables")
        fruits = ProductCategory(name="Fruits")
        session.add_all([vegetables, fruits])
        session.commit()

        print("Inserting sub categories")
        vegetables = session.query(ProductCategory).filter_by(name="Vegetables").one()
        fruits = session.query(ProductCategory).filter_by(name="Fruits").one()
        session.add_all([
            ProductCategory(name="Leafy", parentCategoryId=vegetables.id),
            ProductCategory(name="Root", parentCategoryId=vegetables.id),
            ProductCategory(name="Citrus", parentCategoryId=fruits.id),
            ProductCategory(name="Berry", parentCategoryId=fruits.id),
        ])
        session.commit()

        print("Inserting sub sub categories")
        leafy = session.query(ProductCategory).filter_by(name="Leafy").one()
        root = session.query(ProductCategory).filter_by(name="Root").one()
        citrus = session.query(ProductCategory).filter_by(name="Citrus").one()
        berry = session.query(ProductCategory).filter_by(name="Berry").one()
        session.add_all([
            ProductCategory(name="Spinach", parentCategoryId=leafy.id, atributes="[{\"name\":\"only Leaves\",\"type\":\"boolean\",\"isRequired\":false},{\"name\":\"is baby\",\"type\":\"boolean\",\"isRequired\":false}]"),
            ProductCategory(name="Kale", parentCategoryId=leafy.id, atributes="[{\"name\":\"weight in kg\",\"type\":\"number\",\"isRequired\":true},{\"name\":\"is BIO\",\"type\":\"boolean\",\"isRequired\":false}]"),
            ProductCategory(name="Carrot", parentCategoryId=root.id, atributes="[{\"name\":\"length in cm\",\"type\":\"number\",\"isRequired\":false},{\"name\":\"is BIO\",\"type\":\"boolean\",\"isRequired\":true}]"),
            ProductCategory(name="Beetroot", parentCategoryId=root.id, atributes="[{\"name\":\"weight in kg\",\"type\":\"number\",\"isRequired\":true},{\"name\":\"is BIO\",\"type\":\"boolean\",\"isRequired\":false}]"),
            ProductCategory(name="Orange", parentCategoryId=citrus.id, atributes="[{\"name\":\"diameter in mm\",\"type\":\"number\",\"isRequired\":true},{\"name\":\"is BIO\",\"type\":\"boolean\",\"isRequired\":false}]"),
            ProductCategory(name="Lemon", parentCategoryId=citrus.id, atributes="[{\"name\":\"weight in kg\",\"type\":\"number\",\"isRequired\":true},{\"name\":\"color\",\"type\":\"text\",\"isRequired\":false}]"),
            ProductCategory(name="Strawberry", parentCategoryId=berry.id, atributes="[{\"name\":\"Country of origin\",\"type\":\"text\",\"isRequired\":true},{\"name\":\"is BIO\",\"type\":\"boolean\",\"isRequired\":false},{\"name\":\"number in package\",\"type\":\"number\",\"isRequired\":true}]"),
            ProductCategory(name="Blueberry", parentCategoryId=berry.id, atributes="[{\"name\":\"weight in kg\",\"type\":\"number\",\"isRequired\":false}]"),
        ])
        session.commit()

        print("Inserting new category requests")
        session.add_all([
            NewCategoryRequest(newCategoryName="Cucumber", parentCategoryId=vegetables.id, createdById=sophia.id, atributes="[{\"name\":\"pickled\",\"type\":\"boolean\",\"isRequired\":false}]"),
            NewCategoryRequest(newCategoryName="Apple", parentCategoryId=fruits.id, createdById=amanda.id, atributes="[{\"name\":\"color\",\"type\":\"text\",\"isRequired\":true}]"),
        ])
        session.commit()

        print("Inserting products")
        session.add_all([
            #Sophia's products
            Product(name="Spinach Frans Hubert", imageUrl="https://plus.unsplash.com/premium_photo-1701699718915-49b72f1a4b47?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fHNwaW5hY2h8ZW58MHx8MHx8fDA%3D", unit=Unit.KILOGRAM, unitPrice=2.5, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Spinach").one().id, farmerId=sophiasFarm.id, categoryAtributes="[{\"name\":\"only Leaves\",\"value\":true},{\"name\":\"is baby\",\"value\":true}]"),
            Product(name="Kale Marionet", imageUrl="https://plus.unsplash.com/premium_photo-1702286619432-740a9d5e3ff0?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8a2FsZXxlbnwwfHwwfHx8MA%3D%3D", unit=Unit.KILOGRAM, unitPrice=3.5, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Kale").one().id, farmerId=sophiasFarm.id, categoryAtributes="[{\"name\":\"weight in kg\",\"value\":1.5},{\"name\":\"is BIO\",\"value\":true}]"),
            Product(name="Carrot Nantes", imageUrl="https://images.unsplash.com/photo-1445282768818-728615cc910a?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGNhcnJvdHxlbnwwfHwwfHx8MA%3D%3D", unit=Unit.PIECE, unitPrice=1.5, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Carrot").one().id, farmerId=sophiasFarm.id, categoryAtributes="[{\"name\":\"length in cm\",\"value\":20},{\"name\":\"is BIO\",\"value\":true}]"),
            Product(name="Beetroot Detroit", imageUrl="https://images.unsplash.com/photo-1627738668643-1c166aecbf3d?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTV8fGJlZXRyb290fGVufDB8fDB8fHww", unit=Unit.PIECE, unitPrice=1.8, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Beetroot").one().id, farmerId=sophiasFarm.id, categoryAtributes="[{\"name\":\"weight in kg\",\"value\":0.5},{\"name\":\"is BIO\",\"value\":false}]"),
            Product(name="Orange Jazz", imageUrl="https://images.unsplash.com/photo-1517161782303-6bee363b9d9a?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8b3Jhbmdlc3xlbnwwfHwwfHx8MA%3D%3D", unit=Unit.PIECE, unitPrice=0.9, stock=200, categoryId=session.query(ProductCategory).filter_by(name="Orange").one().id, farmerId=sophiasFarm.id, categoryAtributes="[{\"name\":\"diameter in mm\",\"value\":80},{\"name\":\"is BIO\",\"value\":false}]"),
            Product(name="Lemon Elton", imageUrl="https://images.unsplash.com/photo-1498060059232-54fd57716ac6?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8bGVtb25zfGVufDB8fDB8fHww", unit=Unit.PIECE, unitPrice=0.5, stock=150, categoryId=session.query(ProductCategory).filter_by(name="Lemon").one().id, farmerId=sophiasFarm.id, categoryAtributes="[{\"name\":\"weight in kg\",\"value\":0.1},{\"name\":\"color\",\"value\":\"yellow\"}]"),
            Product(name="Strawberry Sweet Charlie", imageUrl="https://images.unsplash.com/photo-1543528176-61b239494933?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8c3RyYXdiZXJyaWVzfGVufDB8fDB8fHww", unit=Unit.KILOGRAM, unitPrice=6.0, stock=40, categoryId=session.query(ProductCategory).filter_by(name="Strawberry").one().id, farmerId=sophiasFarm.id, categoryAtributes="[{\"name\":\"Country of origin\",\"value\":\"Czech Republic\"},{\"name\":\"is BIO\",\"value\":false},{\"name\":\"number in package\",\"value\":250}]"),
            Product(name="Blueberry Bluecrop", imageUrl="https://images.unsplash.com/photo-1498557850523-fd3d118b962e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Ymx1ZWJlcnJpZXN8ZW58MHx8MHx8fDA%3D", unit=Unit.KILOGRAM, unitPrice=8.0, stock=30, categoryId=session.query(ProductCategory).filter_by(name="Blueberry").one().id, farmerId=sophiasFarm.id, categoryAtributes="[{\"name\":\"weight in kg\",\"value\":0.25}]"),
            #Amanda's products with different atributes
            Product(name="Spanish Spinach", imageUrl="https://plus.unsplash.com/premium_photo-1701699718915-49b72f1a4b47?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fHNwaW5hY2h8ZW58MHx8MHx8fDA%3D", unit=Unit.KILOGRAM, unitPrice=2.7, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Spinach").one().id, farmerId=amandasFarm.id, categoryAtributes="[{\"name\":\"only Leaves\",\"value\":false},{\"name\":\"is baby\",\"value\":true}]"),
            Product(name="Glorious Kale", imageUrl="https://plus.unsplash.com/premium_photo-1702286619432-740a9d5e3ff0?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8a2FsZXxlbnwwfHwwfHx8MA%3D%3D", unit=Unit.KILOGRAM,  unitPrice=3.8, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Kale").one().id, farmerId=amandasFarm.id, categoryAtributes="[{\"name\":\"weight in kg\",\"value\":1.2},{\"name\":\"is BIO\",\"value\":true}]"),
            Product(name="Cute Carrot", imageUrl="https://images.unsplash.com/photo-1445282768818-728615cc910a?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGNhcnJvdHxlbnwwfHwwfHx8MA%3D%3D", unit=Unit.PIECE, unitPrice=1.6, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Carrot").one().id, farmerId=amandasFarm.id, categoryAtributes="[{\"name\":\"length in cm\",\"value\":18},{\"name\":\"is BIO\",\"value\":false}]"),
            Product(name="Beige Beetroot", imageUrl="https://images.unsplash.com/photo-1627738668643-1c166aecbf3d?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTV8fGJlZXRyb290fGVufDB8fDB8fHww", unit=Unit.PIECE, unitPrice=2.0, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Beetroot").one().id, farmerId=amandasFarm.id, categoryAtributes="[{\"name\":\"weight in kg\",\"value\":0.6},{\"name\":\"is BIO\",\"value\":false}]"),      
            Product(name="Omnious Orange", imageUrl="https://images.unsplash.com/photo-1517161782303-6bee363b9d9a?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8b3Jhbmdlc3xlbnwwfHwwfHx8MA%3D%3D", unit=Unit.PIECE, unitPrice=1.0, stock=200, categoryId=session.query(ProductCategory).filter_by(name="Orange").one().id, farmerId=amandasFarm.id, categoryAtributes="[{\"name\":\"diameter in mm\",\"value\":85},{\"name\":\"is BIO\",\"value\":true}]"),   
            Product(name="Lazy Lemon", imageUrl="https://images.unsplash.com/photo-1498060059232-54fd57716ac6?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8bGVtb25zfGVufDB8fDB8fHww", unit=Unit.PIECE, unitPrice=0.6, stock=150, categoryId=session.query(ProductCategory).filter_by(name="Lemon").one().id, farmerId=amandasFarm.id, categoryAtributes="[{\"name\":\"weight in kg\",\"value\":0.12},{\"name\":\"color\",\"value\":\"bright yellow\"}]"),
            Product(name="Sweet Strawberry", imageUrl="https://images.unsplash.com/photo-1543528176-61b239494933?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8c3RyYXdiZXJyaWVzfGVufDB8fDB8fHww", unit=Unit.KILOGRAM, unitPrice=6.5, stock=40, categoryId=session.query(ProductCategory).filter_by(name="Strawberry").one().id, farmerId=amandasFarm.id, categoryAtributes="[{\"name\":\"Country of origin\",\"value\":\"France\"},{\"name\":\"is BIO\",\"value\":true},{\"name\":\"number in package\",\"value\":300}]"),
            Product(name="Barbarous Blueberry", imageUrl="https://images.unsplash.com/photo-1498557850523-fd3d118b962e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Ymx1ZWJlcnJpZXN8ZW58MHx8MHx8fDA%3D", unit=Unit.KILOGRAM, unitPrice=7.8, stock=30, categoryId=session.query(ProductCategory).filter_by(name="Blueberry").one().id, farmerId=amandasFarm.id, categoryAtributes="[{\"name\":\"weight in kg\",\"value\":0.3}]"),
            #Michael's products
            Product(name="Spinach", imageUrl="https://plus.unsplash.com/premium_photo-1701699718915-49b72f1a4b47?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fHNwaW5hY2h8ZW58MHx8MHx8fDA%3D", unit=Unit.KILOGRAM, unitPrice=2.7, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Spinach").one().id, farmerId=michaelsFarm.id, categoryAtributes="[{\"name\":\"only Leaves\",\"value\":false},{\"name\":\"is baby\",\"value\":false}]"),
            Product(name="Kale", imageUrl="https://plus.unsplash.com/premium_photo-1702286619432-740a9d5e3ff0?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8a2FsZXxlbnwwfHwwfHx8MA%3D%3D", unit=Unit.KILOGRAM,  unitPrice=3.8, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Kale").one().id, farmerId=michaelsFarm.id, categoryAtributes="[{\"name\":\"weight in kg\",\"value\":2.2},{\"name\":\"is BIO\",\"value\":true}]"),
            Product(name="Carrot", imageUrl="https://images.unsplash.com/photo-1445282768818-728615cc910a?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGNhcnJvdHxlbnwwfHwwfHx8MA%3D%3D", unit=Unit.PIECE, unitPrice=1.6, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Carrot").one().id, farmerId=michaelsFarm.id, categoryAtributes="[{\"name\":\"length in cm\",\"value\":15},{\"name\":\"is BIO\",\"value\":true}]"),
            Product(name="Beetroot", imageUrl="https://images.unsplash.com/photo-1627738668643-1c166aecbf3d?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTV8fGJlZXRyb290fGVufDB8fDB8fHww", unit=Unit.PIECE, unitPrice=2.0, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Beetroot").one().id, farmerId=michaelsFarm.id, categoryAtributes="[{\"name\":\"weight in kg\",\"value\":0.5},{\"name\":\"is BIO\",\"value\":true}]"),      
            Product(name="Orange", imageUrl="https://images.unsplash.com/photo-1517161782303-6bee363b9d9a?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8b3Jhbmdlc3xlbnwwfHwwfHx8MA%3D%3D", unit=Unit.PIECE, unitPrice=1.0, stock=200, categoryId=session.query(ProductCategory).filter_by(name="Orange").one().id, farmerId=michaelsFarm.id, categoryAtributes="[{\"name\":\"diameter in mm\",\"value\":81},{\"name\":\"is BIO\",\"value\":true}]"),   
            Product(name="Lemon", imageUrl="https://images.unsplash.com/photo-1498060059232-54fd57716ac6?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8bGVtb25zfGVufDB8fDB8fHww", unit=Unit.PIECE, unitPrice=0.6, stock=150, categoryId=session.query(ProductCategory).filter_by(name="Lemon").one().id, farmerId=michaelsFarm.id, categoryAtributes="[{\"name\":\"weight in kg\",\"value\":0.22},{\"name\":\"color\",\"value\":\"yellow\"}]"),
            Product(name="Strawberry", imageUrl="https://images.unsplash.com/photo-1543528176-61b239494933?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8c3RyYXdiZXJyaWVzfGVufDB8fDB8fHww", unit=Unit.KILOGRAM, unitPrice=6.5, stock=40, categoryId=session.query(ProductCategory).filter_by(name="Strawberry").one().id, farmerId=michaelsFarm.id, categoryAtributes="[{\"name\":\"Country of origin\",\"value\":\"France\"},{\"name\":\"is BIO\",\"value\":false},{\"name\":\"number in package\",\"value\":200}]"),
            Product(name="Blueberry", imageUrl="https://images.unsplash.com/photo-1498557850523-fd3d118b962e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Ymx1ZWJlcnJpZXN8ZW58MHx8MHx8fDA%3D", unit=Unit.KILOGRAM, unitPrice=7.8, stock=30, categoryId=session.query(ProductCategory).filter_by(name="Blueberry").one().id, farmerId=michaelsFarm.id, categoryAtributes="[{\"name\":\"weight in kg\",\"value\":0.7}]"),
            
        ])
        session.commit()

        print("Inserting orders")
        james = session.query(User).filter_by(email="jb@gmail.com").one()
        session.add_all([
            Order(orderNumber="ORD-001", userId=james.id, farmerId=sophiasFarm.id, createdAt=datetime.timestamp(datetime.strptime("2021-10-01 10:00", "%Y-%m-%d %H:%M")), status="SUPPLIED"),
            Order(orderNumber="ORD-002", userId=james.id, farmerId=sophiasFarm.id, createdAt=datetime.timestamp(datetime.strptime("2024-10-02 12:30", "%Y-%m-%d %H:%M")), status="SUPPLIED"),
            Order(orderNumber="ORD-003", userId=james.id, farmerId=amandasFarm.id, createdAt=datetime.timestamp(datetime.strptime("2024-10-03 12:30", "%Y-%m-%d %H:%M")), status="IN_CART"),
        ])
        session.commit()

        print("Inserting order product relations")
        order1 = session.query(Order).filter_by(orderNumber="ORD-001").one()
        order2 = session.query(Order).filter_by(orderNumber="ORD-002").one()
        order3 = session.query(Order).filter_by(orderNumber="ORD-003").one()
        sophiasOranges = session.query(Product).filter_by(name="Orange Jazz").one()
        sophiasStrawberries = session.query(Product).filter_by(name="Strawberry Sweet Charlie").one()
        sophiasLemons = session.query(Product).filter_by(name="Lemon Elton").one()
        amandasSpinach = session.query(Product).filter_by(name="Spanish Spinach").one()
        amandasKale = session.query(Product).filter_by(name="Glorious Kale").one()
        session.add_all([
            # Order 1
            OrderProductRelation(orderId=order1.id, productId=sophiasOranges.id, quantity=2),
            OrderProductRelation(orderId=order1.id, productId=sophiasStrawberries.id, quantity=1),
            OrderProductRelation(orderId=order1.id, productId=sophiasLemons.id, quantity=3),
            # Order 2
            OrderProductRelation(orderId=order2.id, productId=sophiasOranges.id, quantity=3),
            OrderProductRelation(orderId=order2.id, productId=sophiasStrawberries.id, quantity=2),
            OrderProductRelation(orderId=order2.id, productId=sophiasLemons.id, quantity=4),
            # Order 3
            OrderProductRelation(orderId=order3.id, productId=amandasSpinach.id, quantity=2),
            OrderProductRelation(orderId=order3.id, productId=amandasKale.id, quantity=3),

        ])
        session.commit()

        print("Inserting events")
        session.add_all([
            Event(name="Old Farmers Market", description="Join us at the farmers market to buy fresh produce directly from the farmers.", startDate=datetime.timestamp(datetime.strptime("2024-10-01 12:30", "%Y-%m-%d %H:%M")), endDate=datetime.timestamp(datetime.strptime("2024-10-03 20:00", "%Y-%m-%d %H:%M")), createdById=sophiasFarm.id, createdAt=datetime.timestamp(datetime.strptime("2024-09-01 11:00", "%Y-%m-%d %H:%M")), state="Slovenská republika", city="Bratislava", street="Vajnorská", streetNumber="100", zipCode="831 04"),
            Event(name="New Farmers Market", description="Join us at the farmers market to buy fresh produce directly from the farmers.", startDate=datetime.timestamp(datetime.strptime("2024-12-01 12:30", "%Y-%m-%d %H:%M")), endDate=datetime.timestamp(datetime.strptime("2024-12-03 20:00", "%Y-%m-%d %H:%M")), createdById=amandasFarm.id, createdAt=datetime.timestamp(datetime.strptime("2024-09-01 11:00", "%Y-%m-%d %H:%M")), state="Slovenská republika", city="Košice", street="Orlia", streetNumber="1", zipCode="040 01"),
            Event(name="Green Market", description="Join us at the farmers market to buy fresh produce directly from the farmers.", startDate=datetime.timestamp(datetime.strptime("2025-10-01 12:30", "%Y-%m-%d %H:%M")), endDate=datetime.timestamp(datetime.strptime("2025-10-03 20:00", "%Y-%m-%d %H:%M")), createdById=michaelsFarm.id, createdAt=datetime.timestamp(datetime.strptime("2025-09-01 11:00", "%Y-%m-%d %H:%M")), state="Česká republika", city="Brno", street="Haškova", streetNumber="1", zipCode="602 00"),
        ])
        session.commit()

        print("Inserting user event relations")        
        event1 = session.query(Event).filter_by(name="Old Farmers Market").one()
        event2 = session.query(Event).filter_by(name="New Farmers Market").one()
        session.add_all([
            UserEventRelation(userId=james.id, eventId=event1.id),
            UserEventRelation(userId=james.id, eventId=event2.id),
        ])
        session.commit()
        
        print("Inserting reviews")
        session.add_all([
            Review(userId=james.id, orderId=order1.id, productId=sophiasOranges.id, rating=5, createdAt=datetime.timestamp(datetime.strptime("2021-10-01 11:00", "%Y-%m-%d %H:%M"))),
            Review(userId=james.id, orderId=order1.id, productId=sophiasStrawberries.id, rating=4, createdAt=datetime.timestamp(datetime.strptime("2021-10-01 11:00", "%Y-%m-%d %H:%M"))),
            Review(userId=james.id, orderId=order1.id, productId=sophiasLemons.id, rating=4, createdAt=datetime.timestamp(datetime.strptime("2021-10-01 11:00", "%Y-%m-%d %H:%M"))),
            Review(userId=james.id, orderId=order2.id, productId=sophiasOranges.id, rating=2, createdAt=datetime.timestamp(datetime.strptime("2024-10-02 13:00", "%Y-%m-%d %H:%M"))),
            Review(userId=james.id, orderId=order2.id, productId=sophiasStrawberries.id, rating=1, createdAt=datetime.timestamp(datetime.strptime("2024-10-02 13:00", "%Y-%m-%d %H:%M"))),
            Review(userId=james.id, orderId=order2.id, productId=sophiasLemons.id, rating=3, createdAt=datetime.timestamp(datetime.strptime("2024-10-02 13:00", "%Y-%m-%d %H:%M"))),
        ])
        session.commit()
        
        print("Demo data inserted")

if __name__ == "__main__":
    main()