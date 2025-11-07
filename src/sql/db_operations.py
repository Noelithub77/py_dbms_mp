import pymysql
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from datetime import datetime, timedelta

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

class UserOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, username: str, password: str, email: str, phone: str = None, address: str = None, role: str = 'customer'):
        query = "INSERT INTO Users (username, password, email, phone, address, role) VALUES (%s, %s, %s, %s, %s, %s)"
        return self.db.execute_query(query, (username, password, email, phone, address, role))
    
    def read_all(self):
        return self.db.execute_query("SELECT * FROM Users ORDER BY id", fetch=True)
    
    def read_by_id(self, user_id: int):
        result = self.db.execute_query("SELECT * FROM Users WHERE id = %s", (user_id,), fetch=True)
        return result[0] if result else None
    
    def read_by_username(self, username: str):
        result = self.db.execute_query("SELECT * FROM Users WHERE username = %s", (username,), fetch=True)
        return result[0] if result else None
    
    def read_by_role(self, role: str):
        return self.db.execute_query("SELECT * FROM Users WHERE role = %s ORDER BY id", (role,), fetch=True)
    
    def update(self, user_id: int, username: str = None, password: str = None, email: str = None, phone: str = None, address: str = None, role: str = None):
        user = self.read_by_id(user_id)
        if not user:
            return False
        query = "UPDATE Users SET username = %s, password = %s, email = %s, phone = %s, address = %s, role = %s WHERE id = %s"
        params = (
            username or user['username'],
            password or user['password'],
            email or user['email'],
            phone if phone is not None else user['phone'],
            address if address is not None else user['address'],
            role if role is not None else user['role'],
            user_id
        )
        self.db.execute_query(query, params)
        return True
    
    def delete(self, user_id: int):
        self.db.execute_query("DELETE FROM Users WHERE id = %s", (user_id,))

class RestaurantOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, name: str, address: str, phone: str = None, email: str = None, cuisine_type: str = None, opening_hours: str = None, admin_id: int = None):
        query = "INSERT INTO Restaurants (name, address, phone, email, cuisine_type, opening_hours, admin_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        return self.db.execute_query(query, (name, address, phone, email, cuisine_type, opening_hours, admin_id))
    
    def read_all(self):
        query = """
            SELECT r.*, u.username as admin_username 
            FROM Restaurants r 
            LEFT JOIN Users u ON r.admin_id = u.id 
            ORDER BY r.id
        """
        return self.db.execute_query(query, fetch=True)
    
    def read_by_id(self, restaurant_id: int):
        query = """
            SELECT r.*, u.username as admin_username 
            FROM Restaurants r 
            LEFT JOIN Users u ON r.admin_id = u.id 
            WHERE r.id = %s
        """
        result = self.db.execute_query(query, (restaurant_id,), fetch=True)
        return result[0] if result else None
    
    def read_by_admin(self, admin_id: int):
        return self.db.execute_query("SELECT * FROM Restaurants WHERE admin_id = %s ORDER BY id", (admin_id,), fetch=True)
    
    def update(self, restaurant_id: int, name: str = None, address: str = None, phone: str = None, email: str = None, cuisine_type: str = None, opening_hours: str = None, admin_id: int = None, is_active: bool = None):
        restaurant = self.read_by_id(restaurant_id)
        if not restaurant:
            return False
        query = "UPDATE Restaurants SET name = %s, address = %s, phone = %s, email = %s, cuisine_type = %s, opening_hours = %s, admin_id = %s, is_active = %s WHERE id = %s"
        params = (
            name or restaurant['name'],
            address if address is not None else restaurant['address'],
            phone if phone is not None else restaurant['phone'],
            email if email is not None else restaurant['email'],
            cuisine_type if cuisine_type is not None else restaurant['cuisine_type'],
            opening_hours if opening_hours is not None else restaurant['opening_hours'],
            admin_id if admin_id is not None else restaurant['admin_id'],
            is_active if is_active is not None else restaurant['is_active'],
            restaurant_id
        )
        self.db.execute_query(query, params)
        return True
    
    def delete(self, restaurant_id: int):
        self.db.execute_query("DELETE FROM Restaurants WHERE id = %s", (restaurant_id,))

class MenuItemOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, restaurant_id: int, name: str, description: str = None, price: float = 0.0, category: str = None, is_vegetarian: bool = True, preparation_time: int = 15):
        query = "INSERT INTO MenuItems (restaurant_id, name, description, price, category, is_vegetarian, preparation_time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        return self.db.execute_query(query, (restaurant_id, name, description, price, category, is_vegetarian, preparation_time))
    
    def read_all(self):
        query = """
            SELECT mi.*, r.name as restaurant_name 
            FROM MenuItems mi 
            LEFT JOIN Restaurants r ON mi.restaurant_id = r.id 
            ORDER BY mi.restaurant_id, mi.name
        """
        return self.db.execute_query(query, fetch=True)
    
    def read_by_id(self, menu_item_id: int):
        query = """
            SELECT mi.*, r.name as restaurant_name 
            FROM MenuItems mi 
            LEFT JOIN Restaurants r ON mi.restaurant_id = r.id 
            WHERE mi.id = %s
        """
        result = self.db.execute_query(query, (menu_item_id,), fetch=True)
        return result[0] if result else None
    
    def read_by_restaurant(self, restaurant_id: int):
        query = """
            SELECT mi.*, r.name as restaurant_name 
            FROM MenuItems mi 
            LEFT JOIN Restaurants r ON mi.restaurant_id = r.id 
            WHERE mi.restaurant_id = %s
            ORDER BY mi.name
        """
        return self.db.execute_query(query, (restaurant_id,), fetch=True)
    
    def read_available_by_restaurant(self, restaurant_id: int):
        query = """
            SELECT mi.*, r.name as restaurant_name 
            FROM MenuItems mi 
            LEFT JOIN Restaurants r ON mi.restaurant_id = r.id 
            WHERE mi.restaurant_id = %s AND mi.is_available = TRUE
            ORDER BY mi.name
        """
        return self.db.execute_query(query, (restaurant_id,), fetch=True)
    
    def update(self, menu_item_id: int, name: str = None, description: str = None, price: float = None, category: str = None, is_vegetarian: bool = None, preparation_time: int = None, is_available: bool = None):
        menu_item = self.read_by_id(menu_item_id)
        if not menu_item:
            return False
        query = "UPDATE MenuItems SET name = %s, description = %s, price = %s, category = %s, is_vegetarian = %s, preparation_time = %s, is_available = %s WHERE id = %s"
        params = (
            name or menu_item['name'],
            description if description is not None else menu_item['description'],
            price if price is not None else menu_item['price'],
            category if category is not None else menu_item['category'],
            is_vegetarian if is_vegetarian is not None else menu_item['is_vegetarian'],
            preparation_time if preparation_time is not None else menu_item['preparation_time'],
            is_available if is_available is not None else menu_item['is_available'],
            menu_item_id
        )
        self.db.execute_query(query, params)
        return True
    
    def delete(self, menu_item_id: int):
        self.db.execute_query("DELETE FROM MenuItems WHERE id = %s", (menu_item_id,))

class OrderOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, customer_id: int, restaurant_id: int, delivery_address: str, total_amount: float, payment_method: str = None):
        estimated_time = datetime.now() + timedelta(minutes=45)
        query = "INSERT INTO Orders (customer_id, restaurant_id, delivery_address, total_amount, payment_method, estimated_delivery_time) VALUES (%s, %s, %s, %s, %s, %s)"
        return self.db.execute_query(query, (customer_id, restaurant_id, delivery_address, total_amount, payment_method, estimated_time))
    
    def read_all(self):
        query = """
            SELECT o.*, u.username as customer_username, r.name as restaurant_name, dp.username as delivery_partner_username
            FROM Orders o
            LEFT JOIN Users u ON o.customer_id = u.id
            LEFT JOIN Restaurants r ON o.restaurant_id = r.id
            LEFT JOIN Users dp ON o.delivery_partner_id = dp.id
            ORDER BY o.created_at DESC
        """
        return self.db.execute_query(query, fetch=True)
    
    def read_by_id(self, order_id: int):
        query = """
            SELECT o.*, u.username as customer_username, r.name as restaurant_name, dp.username as delivery_partner_username
            FROM Orders o
            LEFT JOIN Users u ON o.customer_id = u.id
            LEFT JOIN Restaurants r ON o.restaurant_id = r.id
            LEFT JOIN Users dp ON o.delivery_partner_id = dp.id
            WHERE o.id = %s
        """
        result = self.db.execute_query(query, (order_id,), fetch=True)
        return result[0] if result else None
    
    def read_by_customer(self, customer_id: int):
        query = """
            SELECT o.*, u.username as customer_username, r.name as restaurant_name, dp.username as delivery_partner_username
            FROM Orders o
            LEFT JOIN Users u ON o.customer_id = u.id
            LEFT JOIN Restaurants r ON o.restaurant_id = r.id
            LEFT JOIN Users dp ON o.delivery_partner_id = dp.id
            WHERE o.customer_id = %s
            ORDER BY o.created_at DESC
        """
        return self.db.execute_query(query, (customer_id,), fetch=True)
    
    def read_by_restaurant(self, restaurant_id: int):
        query = """
            SELECT o.*, u.username as customer_username, r.name as restaurant_name, dp.username as delivery_partner_username
            FROM Orders o
            LEFT JOIN Users u ON o.customer_id = u.id
            LEFT JOIN Restaurants r ON o.restaurant_id = r.id
            LEFT JOIN Users dp ON o.delivery_partner_id = dp.id
            WHERE o.restaurant_id = %s
            ORDER BY o.created_at DESC
        """
        return self.db.execute_query(query, (restaurant_id,), fetch=True)
    
    def read_by_delivery_partner(self, delivery_partner_id: int):
        query = """
            SELECT o.*, u.username as customer_username, r.name as restaurant_name, dp.username as delivery_partner_username
            FROM Orders o
            LEFT JOIN Users u ON o.customer_id = u.id
            LEFT JOIN Restaurants r ON o.restaurant_id = r.id
            LEFT JOIN Users dp ON o.delivery_partner_id = dp.id
            WHERE o.delivery_partner_id = %s
            ORDER BY o.created_at DESC
        """
        return self.db.execute_query(query, (delivery_partner_id,), fetch=True)
    
    def update_status(self, order_id: int, status: str):
        query = "UPDATE Orders SET status = %s WHERE id = %s"
        self.db.execute_query(query, (status, order_id))
    
    def update_payment_status(self, order_id: int, payment_status: str):
        query = "UPDATE Orders SET payment_status = %s WHERE id = %s"
        self.db.execute_query(query, (payment_status, order_id))
    
    def assign_delivery_partner(self, order_id: int, delivery_partner_id: int):
        query = "UPDATE Orders SET delivery_partner_id = %s, status = 'confirmed' WHERE id = %s"
        self.db.execute_query(query, (delivery_partner_id, order_id))
    
    def update(self, order_id: int, customer_id: int = None, restaurant_id: int = None, delivery_address: str = None, total_amount: float = None, status: str = None, payment_status: str = None, payment_method: str = None, delivery_partner_id: int = None):
        order = self.read_by_id(order_id)
        if not order:
            return False
        query = "UPDATE Orders SET customer_id = %s, restaurant_id = %s, delivery_address = %s, total_amount = %s, status = %s, payment_status = %s, payment_method = %s, delivery_partner_id = %s WHERE id = %s"
        params = (
            customer_id if customer_id is not None else order['customer_id'],
            restaurant_id if restaurant_id is not None else order['restaurant_id'],
            delivery_address if delivery_address is not None else order['delivery_address'],
            total_amount if total_amount is not None else order['total_amount'],
            status if status is not None else order['status'],
            payment_status if payment_status is not None else order['payment_status'],
            payment_method if payment_method is not None else order['payment_method'],
            delivery_partner_id if delivery_partner_id is not None else order['delivery_partner_id'],
            order_id
        )
        self.db.execute_query(query, params)
        return True
    
    def delete(self, order_id: int):
        self.db.execute_query("DELETE FROM Orders WHERE id = %s", (order_id,))
    
    def add_item(self, order_id: int, menu_item_id: int, quantity: int = 1, price_per_item: float = None):
        menu_item = self.db.execute_query("SELECT price FROM MenuItems WHERE id = %s", (menu_item_id,), fetch=True)[0]
        price = price_per_item or menu_item['price']
        subtotal = price * quantity
        query = "INSERT INTO OrderItems (order_id, menu_item_id, quantity, price_per_item, subtotal) VALUES (%s, %s, %s, %s, %s)"
        self.db.execute_query(query, (order_id, menu_item_id, quantity, price, subtotal))
    
    def remove_item(self, order_id: int, menu_item_id: int):
        self.db.execute_query("DELETE FROM OrderItems WHERE order_id = %s AND menu_item_id = %s", (order_id, menu_item_id))
    
    def get_order_items(self, order_id: int):
        query = """
            SELECT oi.*, mi.name as item_name, mi.description as item_description
            FROM OrderItems oi
            JOIN MenuItems mi ON oi.menu_item_id = mi.id
            WHERE oi.order_id = %s
        """
        return self.db.execute_query(query, (order_id,), fetch=True)

class DeliveryPartnerOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create(self, user_id: int, vehicle_type: str, vehicle_number: str, license_number: str = None):
        query = "INSERT INTO DeliveryPartners (user_id, vehicle_type, vehicle_number, license_number) VALUES (%s, %s, %s, %s)"
        return self.db.execute_query(query, (user_id, vehicle_type, vehicle_number, license_number))
    
    def read_all(self):
        query = """
            SELECT dp.*, u.username, u.phone, u.email
            FROM DeliveryPartners dp
            JOIN Users u ON dp.user_id = u.id
            ORDER BY dp.rating DESC
        """
        return self.db.execute_query(query, fetch=True)
    
    def read_by_id(self, delivery_partner_id: int):
        query = """
            SELECT dp.*, u.username, u.phone, u.email
            FROM DeliveryPartners dp
            JOIN Users u ON dp.user_id = u.id
            WHERE dp.id = %s
        """
        result = self.db.execute_query(query, (delivery_partner_id,), fetch=True)
        return result[0] if result else None
    
    def read_online(self):
        query = """
            SELECT dp.*, u.username, u.phone, u.email
            FROM DeliveryPartners dp
            JOIN Users u ON dp.user_id = u.id
            WHERE dp.is_online = TRUE
            ORDER BY dp.rating DESC
        """
        return self.db.execute_query(query, fetch=True)
    
    def update_online_status(self, delivery_partner_id: int, is_online: bool):
        query = "UPDATE DeliveryPartners SET is_online = %s WHERE id = %s"
        self.db.execute_query(query, (is_online, delivery_partner_id))
    
    def update_location(self, delivery_partner_id: int, latitude: float, longitude: float):
        query = "UPDATE DeliveryPartners SET current_latitude = %s, current_longitude = %s WHERE id = %s"
        self.db.execute_query(query, (latitude, longitude, delivery_partner_id))
    
    def update_rating(self, delivery_partner_id: int, rating: float):
        query = "UPDATE DeliveryPartners SET rating = %s WHERE id = %s"
        self.db.execute_query(query, (rating, delivery_partner_id))
    
    def increment_deliveries(self, delivery_partner_id: int):
        query = "UPDATE DeliveryPartners SET total_deliveries = total_deliveries + 1 WHERE id = %s"
        self.db.execute_query(query, (delivery_partner_id,))
    
    def delete(self, delivery_partner_id: int):
        self.db.execute_query("DELETE FROM DeliveryPartners WHERE id = %s", (delivery_partner_id,))

class CartOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def add_item(self, customer_id: int, menu_item_id: int, quantity: int = 1):
        query = "INSERT INTO Cart (customer_id, menu_item_id, quantity) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE quantity = %s"
        self.db.execute_query(query, (customer_id, menu_item_id, quantity, quantity))
    
    def update_quantity(self, customer_id: int, menu_item_id: int, quantity: int):
        if quantity <= 0:
            self.remove_item(customer_id, menu_item_id)
        else:
            query = "UPDATE Cart SET quantity = %s WHERE customer_id = %s AND menu_item_id = %s"
            self.db.execute_query(query, (quantity, customer_id, menu_item_id))
    
    def remove_item(self, customer_id: int, menu_item_id: int):
        self.db.execute_query("DELETE FROM Cart WHERE customer_id = %s AND menu_item_id = %s", (customer_id, menu_item_id))
    
    def get_cart(self, customer_id: int):
        query = """
            SELECT c.*, mi.name as item_name, mi.price, mi.restaurant_id, r.name as restaurant_name
            FROM Cart c
            JOIN MenuItems mi ON c.menu_item_id = mi.id
            JOIN Restaurants r ON mi.restaurant_id = r.id
            WHERE c.customer_id = %s
            ORDER BY r.name, mi.name
        """
        return self.db.execute_query(query, (customer_id,), fetch=True)
    
    def clear_cart(self, customer_id: int):
        self.db.execute_query("DELETE FROM Cart WHERE customer_id = %s", (customer_id,))
    
    def get_cart_total(self, customer_id: int):
        query = """
            SELECT SUM(c.quantity * mi.price) as total
            FROM Cart c
            JOIN MenuItems mi ON c.menu_item_id = mi.id
            WHERE c.customer_id = %s
        """
        result = self.db.execute_query(query, (customer_id,), fetch=True)
        return result[0]['total'] if result and result[0]['total'] else 0.0

class RatingOperations:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create_restaurant_rating(self, restaurant_id: int, customer_id: int, rating: int, review: str = None):
        query = "INSERT INTO RestaurantRatings (restaurant_id, customer_id, rating, review) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE rating = %s, review = %s"
        self.db.execute_query(query, (restaurant_id, customer_id, rating, review, rating, review))
    
    def create_item_rating(self, menu_item_id: int, customer_id: int, rating: int, review: str = None):
        query = "INSERT INTO ItemRatings (menu_item_id, customer_id, rating, review) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE rating = %s, review = %s"
        self.db.execute_query(query, (menu_item_id, customer_id, rating, review, rating, review))
    
    def get_restaurant_ratings(self, restaurant_id: int):
        query = """
            SELECT rr.*, u.username as customer_username
            FROM RestaurantRatings rr
            JOIN Users u ON rr.customer_id = u.id
            WHERE rr.restaurant_id = %s
            ORDER BY rr.created_at DESC
        """
        return self.db.execute_query(query, (restaurant_id,), fetch=True)
    
    def get_item_ratings(self, menu_item_id: int):
        query = """
            SELECT ir.*, u.username as customer_username
            FROM ItemRatings ir
            JOIN Users u ON ir.customer_id = u.id
            WHERE ir.menu_item_id = %s
            ORDER BY ir.created_at DESC
        """
        return self.db.execute_query(query, (menu_item_id,), fetch=True)
    
    def get_restaurant_average_rating(self, restaurant_id: int):
        query = "SELECT COALESCE(AVG(rating), 0) as avg_rating FROM RestaurantRatings WHERE restaurant_id = %s"
        result = self.db.execute_query(query, (restaurant_id,), fetch=True)
        return result[0]['avg_rating'] if result else 0.0
    
    def get_item_average_rating(self, menu_item_id: int):
        query = "SELECT COALESCE(AVG(rating), 0) as avg_rating FROM ItemRatings WHERE menu_item_id = %s"
        result = self.db.execute_query(query, (menu_item_id,), fetch=True)
        return result[0]['avg_rating'] if result else 0.0
