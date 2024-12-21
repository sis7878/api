import time
from flask import Flask
from models import db, Pizza
from routes import pizza_bp
from config import Config
import random

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(pizza_bp, url_prefix='/api/pizza')

    return app

def generate_test_data(app, num_records):
    """Generate test data for Pizza table."""
    with app.app_context():
        for _ in range(num_records):
            pizza = Pizza(
                name=f'Pizza {random.randint(1, 1000000)}',
                description=f'Description for Pizza {random.randint(1, 1000000)}',
                price=random.uniform(5, 20)
            )
            db.session.add(pizza)
        db.session.commit()

def measure_query_performance(app, num_records):
    """Measure performance of SELECT, INSERT, UPDATE, DELETE queries."""
    print(f"Measuring performance for {num_records} records...")

    start_time = time.time()
    generate_test_data(app, num_records)
    insert_time = time.time() - start_time
    print(f"INSERT took {insert_time:.5f} seconds")

    start_time = time.time()
    with app.app_context():
        pizzas = Pizza.query.filter(Pizza.name.like('%Pizza%')).all() 
    select_time = time.time() - start_time
    print(f"SELECT took {select_time:.5f} seconds")

    start_time = time.time()
    with app.app_context():
        pizza = Pizza.query.filter_by(name='Pizza 1').first()  
        if pizza:
            pizza.price += 1
            db.session.commit()
    update_time = time.time() - start_time
    print(f"UPDATE took {update_time:.5f} seconds")

    start_time = time.time()
    with app.app_context():
        pizza_to_delete = Pizza.query.filter_by(name='Pizza 1').first()  
        if pizza_to_delete:
            db.session.delete(pizza_to_delete)
            db.session.commit()
    delete_time = time.time() - start_time
    print(f"DELETE took {delete_time:.5f} seconds")

    return insert_time, select_time, update_time, delete_time

if __name__ == "__main__":
    app = create_app()

    record_sizes = [1000, 10000, 100000]

    for num_records in record_sizes:
        insert_time, select_time, update_time, delete_time = measure_query_performance(app, num_records)
        print(f"\nResults for {num_records} records:")
        print(f"INSERT time: {insert_time:.5f}s")
        print(f"SELECT time: {select_time:.5f}s")
        print(f"UPDATE time: {update_time:.5f}s")
        print(f"DELETE time: {delete_time:.5f}s\n")

    app.run(debug=True)
