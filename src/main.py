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
    page_title="Food delivery Management System",
    layout="wide"
)

st.title("Food delivery Management System")
st.markdown("---")

if 'db_connected' not in st.session_state:
    st.session_state.db_connected = False

with st.sidebar:
    if not st.session_state.db_connected:
        st.header("Database Configuration")
        
        if 'db_config' not in st.session_state:
            st.session_state.db_config = {
                'host': 'dbms-mysql-dbmslab.e.aivencloud.com',
                'user': 'avnadmin',
                'password': 'AVNS_eHpHclo73k4_4xp285J',
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
        
        if st.button("Logout"):
            st.session_state.db = None
            st.session_state.db_connected = False
            st.rerun()

if not st.session_state.db_connected:
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
else:
    main_col, nav_col = st.columns([4, 1])
    
    with nav_col:
        st.header("Navigation")
        page = st.radio(
            "Select Entity",
            ["Admin", "Restaurant", "Food", "Customer", "Payment", "Order"],
            label_visibility="collapsed"
        )
    
    with main_col:
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
