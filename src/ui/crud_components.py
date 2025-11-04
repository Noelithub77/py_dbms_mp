import streamlit as st
from typing import Any, Dict

def render_admin_crud(admin_ops):
    st.header("Admin Management")
    
    tab1, tab2, tab3, tab4 = st.tabs([":material/add_circle: Create", ":material/visibility: View", ":material/edit: Update", ":material/delete: Delete"])
    
    with tab1:
        with st.form("create_admin"):
            username = st.text_input("Username*")
            password = st.text_input("Password*", type="password")
            email = st.text_input("Email*")
            address = st.text_area("Address")
            phoneno = st.text_input("Phone Number")
            
            if st.form_submit_button("Create Admin"):
                if username and password and email:
                    try:
                        admin_ops.create(username, password, email, address, phoneno)
                        st.success(f"Admin '{username}' created successfully!")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please fill all required fields")
    
    with tab2:
        admins = admin_ops.read_all()
        if admins:
            st.dataframe(admins, use_container_width=True)
        else:
            st.info("No admins found")
    
    with tab3:
        admins = admin_ops.read_all()
        if admins:
            admin_ids = {f"{a['username']} (ID: {a['id']})": a['id'] for a in admins}
            selected = st.selectbox("Select Admin", list(admin_ids.keys()))
            
            if selected:
                admin_id = admin_ids[selected]
                admin = admin_ops.read_by_id(admin_id)
                
                with st.form("update_admin"):
                    username = st.text_input("Username", value=admin['username'])
                    password = st.text_input("Password", type="password", placeholder="Leave empty to keep current")
                    email = st.text_input("Email", value=admin['email'])
                    address = st.text_area("Address", value=admin['address'] or "")
                    phoneno = st.text_input("Phone Number", value=admin['phoneno'] or "")
                    
                    if st.form_submit_button("Update Admin"):
                        try:
                            admin_ops.update(admin_id, username, password or None, email, address, phoneno)
                            st.success("Admin updated successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        else:
            st.info("No admins available")
    
    with tab4:
        admins = admin_ops.read_all()
        if admins:
            admin_ids = {f"{a['username']} (ID: {a['id']})": a['id'] for a in admins}
            selected = st.selectbox("Select Admin to Delete", list(admin_ids.keys()))
            
            if st.button("Delete Admin", type="primary"):
                admin_id = admin_ids[selected]
                try:
                    admin_ops.delete(admin_id)
                    st.success("Admin deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.info("No admins available")

def render_restaurant_crud(restaurant_ops, admin_ops):
    st.header("Restaurant Management")
    
    tab1, tab2, tab3, tab4 = st.tabs([":material/add_circle: Create", ":material/visibility: View", ":material/edit: Update", ":material/delete: Delete"])
    
    with tab1:
        with st.form("create_restaurant"):
            name = st.text_input("Restaurant Name*")
            address = st.text_area("Address")
            opening_hours = st.text_input("Opening Hours")
            
            admins = admin_ops.read_all()
            admin_options = {f"{a['username']} (ID: {a['id']})": a['id'] for a in admins} if admins else {}
            admin_options = {"None": None, **admin_options}
            selected_admin = st.selectbox("Managed By Admin", list(admin_options.keys()))
            
            if st.form_submit_button("Create Restaurant"):
                if name:
                    try:
                        admin_id = admin_options[selected_admin]
                        restaurant_ops.create(name, address, opening_hours, admin_id)
                        st.success(f"Restaurant '{name}' created successfully!")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please provide restaurant name")
    
    with tab2:
        restaurants = restaurant_ops.read_all()
        if restaurants:
            st.dataframe(restaurants, use_container_width=True)
        else:
            st.info("No restaurants found")
    
    with tab3:
        restaurants = restaurant_ops.read_all()
        if restaurants:
            restaurant_ids = {f"{r['name']} (ID: {r['id']})": r['id'] for r in restaurants}
            selected = st.selectbox("Select Restaurant", list(restaurant_ids.keys()))
            
            if selected:
                restaurant_id = restaurant_ids[selected]
                restaurant = restaurant_ops.read_by_id(restaurant_id)
                
                with st.form("update_restaurant"):
                    name = st.text_input("Restaurant Name", value=restaurant['name'])
                    address = st.text_area("Address", value=restaurant['address'] or "")
                    opening_hours = st.text_input("Opening Hours", value=restaurant['openingHours'] or "")
                    
                    admins = admin_ops.read_all()
                    admin_options = {f"{a['username']} (ID: {a['id']})": a['id'] for a in admins} if admins else {}
                    admin_options = {"None": None, **admin_options}
                    current_admin = next((k for k, v in admin_options.items() if v == restaurant['admin_id']), "None")
                    selected_admin = st.selectbox("Managed By Admin", list(admin_options.keys()), index=list(admin_options.keys()).index(current_admin))
                    
                    if st.form_submit_button("Update Restaurant"):
                        try:
                            admin_id = admin_options[selected_admin]
                            restaurant_ops.update(restaurant_id, name, address, opening_hours, admin_id)
                            st.success("Restaurant updated successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        else:
            st.info("No restaurants available")
    
    with tab4:
        restaurants = restaurant_ops.read_all()
        if restaurants:
            restaurant_ids = {f"{r['name']} (ID: {r['id']})": r['id'] for r in restaurants}
            selected = st.selectbox("Select Restaurant to Delete", list(restaurant_ids.keys()))
            
            if st.button("Delete Restaurant", type="primary"):
                restaurant_id = restaurant_ids[selected]
                try:
                    restaurant_ops.delete(restaurant_id)
                    st.success("Restaurant deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.info("No restaurants available")

def render_food_crud(food_ops, admin_ops):
    st.header("Food Management")
    
    tab1, tab2, tab3, tab4 = st.tabs([":material/add_circle: Create", ":material/visibility: View", ":material/edit: Update", ":material/delete: Delete"])
    
    with tab1:
        with st.form("create_food"):
            name = st.text_input("Food Name*")
            ingredients = st.text_area("Ingredients")
            category = st.selectbox("Category", ["Appetizer", "Main Course", "Dessert", "Beverage", "Other"])
            is_non_veg = st.checkbox("Non-Vegetarian")
            
            admins = admin_ops.read_all()
            admin_options = {f"{a['username']} (ID: {a['id']})": a['id'] for a in admins} if admins else {}
            admin_options = {"None": None, **admin_options}
            selected_admin = st.selectbox("Prepared By Admin", list(admin_options.keys()))
            
            if st.form_submit_button("Create Food"):
                if name:
                    try:
                        admin_id = admin_options[selected_admin]
                        food_ops.create(name, ingredients, category, is_non_veg, admin_id)
                        st.success(f"Food '{name}' created successfully!")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please provide food name")
    
    with tab2:
        foods = food_ops.read_all()
        if foods:
            st.dataframe(foods, use_container_width=True)
        else:
            st.info("No foods found")
    
    with tab3:
        foods = food_ops.read_all()
        if foods:
            food_ids = {f"{f['name']} (ID: {f['id']})": f['id'] for f in foods}
            selected = st.selectbox("Select Food", list(food_ids.keys()))
            
            if selected:
                food_id = food_ids[selected]
                food = food_ops.read_by_id(food_id)
                
                with st.form("update_food"):
                    name = st.text_input("Food Name", value=food['name'])
                    ingredients = st.text_area("Ingredients", value=food['ingredients'] or "")
                    category = st.selectbox("Category", ["Appetizer", "Main Course", "Dessert", "Beverage", "Other"], 
                                          index=["Appetizer", "Main Course", "Dessert", "Beverage", "Other"].index(food['category']) if food['category'] in ["Appetizer", "Main Course", "Dessert", "Beverage", "Other"] else 4)
                    is_non_veg = st.checkbox("Non-Vegetarian", value=bool(food['isNonVeg']))
                    
                    admins = admin_ops.read_all()
                    admin_options = {f"{a['username']} (ID: {a['id']})": a['id'] for a in admins} if admins else {}
                    admin_options = {"None": None, **admin_options}
                    current_admin = next((k for k, v in admin_options.items() if v == food['admin_id']), "None")
                    selected_admin = st.selectbox("Prepared By Admin", list(admin_options.keys()), index=list(admin_options.keys()).index(current_admin))
                    
                    if st.form_submit_button("Update Food"):
                        try:
                            admin_id = admin_options[selected_admin]
                            food_ops.update(food_id, name, ingredients, category, is_non_veg, admin_id)
                            st.success("Food updated successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        else:
            st.info("No foods available")
    
    with tab4:
        foods = food_ops.read_all()
        if foods:
            food_ids = {f"{f['name']} (ID: {f['id']})": f['id'] for f in foods}
            selected = st.selectbox("Select Food to Delete", list(food_ids.keys()))
            
            if st.button("Delete Food", type="primary"):
                food_id = food_ids[selected]
                try:
                    food_ops.delete(food_id)
                    st.success("Food deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.info("No foods available")

def render_customer_crud(customer_ops):
    st.header("Customer Management")
    
    tab1, tab2, tab3, tab4 = st.tabs([":material/add_circle: Create", ":material/visibility: View", ":material/edit: Update", ":material/delete: Delete"])
    
    with tab1:
        with st.form("create_customer"):
            username = st.text_input("Username*")
            password = st.text_input("Password*", type="password")
            email = st.text_input("Email*")
            address = st.text_area("Address")
            phoneno = st.text_input("Phone Number")
            
            if st.form_submit_button("Create Customer"):
                if username and password and email:
                    try:
                        customer_ops.create(username, password, email, address, phoneno)
                        st.success(f"Customer '{username}' created successfully!")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please fill all required fields")
    
    with tab2:
        customers = customer_ops.read_all()
        if customers:
            st.dataframe(customers, use_container_width=True)
        else:
            st.info("No customers found")
    
    with tab3:
        customers = customer_ops.read_all()
        if customers:
            customer_ids = {f"{c['username']} (ID: {c['id']})": c['id'] for c in customers}
            selected = st.selectbox("Select Customer", list(customer_ids.keys()))
            
            if selected:
                customer_id = customer_ids[selected]
                customer = customer_ops.read_by_id(customer_id)
                
                with st.form("update_customer"):
                    username = st.text_input("Username", value=customer['username'])
                    password = st.text_input("Password", type="password", placeholder="Leave empty to keep current")
                    email = st.text_input("Email", value=customer['email'])
                    address = st.text_area("Address", value=customer['address'] or "")
                    phoneno = st.text_input("Phone Number", value=customer['phoneno'] or "")
                    
                    if st.form_submit_button("Update Customer"):
                        try:
                            customer_ops.update(customer_id, username, password or None, email, address, phoneno)
                            st.success("Customer updated successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        else:
            st.info("No customers available")
    
    with tab4:
        customers = customer_ops.read_all()
        if customers:
            customer_ids = {f"{c['username']} (ID: {c['id']})": c['id'] for c in customers}
            selected = st.selectbox("Select Customer to Delete", list(customer_ids.keys()))
            
            if st.button("Delete Customer", type="primary"):
                customer_id = customer_ids[selected]
                try:
                    customer_ops.delete(customer_id)
                    st.success("Customer deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.info("No customers available")

def render_payment_crud(payment_ops, customer_ops):
    st.header("Payment Management")
    
    tab1, tab2, tab3, tab4 = st.tabs([":material/add_circle: Create", ":material/visibility: View", ":material/edit: Update", ":material/delete: Delete"])
    
    with tab1:
        with st.form("create_payment"):
            payment_type = st.selectbox("Payment Type*", ["Cash", "Credit Card", "Debit Card", "UPI", "Net Banking"])
            price = st.number_input("Amount*", min_value=0.0, step=0.01)
            
            customers = customer_ops.read_all()
            customer_options = {f"{c['username']} (ID: {c['id']})": c['id'] for c in customers} if customers else {}
            selected_customer = st.selectbox("Customer*", list(customer_options.keys()))
            
            if st.form_submit_button("Create Payment"):
                if payment_type and price > 0 and selected_customer:
                    try:
                        customer_id = customer_options[selected_customer]
                        payment_ops.create(payment_type, price, customer_id)
                        st.success(f"Payment of ₹{price} created successfully!")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please fill all required fields")
    
    with tab2:
        payments = payment_ops.read_all()
        if payments:
            st.dataframe(payments, use_container_width=True)
        else:
            st.info("No payments found")
    
    with tab3:
        payments = payment_ops.read_all()
        if payments:
            payment_ids = {f"Payment #{p['id']} - ₹{p['price']}": p['id'] for p in payments}
            selected = st.selectbox("Select Payment", list(payment_ids.keys()))
            
            if selected:
                payment_id = payment_ids[selected]
                payment = payment_ops.read_by_id(payment_id)
                
                with st.form("update_payment"):
                    payment_type = st.selectbox("Payment Type", ["Cash", "Credit Card", "Debit Card", "UPI", "Net Banking"],
                                               index=["Cash", "Credit Card", "Debit Card", "UPI", "Net Banking"].index(payment['type']) if payment['type'] in ["Cash", "Credit Card", "Debit Card", "UPI", "Net Banking"] else 0)
                    price = st.number_input("Amount", value=float(payment['price']), min_value=0.0, step=0.01)
                    
                    customers = customer_ops.read_all()
                    customer_options = {f"{c['username']} (ID: {c['id']})": c['id'] for c in customers} if customers else {}
                    current_customer = next((k for k, v in customer_options.items() if v == payment['customer_id']), list(customer_options.keys())[0] if customer_options else None)
                    selected_customer = st.selectbox("Customer", list(customer_options.keys()), index=list(customer_options.keys()).index(current_customer) if current_customer else 0)
                    
                    if st.form_submit_button("Update Payment"):
                        try:
                            customer_id = customer_options[selected_customer]
                            payment_ops.update(payment_id, payment_type, price, customer_id)
                            st.success("Payment updated successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        else:
            st.info("No payments available")
    
    with tab4:
        payments = payment_ops.read_all()
        if payments:
            payment_ids = {f"Payment #{p['id']} - ₹{p['price']}": p['id'] for p in payments}
            selected = st.selectbox("Select Payment to Delete", list(payment_ids.keys()))
            
            if st.button("Delete Payment", type="primary"):
                payment_id = payment_ids[selected]
                try:
                    payment_ops.delete(payment_id)
                    st.success("Payment deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.info("No payments available")

def render_order_crud(order_ops, customer_ops, restaurant_ops, payment_ops, food_ops):
    st.header("Order Management")
    
    tab1, tab2, tab3, tab4 = st.tabs([":material/add_circle: Create", ":material/visibility: View", ":material/edit: Update", ":material/delete: Delete"])
    
    with tab1:
        with st.form("create_order"):
            price = st.number_input("Total Price*", min_value=0.0, step=0.01)
            address = st.text_area("Delivery Address")
            
            customers = customer_ops.read_all()
            customer_options = {f"{c['username']} (ID: {c['id']})": c['id'] for c in customers} if customers else {}
            selected_customer = st.selectbox("Customer*", list(customer_options.keys()))
            
            restaurants = restaurant_ops.read_all()
            restaurant_options = {f"{r['name']} (ID: {r['id']})": r['id'] for r in restaurants} if restaurants else {}
            selected_restaurant = st.selectbox("Restaurant*", list(restaurant_options.keys()))
            
            payments = payment_ops.read_all()
            payment_options = {f"Payment #{p['id']} - ₹{p['price']}": p['id'] for p in payments} if payments else {}
            payment_options = {"None": None, **payment_options}
            selected_payment = st.selectbox("Payment", list(payment_options.keys()))
            
            if st.form_submit_button("Create Order"):
                if price > 0 and selected_customer and selected_restaurant:
                    try:
                        customer_id = customer_options[selected_customer]
                        restaurant_id = restaurant_options[selected_restaurant]
                        payment_id = payment_options[selected_payment]
                        order_ops.create(price, customer_id, restaurant_id, payment_id, address)
                        st.success(f"Order created successfully!")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please fill all required fields")
    
    with tab2:
        orders = order_ops.read_all()
        if orders:
            st.dataframe(orders, use_container_width=True)
            
            st.subheader("Order Details")
            order_ids = {f"Order #{o['id']}": o['id'] for o in orders}
            selected_order = st.selectbox("View Foods in Order", list(order_ids.keys()))
            if selected_order:
                order_id = order_ids[selected_order]
                foods = order_ops.get_order_foods(order_id)
                if foods:
                    st.dataframe(foods, use_container_width=True)
                else:
                    st.info("No foods in this order")
        else:
            st.info("No orders found")
    
    with tab3:
        orders = order_ops.read_all()
        if orders:
            order_ids = {f"Order #{o['id']}": o['id'] for o in orders}
            selected = st.selectbox("Select Order", list(order_ids.keys()))
            
            if selected:
                order_id = order_ids[selected]
                order = order_ops.read_by_id(order_id)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Update Order Details")
                    with st.form("update_order"):
                        price = st.number_input("Total Price", value=float(order['price']), min_value=0.0, step=0.01)
                        address = st.text_area("Delivery Address", value=order['address'] or "")
                        
                        customers = customer_ops.read_all()
                        customer_options = {f"{c['username']} (ID: {c['id']})": c['id'] for c in customers} if customers else {}
                        current_customer = next((k for k, v in customer_options.items() if v == order['customer_id']), list(customer_options.keys())[0] if customer_options else None)
                        selected_customer = st.selectbox("Customer", list(customer_options.keys()), index=list(customer_options.keys()).index(current_customer) if current_customer else 0)
                        
                        restaurants = restaurant_ops.read_all()
                        restaurant_options = {f"{r['name']} (ID: {r['id']})": r['id'] for r in restaurants} if restaurants else {}
                        current_restaurant = next((k for k, v in restaurant_options.items() if v == order['restaurant_id']), list(restaurant_options.keys())[0] if restaurant_options else None)
                        selected_restaurant = st.selectbox("Restaurant", list(restaurant_options.keys()), index=list(restaurant_options.keys()).index(current_restaurant) if current_restaurant else 0)
                        
                        payments = payment_ops.read_all()
                        payment_options = {f"Payment #{p['id']} - ₹{p['price']}": p['id'] for p in payments} if payments else {}
                        payment_options = {"None": None, **payment_options}
                        current_payment = next((k for k, v in payment_options.items() if v == order['payment_id']), "None")
                        selected_payment = st.selectbox("Payment", list(payment_options.keys()), index=list(payment_options.keys()).index(current_payment))
                        
                        if st.form_submit_button("Update Order"):
                            try:
                                customer_id = customer_options[selected_customer]
                                restaurant_id = restaurant_options[selected_restaurant]
                                payment_id = payment_options[selected_payment]
                                order_ops.update(order_id, price, customer_id, restaurant_id, payment_id, address)
                                st.success("Order updated successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                
                with col2:
                    st.subheader("Manage Order Foods")
                    foods = food_ops.read_all()
                    if foods:
                        food_options = {f"{f['name']} (ID: {f['id']})": f['id'] for f in foods}
                        selected_food = st.selectbox("Add Food", list(food_options.keys()))
                        quantity = st.number_input("Quantity", min_value=1, value=1)
                        
                        if st.button("Add Food to Order"):
                            try:
                                food_id = food_options[selected_food]
                                order_ops.add_food(order_id, food_id, quantity)
                                st.success("Food added to order!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                        
                        order_foods = order_ops.get_order_foods(order_id)
                        if order_foods:
                            st.write("Current Foods:")
                            for food in order_foods:
                                col_a, col_b = st.columns([3, 1])
                                with col_a:
                                    st.write(f"{food['name']} (Qty: {food['quantity']})")
                                with col_b:
                                    if st.button("Remove", key=f"remove_{food['id']}"):
                                        order_ops.remove_food(order_id, food['id'])
                                        st.rerun()
        else:
            st.info("No orders available")
    
    with tab4:
        orders = order_ops.read_all()
        if orders:
            order_ids = {f"Order #{o['id']}": o['id'] for o in orders}
            selected = st.selectbox("Select Order to Delete", list(order_ids.keys()))
            
            if st.button("Delete Order", type="primary"):
                order_id = order_ids[selected]
                try:
                    order_ops.delete(order_id)
                    st.success("Order deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.info("No orders available")
