# library imports
import sqlalchemy as sa
from sqlalchemy import URL

# local imports
from entities.Address import Address
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
    Address.metadata.drop_all(db)

    print("Creating tables")
    Address.metadata.create_all(db)
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
        print("Inserting addresses")
        session.add_all([
            Address(state="Slovenská republika", city="Bratislava", street="Mlynské nivy", streetNumber="45", zipCode="821 09"),
            Address(state="Slovenská republika", city="Bratislava", street="Miletičova", streetNumber="1", zipCode="821 08"),
            Address(state="Slovenská republika", city="Bratislava", street="Špitálska", streetNumber="24", zipCode="811 08"),
            Address(state="Česká republika", city="Brno", street="Kounicova", streetNumber="65", zipCode="602 00"),
            Address(state="Česká republika", city="Brno", street="Veveří", streetNumber="113", zipCode="602 00"),
            Address(state="Česká republika", city="Brno", street="Pekařská", streetNumber="11", zipCode="602 00"),
        ])
        session.commit()

        print("Inserting users")
        address1 = session.query(Address).filter_by(street="Mlynské nivy").first()
        address2 = session.query(Address).filter_by(street="Miletičova").first()
        address3 = session.query(Address).filter_by(street="Špitálska").first()
        address4 = session.query(Address).filter_by(street="Kounicova").first()
        address5 = session.query(Address).filter_by(street="Veveří").first()
        address6 = session.query(Address).filter_by(street="Pekařská").first()
        session.add_all([
            User(name="John", surname="Doe", email="jd@gmail.com", password="password", phone="+421908111222", addressId=address1.id),
            User(name="Emma", surname="Smith", email="es@gmail.com", password="password", phone="+421908111223", addressId=address2.id),
            User(name="Michael", surname="Johnson", email="mj@gmail.com", password="password", phone="+421908111224", addressId=address3.id),
            User(name="Sophia", surname="Williams", email="sw@gmail.com", password="password", phone="+420777111222", addressId=address4.id),
            User(name="James", surname="Brown", email="jb@gmail.com", password="password", phone="+420777111223", addressId=address5.id),
            User(name="Olivia", surname="Davis", email="od@gmail.com", password="password", phone="+420777111224", addressId=address6.id),
        ])
        session.commit()

        print("Inserting farmers")
        user1 = session.query(User).filter_by(name="John").first()
        user2 = session.query(User).filter_by(name="Emma").first()
        user3 = session.query(User).filter_by(name="Sophia").first()
        session.add_all([
            Farmer(userId=user1.id, farmName="John's Farm", description="We are a small family farm located in the heart of Bratislava. We grow a variety of vegetables and fruits and we are proud to offer our customers the freshest produce.", CIN="12345678", VATIN="12345678", VAT="SK12345678", paysVat=True, bankCode="123", accountNumber="1234567890", billingAddressId=address1.id),
            Farmer(userId=user2.id, farmName="Emma's Farm", description="We are a small family farm located in the heart of Bratislava. We grow a variety of vegetables and fruits and we are proud to offer our customers the freshest produce.", CIN="12345679", VATIN="12345679", VAT="SK12345679", paysVat=True, bankCode="124", accountNumber="1234567891", billingAddressId=address2.id),
            Farmer(userId=user3.id, farmName="Sophia's Farm", description="We are a small family farm located in the heart of Brno. We grow a variety of vegetables and fruits and we are proud to offer our customers the freshest produce.", CIN="12345680", VATIN="CZ12345680", VAT="CZ12345678", paysVat=True, bankCode="125", accountNumber="1234567892", billingAddressId=address4.id),
        ])
        session.commit()

        print("Updating users with farmerId")
        farmer1 = session.query(Farmer).filter_by(farmName="John's Farm").first()
        farmer2 = session.query(Farmer).filter_by(farmName="Emma's Farm").first()
        farmer3 = session.query(Farmer).filter_by(farmName="Sophia's Farm").first()
        user1.farmerId = farmer1.id
        user2.farmerId = farmer2.id
        user3.farmerId = farmer3.id
        session.add_all([user1, user2, user3])
        session.commit()

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

        print("Inserting new category requests")
        user4 = session.query(User).filter_by(name="Michael").first()
        user5 = session.query(User).filter_by(name="James").first()
        user6 = session.query(User).filter_by(name="Olivia").first()
        session.add_all([
            NewCategoryRequest(newCategoryName="Pumpkin", parentCategoryId=melon.id, createdById=user4.id),
            NewCategoryRequest(newCategoryName="Cucumber", parentCategoryId=vegetables.id, createdById=user5.id),
            NewCategoryRequest(newCategoryName="Flower", createdById=user6.id),
        ])
        session.commit()

        print("Inserting products")
        session.add_all([
            Product(name="Spinach", imageUrl="https://plus.unsplash.com/premium_photo-1701699718915-49b72f1a4b47?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fHNwaW5hY2h8ZW58MHx8MHx8fDA%3D", unit=Unit.KILOGRAM, unitPrice=2.5, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Spinach").first().id, farmerId=farmer1.id),
            Product(name="Kale", imageUrl="https://plus.unsplash.com/premium_photo-1702286619432-740a9d5e3ff0?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8a2FsZXxlbnwwfHwwfHx8MA%3D%3D", unit=Unit.KILOGRAM, unitPrice=3.5, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Kale").first().id, farmerId=farmer1.id),
            Product(name="Carrot", imageUrl="https://images.unsplash.com/photo-1445282768818-728615cc910a?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGNhcnJvdHxlbnwwfHwwfHx8MA%3D%3D", unit=Unit.PIECE, unitPrice=1.5, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Carrot").first().id, farmerId=farmer1.id),
            Product(name="Beetroot", imageUrl="https://images.unsplash.com/photo-1627738668643-1c166aecbf3d?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTV8fGJlZXRyb290fGVufDB8fDB8fHww", unit=Unit.PIECE, unitPrice=1.8, stock=100, categoryId=session.query(ProductCategory).filter_by(name="Beetroot").first().id, farmerId=farmer1.id),
            Product(name="Peas", imageUrl="https://images.unsplash.com/photo-1668548205372-1becd11b5641?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8cGVhc3xlbnwwfHwwfHx8MA%3D%3D", unit=Unit.KILOGRAM, unitPrice=4.0, stock=50, categoryId=session.query(ProductCategory).filter_by(name="Peas").first().id, farmerId=farmer2.id),
            Product(name="Beans", imageUrl="https://images.unsplash.com/photo-1506620780696-e5cb6c54524e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTV8fGJlYW5zfGVufDB8fDB8fHww", unit=Unit.KILOGRAM, unitPrice=3.8, stock=60, categoryId=session.query(ProductCategory).filter_by(name="Beans").first().id, farmerId=farmer2.id),
            Product(name="Orange", imageUrl="https://images.unsplash.com/photo-1517161782303-6bee363b9d9a?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8b3Jhbmdlc3xlbnwwfHwwfHx8MA%3D%3D", unit=Unit.PIECE, unitPrice=0.9, stock=200, categoryId=session.query(ProductCategory).filter_by(name="Orange").first().id, farmerId=farmer2.id),
            Product(name="Lemon", imageUrl="https://images.unsplash.com/photo-1498060059232-54fd57716ac6?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8bGVtb25zfGVufDB8fDB8fHww", unit=Unit.PIECE, unitPrice=0.5, stock=150, categoryId=session.query(ProductCategory).filter_by(name="Lemon").first().id, farmerId=farmer2.id),
            Product(name="Strawberry", imageUrl="https://images.unsplash.com/photo-1543528176-61b239494933?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8c3RyYXdiZXJyaWVzfGVufDB8fDB8fHww", unit=Unit.KILOGRAM, unitPrice=6.0, stock=40, categoryId=session.query(ProductCategory).filter_by(name="Strawberry").first().id, farmerId=farmer3.id),
            Product(name="Blueberry", imageUrl="https://images.unsplash.com/photo-1498557850523-fd3d118b962e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Ymx1ZWJlcnJpZXN8ZW58MHx8MHx8fDA%3D", unit=Unit.KILOGRAM, unitPrice=8.0, stock=30, categoryId=session.query(ProductCategory).filter_by(name="Blueberry").first().id, farmerId=farmer3.id),
            Product(name="Watermelon", imageUrl="https://plus.unsplash.com/premium_photo-1663855531381-f9c100b3c48f?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8d2F0ZXJtZWxvbnxlbnwwfHwwfHx8MA%3D%3D", unit=Unit.PIECE, unitPrice=3.0, stock=25, categoryId=session.query(ProductCategory).filter_by(name="Watermelon").first().id, farmerId=farmer3.id),
            Product(name="Honeydew", imageUrl="https://images.unsplash.com/photo-1623125489492-6d3641414e37?q=80&w=1740&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", unit=Unit.PIECE, unitPrice=3.2, stock=20, categoryId=session.query(ProductCategory).filter_by(name="Honeydew").first().id, farmerId=farmer3.id),
        ])
        session.commit()

        print("Inserting orders")
        user1 = session.query(User).filter_by(name="James").first()
        user2 = session.query(User).filter_by(name="Olivia").first()
        user3 = session.query(User).filter_by(name="Michael").first()
        farmer1 = session.query(Farmer).filter_by(farmName="John's Farm").first()
        farmer2 = session.query(Farmer).filter_by(farmName="Emma's Farm").first()
        session.add_all([
            Order(orderNumber="ORD-001", userId=user1.id, farmerId=farmer1.id, createdAt="2021-10-01", status="ACCEPTED"),
            Order(orderNumber="ORD-002", userId=user2.id, farmerId=farmer2.id, createdAt="2021-10-02", status="ACCEPTED"),
            Order(orderNumber="ORD-003", userId=user3.id, farmerId=farmer1.id, createdAt="2021-10-03", status="ACCEPTED"),
            Order(orderNumber="ORD-004", userId=user1.id, farmerId=farmer2.id, createdAt="2021-10-04", status="ACCEPTED"),
        ])
        session.commit()

        print("Inserting order product relations")
        order1 = session.query(Order).filter_by(orderNumber="ORD-001").first()
        order2 = session.query(Order).filter_by(orderNumber="ORD-002").first()
        order3 = session.query(Order).filter_by(orderNumber="ORD-003").first()
        order4 = session.query(Order).filter_by(orderNumber="ORD-004").first()
        product1 = session.query(Product).filter_by(name="Spinach").first()
        product2 = session.query(Product).filter_by(name="Kale").first()
        product3 = session.query(Product).filter_by(name="Carrot").first()
        product4 = session.query(Product).filter_by(name="Beetroot").first()
        product5 = session.query(Product).filter_by(name="Peas").first()
        product6 = session.query(Product).filter_by(name="Beans").first()
        product7 = session.query(Product).filter_by(name="Orange").first()
        product8 = session.query(Product).filter_by(name="Lemon").first()
        product9 = session.query(Product).filter_by(name="Strawberry").first()
        product10 = session.query(Product).filter_by(name="Blueberry").first()
        session.add_all([
            OrderProductRelation(orderId=order1.id, productId=product1.id, quantity=2),
            OrderProductRelation(orderId=order1.id, productId=product2.id, quantity=1),
            OrderProductRelation(orderId=order2.id, productId=product3.id, quantity=3),
            OrderProductRelation(orderId=order2.id, productId=product4.id, quantity=2),
            OrderProductRelation(orderId=order3.id, productId=product5.id, quantity=1),
            OrderProductRelation(orderId=order3.id, productId=product6.id, quantity=2),
            OrderProductRelation(orderId=order4.id, productId=product7.id, quantity=3),
            OrderProductRelation(orderId=order4.id, productId=product8.id, quantity=2),
            OrderProductRelation(orderId=order4.id, productId=product9.id, quantity=1),
            OrderProductRelation(orderId=order4.id, productId=product10.id, quantity=2),
        ])
        session.commit()

        print("Inserting events")
        farmer1 = session.query(Farmer).filter_by(farmName="John's Farm").first()
        farmer2 = session.query(Farmer).filter_by(farmName="Emma's Farm").first()
        farmer3 = session.query(Farmer).filter_by(farmName="Sophia's Farm").first()
        session.add_all([
            Event(name="Farmers Market", description="Join us at the farmers market to buy fresh produce directly from the farmers.", startDate="2024-10-01", endDate="2024-10-03", createdById=farmer1.id, createdAt="2024-09-01", addressId=address1.id),
            Event(name="Farmers Market", description="Join us at the farmers market to buy fresh produce directly from the farmers.", startDate="2024-12-01", endDate="2024-12-03", createdById=farmer2.id, createdAt="2024-09-01", addressId=address2.id),
            Event(name="Farmers Market", description="Join us at the farmers market to buy fresh produce directly from the farmers.", startDate="2025-10-01", endDate="2025-10-03", createdById=farmer3.id, createdAt="2025-09-01", addressId=address4.id),
        ])
        session.commit()

        print("Inserting user event relations")
        user1 = session.query(User).filter_by(name="James").first()
        user2 = session.query(User).filter_by(name="Olivia").first()
        user3 = session.query(User).filter_by(name="Michael").first()
        event1 = session.query(Event).filter_by(name="Farmers Market").first()
        event2 = session.query(Event).filter_by(name="Farmers Market").first()
        event3 = session.query(Event).filter_by(name="Farmers Market").first()
        session.add_all([
            UserEventRelation(userId=user1.id, eventId=event1.id),
            UserEventRelation(userId=user2.id, eventId=event2.id),
            UserEventRelation(userId=user3.id, eventId=event3.id),
            UserEventRelation(userId=user1.id, eventId=event2.id),
            UserEventRelation(userId=user1.id, eventId=event3.id),
        ])
        session.commit()
        
        print("Inserting reviews")
        user1 = session.query(User).filter_by(name="James").first()
        user2 = session.query(User).filter_by(name="Olivia").first()
        user3 = session.query(User).filter_by(name="Michael").first()
        product1 = session.query(Product).filter_by(name="Spinach").first()
        product2 = session.query(Product).filter_by(name="Kale").first()
        product3 = session.query(Product).filter_by(name="Carrot").first()
        product4 = session.query(Product).filter_by(name="Beetroot").first()
        product5 = session.query(Product).filter_by(name="Peas").first()
        order1 = session.query(Order).filter_by(orderNumber="ORD-001").first()
        order2 = session.query(Order).filter_by(orderNumber="ORD-002").first()
        order3 = session.query(Order).filter_by(orderNumber="ORD-003").first()
        order4 = session.query(Order).filter_by(orderNumber="ORD-004").first()
        session.add_all([
            Review(userId=user1.id, productId=product1.id, rating=5, review="Great product!", createdAt="2021-10-01"),
            Review(userId=user1.id, productId=product2.id, rating=4, review="Good product!", createdAt="2021-10-01"),
            Review(userId=user2.id, productId=product3.id, rating=3, review="Average product!", createdAt="2021-10-02"),
            Review(userId=user2.id, productId=product4.id, rating=2, review="Not so good product!", createdAt="2021-10-02"),
            Review(userId=user3.id, productId=product5.id, rating=1, review="Bad product!", createdAt="2021-10-03"),
            Review(userId=user3.id, productId=product6.id, rating=5, review="Great product!", createdAt="2021-10-03"),
            Review(userId=user1.id, orderId=order1.id, rating=4, review="Good service!", createdAt="2021-10-01"),
            Review(userId=user1.id, orderId=order2.id, rating=3, review="Average service!", createdAt="2021-10-01"),
            Review(userId=user2.id, orderId=order3.id, rating=2, review="Not so good service!", createdAt="2021-10-02"),
            Review(userId=user2.id, orderId=order4.id, rating=1, review="Bad service!", createdAt="2021-10-02"),
        ])
        session.commit()
        
        print("Demo data inserted")

if __name__ == "__main__":
    main()