import pymysql
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

class DatabaseConnection:
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306):
        self.config = {
            'charset': 'utf8mb4',
            'connect_timeout': 10,
            'cursorclass': pymysql.cursors.DictCursor,
            'db': database,
            'host': host,
            'password': password,
            'read_timeout': 10,
            'port': port,
            'user': user,
            'write_timeout': 10
        }
    
    @contextmanager
    def get_connection(self):
        conn = pymysql.connect(**self.config)
        try:
            yield conn
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = None, fetch: bool = False):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            conn.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return last_id

class AdminOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, username: str, password: str, email: str, address: str = None, phoneno: str = None):
        query = "INSERT INTO Admin (username, password, email, address, phoneno) VALUES (%s, %s, %s, %s, %s)"
        return self.db.execute_query(query, (username, password, email, address, phoneno))
    
    def read_all(self):
        return self.db.execute_query("SELECT * FROM Admin ORDER BY id", fetch=True)
    
    def read_by_id(self, admin_id: int):
        result = self.db.execute_query("SELECT * FROM Admin WHERE id = %s", (admin_id,), fetch=True)
        return result[0] if result else None
    
    def update(self, admin_id: int, username: str = None, password: str = None, email: str = None, address: str = None, phoneno: str = None):
        admin = self.read_by_id(admin_id)
        if not admin:
            return False
        query = "UPDATE Admin SET username = %s, password = %s, email = %s, address = %s, phoneno = %s WHERE id = %s"
        params = (
            username or admin['username'],
            password or admin['password'],
            email or admin['email'],
            address if address is not None else admin['address'],
            phoneno if phoneno is not None else admin['phoneno'],
            admin_id
        )
        self.db.execute_query(query, params)
        return True
    
    def delete(self, admin_id: int):
        self.db.execute_query("DELETE FROM Admin WHERE id = %s", (admin_id,))

class RestaurantOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, name: str, address: str = None, opening_hours: str = None, admin_id: int = None):
        query = "INSERT INTO Restaurant (name, address, openingHours, admin_id) VALUES (%s, %s, %s, %s)"
        return self.db.execute_query(query, (name, address, opening_hours, admin_id))
    
    def read_all(self):
        query = """
            SELECT r.*, a.username as admin_username 
            FROM Restaurant r 
            LEFT JOIN Admin a ON r.admin_id = a.id 
            ORDER BY r.id
        """
        return self.db.execute_query(query, fetch=True)
    
    def read_by_id(self, restaurant_id: int):
        query = """
            SELECT r.*, a.username as admin_username 
            FROM Restaurant r 
            LEFT JOIN Admin a ON r.admin_id = a.id 
            WHERE r.id = %s
        """
        result = self.db.execute_query(query, (restaurant_id,), fetch=True)
        return result[0] if result else None
    
    def update(self, restaurant_id: int, name: str = None, address: str = None, opening_hours: str = None, admin_id: int = None):
        restaurant = self.read_by_id(restaurant_id)
        if not restaurant:
            return False
        query = "UPDATE Restaurant SET name = %s, address = %s, openingHours = %s, admin_id = %s WHERE id = %s"
        params = (
            name or restaurant['name'],
            address if address is not None else restaurant['address'],
            opening_hours if opening_hours is not None else restaurant['openingHours'],
            admin_id if admin_id is not None else restaurant['admin_id'],
            restaurant_id
        )
        self.db.execute_query(query, params)
        return True
    
    def delete(self, restaurant_id: int):
        self.db.execute_query("DELETE FROM Restaurant WHERE id = %s", (restaurant_id,))

class FoodOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, name: str, ingredients: str = None, category: str = None, is_non_veg: bool = False, admin_id: int = None):
        query = "INSERT INTO Food (name, ingredients, category, isNonVeg, admin_id) VALUES (%s, %s, %s, %s, %s)"
        return self.db.execute_query(query, (name, ingredients, category, is_non_veg, admin_id))
    
    def read_all(self):
        query = """
            SELECT f.*, a.username as prepared_by 
            FROM Food f 
            LEFT JOIN Admin a ON f.admin_id = a.id 
            ORDER BY f.id
        """
        return self.db.execute_query(query, fetch=True)
    
    def read_by_id(self, food_id: int):
        query = """
            SELECT f.*, a.username as prepared_by 
            FROM Food f 
            LEFT JOIN Admin a ON f.admin_id = a.id 
            WHERE f.id = %s
        """
        result = self.db.execute_query(query, (food_id,), fetch=True)
        return result[0] if result else None
    
    def update(self, food_id: int, name: str = None, ingredients: str = None, category: str = None, is_non_veg: bool = None, admin_id: int = None):
        food = self.read_by_id(food_id)
        if not food:
            return False
        query = "UPDATE Food SET name = %s, ingredients = %s, category = %s, isNonVeg = %s, admin_id = %s WHERE id = %s"
        params = (
            name or food['name'],
            ingredients if ingredients is not None else food['ingredients'],
            category if category is not None else food['category'],
            is_non_veg if is_non_veg is not None else food['isNonVeg'],
            admin_id if admin_id is not None else food['admin_id'],
            food_id
        )
        self.db.execute_query(query, params)
        return True
    
    def delete(self, food_id: int):
        self.db.execute_query("DELETE FROM Food WHERE id = %s", (food_id,))

class CustomerOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, username: str, password: str, email: str, address: str = None, phoneno: str = None):
        query = "INSERT INTO Customer (username, password, email, address, phoneno) VALUES (%s, %s, %s, %s, %s)"
        return self.db.execute_query(query, (username, password, email, address, phoneno))
    
    def read_all(self):
        return self.db.execute_query("SELECT * FROM Customer ORDER BY id", fetch=True)
    
    def read_by_id(self, customer_id: int):
        result = self.db.execute_query("SELECT * FROM Customer WHERE id = %s", (customer_id,), fetch=True)
        return result[0] if result else None
    
    def update(self, customer_id: int, username: str = None, password: str = None, email: str = None, address: str = None, phoneno: str = None):
        customer = self.read_by_id(customer_id)
        if not customer:
            return False
        query = "UPDATE Customer SET username = %s, password = %s, email = %s, address = %s, phoneno = %s WHERE id = %s"
        params = (
            username or customer['username'],
            password or customer['password'],
            email or customer['email'],
            address if address is not None else customer['address'],
            phoneno if phoneno is not None else customer['phoneno'],
            customer_id
        )
        self.db.execute_query(query, params)
        return True
    
    def delete(self, customer_id: int):
        self.db.execute_query("DELETE FROM Customer WHERE id = %s", (customer_id,))

class PaymentOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, type: str, price: float, customer_id: int):
        query = "INSERT INTO Payment (type, price, customer_id) VALUES (%s, %s, %s)"
        return self.db.execute_query(query, (type, price, customer_id))
    
    def read_all(self):
        query = """
            SELECT p.*, c.username as customer_username 
            FROM Payment p 
            LEFT JOIN Customer c ON p.customer_id = c.id 
            ORDER BY p.id
        """
        return self.db.execute_query(query, fetch=True)
    
    def read_by_id(self, payment_id: int):
        query = """
            SELECT p.*, c.username as customer_username 
            FROM Payment p 
            LEFT JOIN Customer c ON p.customer_id = c.id 
            WHERE p.id = %s
        """
        result = self.db.execute_query(query, (payment_id,), fetch=True)
        return result[0] if result else None
    
    def update(self, payment_id: int, type: str = None, price: float = None, customer_id: int = None):
        payment = self.read_by_id(payment_id)
        if not payment:
            return False
        query = "UPDATE Payment SET type = %s, price = %s, customer_id = %s WHERE id = %s"
        params = (
            type or payment['type'],
            price if price is not None else payment['price'],
            customer_id if customer_id is not None else payment['customer_id'],
            payment_id
        )
        self.db.execute_query(query, params)
        return True
    
    def delete(self, payment_id: int):
        self.db.execute_query("DELETE FROM Payment WHERE id = %s", (payment_id,))

class OrderOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, price: float, customer_id: int, restaurant_id: int, payment_id: int = None, address: str = None):
        query = "INSERT INTO `Order` (price, address, customer_id, restaurant_id, payment_id) VALUES (%s, %s, %s, %s, %s)"
        return self.db.execute_query(query, (price, address, customer_id, restaurant_id, payment_id))
    
    def read_all(self):
        query = """
            SELECT o.*, c.username as customer_username, r.name as restaurant_name, p.type as payment_type
            FROM `Order` o
            LEFT JOIN Customer c ON o.customer_id = c.id
            LEFT JOIN Restaurant r ON o.restaurant_id = r.id
            LEFT JOIN Payment p ON o.payment_id = p.id
            ORDER BY o.id
        """
        return self.db.execute_query(query, fetch=True)
    
    def read_by_id(self, order_id: int):
        query = """
            SELECT o.*, c.username as customer_username, r.name as restaurant_name, p.type as payment_type
            FROM `Order` o
            LEFT JOIN Customer c ON o.customer_id = c.id
            LEFT JOIN Restaurant r ON o.restaurant_id = r.id
            LEFT JOIN Payment p ON o.payment_id = p.id
            WHERE o.id = %s
        """
        result = self.db.execute_query(query, (order_id,), fetch=True)
        return result[0] if result else None
    
    def update(self, order_id: int, price: float = None, customer_id: int = None, restaurant_id: int = None, payment_id: int = None, address: str = None):
        order = self.read_by_id(order_id)
        if not order:
            return False
        query = "UPDATE `Order` SET price = %s, address = %s, customer_id = %s, restaurant_id = %s, payment_id = %s WHERE id = %s"
        params = (
            price if price is not None else order['price'],
            address if address is not None else order['address'],
            customer_id if customer_id is not None else order['customer_id'],
            restaurant_id if restaurant_id is not None else order['restaurant_id'],
            payment_id if payment_id is not None else order['payment_id'],
            order_id
        )
        self.db.execute_query(query, params)
        return True
    
    def delete(self, order_id: int):
        self.db.execute_query("DELETE FROM `Order` WHERE id = %s", (order_id,))
    
    def add_food(self, order_id: int, food_id: int, quantity: int = 1):
        query = "INSERT INTO OrderFood (order_id, food_id, quantity) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE quantity = %s"
        self.db.execute_query(query, (order_id, food_id, quantity, quantity))
    
    def remove_food(self, order_id: int, food_id: int):
        self.db.execute_query("DELETE FROM OrderFood WHERE order_id = %s AND food_id = %s", (order_id, food_id))
    
    def get_order_foods(self, order_id: int):
        query = """
            SELECT f.*, of.quantity
            FROM OrderFood of
            JOIN Food f ON of.food_id = f.id
            WHERE of.order_id = %s
        """
        return self.db.execute_query(query, (order_id,), fetch=True)
