import streamlit as st
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from sql.db_operations import (
    DatabaseConnection,
    UserOperations,
    RestaurantOperations,
    MenuItemOperations,
    OrderOperations,
    DeliveryPartnerOperations,
    CartOperations,
    RatingOperations
)
from ui.customer_view import render_customer_view
from ui.restaurant_admin_view import render_restaurant_admin_view
from ui.system_admin_view import render_system_admin_view
from ui.delivery_partner_view import render_delivery_partner_view

st.set_page_config(
    page_title="Food Delivery System",
    layout="wide"
)

st.title("Food Delivery System")
st.markdown("---")

if 'db_connected' not in st.session_state:
    st.session_state.db_connected = False

if 'current_user_role' not in st.session_state:
    st.session_state.current_user_role = None

if 'current_user_id' not in st.session_state:
    st.session_state.current_user_id = None

if 'show_register' not in st.session_state:
    st.session_state.show_register = False

with st.sidebar:
    if not st.session_state.db_connected:
        st.header("Database Configuration")
        
        if 'db_config' not in st.session_state:
            st.session_state.db_config = {
                'host': 'dbms-mysql-dbmslab.e.aivencloud.com',
                'user': 'avnadmin',
                'password': os.getenv('DB_PASSWORD', ''),
                'database': 'food_delivery(mp)',
                'port': 26098
            }
        
        if 'db' not in st.session_state:
            st.session_state.db = None
        
        host = st.text_input("Host", value=st.session_state.db_config['host'])
        user = st.text_input("User", value=st.session_state.db_config['user'])
        password = st.text_input("Password", type="password", value=st.session_state.db_config['password'])
        database = st.text_input("Database", value=st.session_state.db_config['database'])
        port = st.number_input("Port", value=st.session_state.db_config['port'], min_value=1, max_value=65535)
        
        connect_btn = st.button("Connect to Database", type="primary")
        
        if connect_btn:
            st.session_state.db_config = {
                'host': host,
                'user': user,
                'password': password,
                'database': database,
                'port': port
            }
            
            try:
                db = DatabaseConnection(host, user, password, database, port)
                with db.get_connection() as conn:
                    pass
                st.session_state.db = db
                st.session_state.db_connected = True
                st.success("Connected to database!")
                st.rerun()
            except Exception as e:
                st.error(f"Connection failed: {str(e)}")
    else:
        st.success("Database Connected")
        
        if not st.session_state.current_user_role:
            if st.session_state.show_register:
                st.header("Customer Registration")
                
                with st.form("register_form"):
                    st.markdown("#### Create New Customer Account")
                    
                    username = st.text_input("Username*")
                    email = st.text_input("Email*")
                    password = st.text_input("Password*", type="password")
                    confirm_password = st.text_input("Confirm Password*", type="password")
                    phone = st.text_input("Phone Number")
                    address = st.text_area("Delivery Address")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Register", type="primary"):
                            if username and email and password and confirm_password:
                                if password != confirm_password:
                                    st.error("Passwords do not match!")
                                else:
                                    try:
                                        user_ops = UserOperations(st.session_state.db)
                                        existing_user = user_ops.read_by_username(username)
                                        if existing_user:
                                            st.error("Username already exists!")
                                        else:
                                            user_ops.create(username, password, email, phone, address, 'customer')
                                            st.success("Registration successful! Please login.")
                                            st.session_state.show_register = False
                                            st.rerun()
                                    except Exception as e:
                                        st.error(f"Registration failed: {str(e)}")
                            else:
                                st.warning("Please fill all required fields")
                    
                    with col2:
                        if st.form_submit_button("Back to Login"):
                            st.session_state.show_register = False
                            st.rerun()
            
            else:
                st.header("Login")
                
                with st.form("login_form"):
                    st.markdown("#### Enter Your Credentials")
                    
                    username = st.text_input("Username*")
                    password = st.text_input("Password*", type="password")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.form_submit_button("Login", type="primary"):
                            if username and password:
                                try:
                                    user_ops = UserOperations(st.session_state.db)
                                    user = user_ops.read_by_username(username)
                                    
                                    if user and user['password'] == password:
                                        st.session_state.current_user_role = user['role']
                                        st.session_state.current_user_id = user['id']
                                        st.session_state.current_username = user['username']
                                        st.success(f"Logged in as {user['username']} ({user['role'].replace('_', ' ').title()})")
                                        st.rerun()
                                    else:
                                        st.error("Invalid username or password!")
                                except Exception as e:
                                    st.error(f"Login failed: {str(e)}")
                            else:
                                st.warning("Please enter username and password")
                    
                    with col2:
                        if st.form_submit_button("Register as Customer"):
                            st.session_state.show_register = True
                            st.rerun()
                
                st.markdown("---")
                st.markdown("**Demo Accounts:**")
                st.markdown("- **System Admin:** noel_admin / admin123")
                st.markdown("- **Restaurant Admin:** jishnu_anand / rest123")
                st.markdown("- **Customer:** rahul_sharma / cust123")
                st.markdown("- **Delivery Partner:** rajesh_delivery / del123")
        else:
            st.header(f"Logged in as: {st.session_state.current_username}")
            st.write(f"Role: {st.session_state.current_user_role.replace('_', ' ').title()}")
            
            if st.button("Logout"):
                st.session_state.current_user_role = None
                st.session_state.current_user_id = None
                st.session_state.current_username = None
                st.session_state.show_register = False
                st.rerun()
            
            if st.button("Disconnect Database"):
                st.session_state.db = None
                st.session_state.db_connected = False
                st.session_state.current_user_role = None
                st.session_state.current_user_id = None
                st.session_state.current_username = None
                st.session_state.show_register = False
                st.rerun()

if not st.session_state.db_connected:
    st.markdown("""
    ## Food Delivery System
    
    ### System Features
    
    1. **Customer View**
       - Browse restaurants and menu items
       - Add items to cart and place orders
       - Track order status
       - Rate restaurants and food items
    
    2. **Restaurant Admin View**
       - Manage restaurant information
       - Add/update menu items and prices
       - View and manage orders
       - Monitor ratings and analytics
    
    3. **Delivery Partner View**
       - View available orders for pickup
       - Track delivery status
       - Manage profile and availability
       - View earnings and delivery history
    
    4. **System Admin View**
       - Full CRUD operations for all entities
       - Manage users, restaurants, and delivery partners
       - System overview and analytics
    
    ### Database Schema
    - Users with role-based access (system_admin, restaurant_admin, customer, delivery_partner)
    - Restaurants with ratings and cuisine information
    - Menu items with pricing and availability
    - Orders with status tracking and payment information
    - Delivery partners with vehicle and location details
    - Ratings and reviews for restaurants and items
    - Cart functionality for active sessions
    """)
else:
    if st.session_state.current_user_role:
        db = st.session_state.db
        
        user_ops = UserOperations(db)
        restaurant_ops = RestaurantOperations(db)
        menu_item_ops = MenuItemOperations(db)
        order_ops = OrderOperations(db)
        delivery_partner_ops = DeliveryPartnerOperations(db)
        cart_ops = CartOperations(db)
        rating_ops = RatingOperations(db)
        
        if st.session_state.current_user_role == 'customer':
            render_customer_view(user_ops, restaurant_ops, menu_item_ops, order_ops, cart_ops, rating_ops)
        
        elif st.session_state.current_user_role == 'restaurant_admin':
            render_restaurant_admin_view(user_ops, restaurant_ops, menu_item_ops, order_ops, rating_ops)
        
        elif st.session_state.current_user_role == 'system_admin':
            render_system_admin_view(user_ops, restaurant_ops, menu_item_ops, order_ops, delivery_partner_ops)
        
        elif st.session_state.current_user_role == 'delivery_partner':
            render_delivery_partner_view(user_ops, order_ops, delivery_partner_ops)
    
    else:
        st.info("Please select a user from the sidebar to login.")
