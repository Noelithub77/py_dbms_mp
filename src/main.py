import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from sql.db_operations import (
    DatabaseConnection,
    AdminOperations,
    RestaurantOperations,
    FoodOperations,
    CustomerOperations,
    PaymentOperations,
    OrderOperations
)
from ui.crud_components import (
    render_admin_crud,
    render_restaurant_crud,
    render_food_crud,
    render_customer_crud,
    render_payment_crud,
    render_order_crud
)

st.set_page_config(
    page_title="Restaurant Management System",
    layout="wide"
)

st.title("Restaurant Management System")
st.markdown("---")

with st.sidebar:
    st.header("Database Configuration")
    
    if 'db_config' not in st.session_state:
        st.session_state.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'restaurant_db'
        }
    
    if 'db' not in st.session_state:
        st.session_state.db = None
    
    host = st.text_input("Host", value=st.session_state.db_config['host'])
    user = st.text_input("User", value=st.session_state.db_config['user'])
    password = st.text_input("Password", type="password", value=st.session_state.db_config['password'])
    database = st.text_input("Database", value=st.session_state.db_config['database'])
    
    connect_btn = st.button("Connect to Database", type="primary")
    
    if connect_btn:
        st.session_state.db_config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        
        try:
            db = DatabaseConnection(host, user, password, database)
            with db.get_connection() as conn:
                pass
            st.session_state.db = db
            st.success("Connected to database!")
        except Exception as e:
            st.error(f"Connection failed: {str(e)}")
    
    st.markdown("---")
    
    if st.session_state.db:
        st.success("Database Connected")
        
        st.header("Navigation")
        page = st.radio(
            "Select Entity",
            ["Admin", "Restaurant", "Food", "Customer", "Payment", "Order"],
            label_visibility="collapsed"
        )
    else:
        st.warning("Not Connected")
        page = None

if st.session_state.db:
    db = st.session_state.db
    
    admin_ops = AdminOperations(db)
    restaurant_ops = RestaurantOperations(db)
    food_ops = FoodOperations(db)
    customer_ops = CustomerOperations(db)
    payment_ops = PaymentOperations(db)
    order_ops = OrderOperations(db)
    
    if page == "Admin":
        render_admin_crud(admin_ops)
    elif page == "Restaurant":
        render_restaurant_crud(restaurant_ops, admin_ops)
    elif page == "Food":
        render_food_crud(food_ops, admin_ops)
    elif page == "Customer":
        render_customer_crud(customer_ops)
    elif page == "Payment":
        render_payment_crud(payment_ops, customer_ops)
    elif page == "Order":
        render_order_crud(order_ops, customer_ops, restaurant_ops, payment_ops, food_ops)
else:
    st.info("Please configure and connect to the database using the sidebar")
    
    st.markdown("""
    ## System Overview
    
    ### Entities and Relationships
    
    1. **Admin**
       - Manages Restaurant (1:1)
       - Prepares Food items (1:N)
    
    2. **Restaurant**
       - Managed by one Admin
       - Receives Orders from Customers
    
    3. **Food**
       - Prepared by Admin
       - Can be part of multiple Orders (N:N)
    
    4. **Customer**
       - Places Orders (1:N)
       - Initiates Payments (1:N)
    
    5. **Order**
       - Placed by one Customer
       - From one Restaurant
       - Contains multiple Food items (N:N)
       - Linked to one Payment
    
    6. **Payment**
       - Initiated by one Customer
       - Can be for multiple Orders
    
    ### Features
    - Complete CRUD operations for all entities
    - Relationship management (1:1, 1:N, N:N)
    - Data integrity with foreign keys
    - Intuitive UI for managing restaurant operations
    """)
