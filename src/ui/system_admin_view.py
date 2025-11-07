import streamlit as st
from typing import Dict, Any

def render_system_admin_view(user_ops, restaurant_ops, menu_item_ops, order_ops, delivery_partner_ops):
    st.header("System Admin View")
    
    tabs = st.tabs(["Users", "Restaurants", "Menu Items", "Orders", "Delivery Partners", "System Overview"])
    
    with tabs[0]:
        render_user_management(user_ops)
    
    with tabs[1]:
        render_restaurant_management(restaurant_ops, user_ops)
    
    with tabs[2]:
        render_menu_item_management(menu_item_ops, restaurant_ops)
    
    with tabs[3]:
        render_order_management(order_ops)
    
    with tabs[4]:
        render_delivery_partner_management(delivery_partner_ops, user_ops)
    
    with tabs[5]:
        render_system_overview(user_ops, restaurant_ops, order_ops)

def render_user_management(user_ops):
    st.subheader("User Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Create User", "View Users", "Update User", "Delete User"])
    
    with tab1:
        with st.form("create_user"):
            st.markdown("#### Create New User")
            
            username = st.text_input("Username*")
            password = st.text_input("Password*", type="password")
            email = st.text_input("Email*")
            phone = st.text_input("Phone")
            address = st.text_area("Address")
            role = st.selectbox("Role*", ["system_admin", "restaurant_admin", "customer", "delivery_partner"])
            
            if st.form_submit_button("Create User", type="primary"):
                if username and password and email:
                    try:
                        user_ops.create(username, password, email, phone, address, role)
                        st.success(f"User '{username}' created successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error creating user: {str(e)}")
                else:
                    st.warning("Please fill all required fields")
    
    with tab2:
        users = user_ops.read_all()
        if users:
            st.dataframe(users, use_container_width=True)
        else:
            st.info("No users found")
    
    with tab3:
        users = user_ops.read_all()
        if users:
            user_options = {f"{u['username']} (ID: {u['id']}) - {u['role']}": u['id'] for u in users}
            selected_user = st.selectbox("Select User", list(user_options.keys()))
            
            if selected_user:
                user_id = user_options[selected_user]
                user = user_ops.read_by_id(user_id)
                
                if user:
                    with st.form("update_user"):
                        username = st.text_input("Username", value=user['username'])
                        password = st.text_input("Password", type="password", placeholder="Leave empty to keep current")
                        email = st.text_input("Email", value=user['email'])
                        phone = st.text_input("Phone", value=user['phone'] or "")
                        address = st.text_area("Address", value=user['address'] or "")
                        role = st.selectbox("Role", ["system_admin", "restaurant_admin", "customer", "delivery_partner"],
                                          index=["system_admin", "restaurant_admin", "customer", "delivery_partner"].index(user['role']))
                        
                        if st.form_submit_button("Update User"):
                            try:
                                user_ops.update(user_id, username, password or None, email, phone, address, role)
                                st.success("User updated successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error updating user: {str(e)}")
        else:
            st.info("No users available")
    
    with tab4:
        users = user_ops.read_all()
        if users:
            user_options = {f"{u['username']} (ID: {u['id']}) - {u['role']}": u['id'] for u in users}
            selected_user = st.selectbox("Select User to Delete", list(user_options.keys()))
            
            if st.button("Delete User", type="primary"):
                user_id = user_options[selected_user]
                try:
                    user_ops.delete(user_id)
                    st.success("User deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting user: {str(e)}")
        else:
            st.info("No users available")

def render_restaurant_management(restaurant_ops, user_ops):
    st.subheader("Restaurant Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Create Restaurant", "View Restaurants", "Update Restaurant", "Delete Restaurant"])
    
    with tab1:
        with st.form("create_restaurant"):
            st.markdown("#### Create New Restaurant")
            
            name = st.text_input("Restaurant Name*")
            address = st.text_area("Address*")
            phone = st.text_input("Phone")
            email = st.text_input("Email")
            cuisine_type = st.text_input("Cuisine Type")
            opening_hours = st.text_input("Opening Hours")
            
            admins = user_ops.read_by_role('restaurant_admin')
            admin_options = {f"{a['username']} (ID: {a['id']})": a['id'] for a in admins} if admins else {}
            
            if admin_options:
                selected_admin = st.selectbox("Restaurant Admin*", list(admin_options.keys()))
            else:
                st.warning("No restaurant admins available. Please create one first.")
                selected_admin = None
            
            if st.form_submit_button("Create Restaurant", type="primary"):
                if name and address and selected_admin:
                    try:
                        admin_id = admin_options[selected_admin]
                        restaurant_ops.create(name, address, phone, email, cuisine_type, opening_hours, admin_id)
                        st.success(f"Restaurant '{name}' created successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error creating restaurant: {str(e)}")
                else:
                    st.warning("Please fill all required fields")
    
    with tab2:
        restaurants = restaurant_ops.read_all()
        if restaurants:
            st.dataframe(restaurants, use_container_width=True)
        else:
            st.info("No restaurants found")
    
    with tab3:
        restaurants = restaurant_ops.read_all()
        if restaurants:
            restaurant_options = {f"{r['name']} (ID: {r['id']})": r['id'] for r in restaurants}
            selected_restaurant = st.selectbox("Select Restaurant", list(restaurant_options.keys()))
            
            if selected_restaurant:
                restaurant_id = restaurant_options[selected_restaurant]
                restaurant = restaurant_ops.read_by_id(restaurant_id)
                
                if restaurant:
                    with st.form("update_restaurant"):
                        name = st.text_input("Restaurant Name", value=restaurant['name'])
                        address = st.text_area("Address", value=restaurant['address'] or "")
                        phone = st.text_input("Phone", value=restaurant['phone'] or "")
                        email = st.text_input("Email", value=restaurant['email'] or "")
                        cuisine_type = st.text_input("Cuisine Type", value=restaurant['cuisine_type'] or "")
                        opening_hours = st.text_input("Opening Hours", value=restaurant['opening_hours'] or "")
                        is_active = st.checkbox("Active", value=bool(restaurant['is_active']))
                        
                        admins = user_ops.read_by_role('restaurant_admin')
                        admin_options = {f"{a['username']} (ID: {a['id']})": a['id'] for a in admins} if admins else {}
                        
                        if admin_options:
                            current_admin = next((k for k, v in admin_options.items() if v == restaurant['admin_id']), list(admin_options.keys())[0])
                            selected_admin = st.selectbox("Restaurant Admin", list(admin_options.keys()), 
                                                        index=list(admin_options.keys()).index(current_admin))
                        else:
                            selected_admin = None
                        
                        if st.form_submit_button("Update Restaurant"):
                            try:
                                admin_id = admin_options[selected_admin] if selected_admin else restaurant['admin_id']
                                restaurant_ops.update(restaurant_id, name, address, phone, email, cuisine_type, 
                                                    opening_hours, admin_id, is_active)
                                st.success("Restaurant updated successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error updating restaurant: {str(e)}")
        else:
            st.info("No restaurants available")
    
    with tab4:
        restaurants = restaurant_ops.read_all()
        if restaurants:
            restaurant_options = {f"{r['name']} (ID: {r['id']})": r['id'] for r in restaurants}
            selected_restaurant = st.selectbox("Select Restaurant to Delete", list(restaurant_options.keys()))
            
            if st.button("Delete Restaurant", type="primary"):
                restaurant_id = restaurant_options[selected_restaurant]
                try:
                    restaurant_ops.delete(restaurant_id)
                    st.success("Restaurant deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting restaurant: {str(e)}")
        else:
            st.info("No restaurants available")

def render_menu_item_management(menu_item_ops, restaurant_ops):
    st.subheader("Menu Item Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Create Menu Item", "View Menu Items", "Update Menu Item", "Delete Menu Item"])
    
    with tab1:
        with st.form("create_menu_item"):
            st.markdown("#### Create New Menu Item")
            
            restaurants = restaurant_ops.read_all()
            restaurant_options = {f"{r['name']} (ID: {r['id']})": r['id'] for r in restaurants} if restaurants else {}
            
            if restaurant_options:
                selected_restaurant = st.selectbox("Restaurant*", list(restaurant_options.keys()))
            else:
                st.warning("No restaurants available. Please create one first.")
                selected_restaurant = None
            
            name = st.text_input("Item Name*")
            description = st.text_area("Description")
            price = st.number_input("Price*", min_value=0.0, step=0.01)
            category = st.selectbox("Category", ["Appetizer", "Main Course", "Dessert", "Beverage", "Side", "Starter", "Other"])
            is_vegetarian = st.checkbox("Vegetarian", value=True)
            preparation_time = st.number_input("Preparation Time (minutes)", min_value=5, max_value=120, value=15)
            is_available = st.checkbox("Available", value=True)
            
            if st.form_submit_button("Create Menu Item", type="primary"):
                if selected_restaurant and name and price > 0:
                    try:
                        restaurant_id = restaurant_options[selected_restaurant]
                        menu_item_ops.create(restaurant_id, name, description, price, category, 
                                           is_vegetarian, preparation_time)
                        st.success(f"Menu item '{name}' created successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error creating menu item: {str(e)}")
                else:
                    st.warning("Please fill all required fields")
    
    with tab2:
        menu_items = menu_item_ops.read_all()
        if menu_items:
            st.dataframe(menu_items, use_container_width=True)
        else:
            st.info("No menu items found")
    
    with tab3:
        menu_items = menu_item_ops.read_all()
        if menu_items:
            item_options = {f"{item['name']} (ID: {item['id']}) - {item['restaurant_name']}": item['id'] for item in menu_items}
            selected_item = st.selectbox("Select Menu Item", list(item_options.keys()))
            
            if selected_item:
                item_id = item_options[selected_item]
                item = menu_item_ops.read_by_id(item_id)
                
                if item:
                    with st.form("update_menu_item"):
                        name = st.text_input("Item Name", value=item['name'])
                        description = st.text_area("Description", value=item['description'] or "")
                        price = st.number_input("Price", value=float(item['price']), min_value=0.0, step=0.01)
                        category = st.selectbox("Category", ["Appetizer", "Main Course", "Dessert", "Beverage", "Side", "Starter", "Other"],
                                              index=["Appetizer", "Main Course", "Dessert", "Beverage", "Side", "Starter", "Other"].index(item['category']) if item['category'] in ["Appetizer", "Main Course", "Dessert", "Beverage", "Side", "Starter", "Other"] else 6)
                        is_vegetarian = st.checkbox("Vegetarian", value=bool(item['is_vegetarian']))
                        preparation_time = st.number_input("Preparation Time (minutes)", min_value=5, max_value=120, value=int(item['preparation_time']))
                        is_available = st.checkbox("Available", value=bool(item['is_available']))
                        
                        if st.form_submit_button("Update Menu Item"):
                            try:
                                menu_item_ops.update(item_id, name, description, price, category, 
                                                   is_vegetarian, preparation_time, is_available)
                                st.success("Menu item updated successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error updating menu item: {str(e)}")
        else:
            st.info("No menu items available")
    
    with tab4:
        menu_items = menu_item_ops.read_all()
        if menu_items:
            item_options = {f"{item['name']} (ID: {item['id']}) - {item['restaurant_name']}": item['id'] for item in menu_items}
            selected_item = st.selectbox("Select Menu Item to Delete", list(item_options.keys()))
            
            if st.button("Delete Menu Item", type="primary"):
                item_id = item_options[selected_item]
                try:
                    menu_item_ops.delete(item_id)
                    st.success("Menu item deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting menu item: {str(e)}")
        else:
            st.info("No menu items available")

def render_order_management(order_ops):
    st.subheader("Order Management")
    
    orders = order_ops.read_all()
    
    if not orders:
        st.info("No orders found")
        return
    
    st.dataframe(orders, use_container_width=True)
    
    st.markdown("#### Order Details")
    
    order_options = {f"Order #{order['id']} - {order['customer_username']} - ₹{order['total_amount']:.2f}": order['id'] for order in orders}
    selected_order = st.selectbox("Select Order", list(order_options.keys()))
    
    if selected_order:
        order_id = order_options[selected_order]
        order = order_ops.read_by_id(order_id)
        
        if order:
            with st.expander("Full Order Details"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Order ID:** {order['id']}")
                    st.write(f"**Customer:** {order['customer_username']}")
                    st.write(f"**Restaurant:** {order['restaurant_name']}")
                    st.write(f"**Status:** {order['status'].replace('_', ' ').title()}")
                
                with col2:
                    st.write(f"**Total Amount:** ₹{order['total_amount']:.2f}")
                    st.write(f"**Payment Status:** {order['payment_status'].title()}")
                    st.write(f"**Payment Method:** {order['payment_method'] or 'Not specified'}")
                    st.write(f"**Delivery Partner:** {order['delivery_partner_username'] or 'Not assigned'}")
                
                st.write(f"**Delivery Address:** {order['delivery_address']}")
                st.write(f"**Created:** {order['created_at']}")
                
                order_items = order_ops.get_order_items(order_id)
                
                if order_items:
                    st.markdown("**Order Items:**")
                    for item in order_items:
                        st.write(f"- {item['item_name']} x{item['quantity']} = ₹{item['subtotal']:.2f}")
            
            st.markdown("#### Update Order Status")
            
            new_status = st.selectbox("New Status", ["pending", "confirmed", "preparing", "ready", "picked_up", "delivered", "cancelled"])
            
            if st.button("Update Status"):
                try:
                    order_ops.update_status(order_id, new_status)
                    st.success("Order status updated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error updating order status: {str(e)}")

def render_delivery_partner_management(delivery_partner_ops, user_ops):
    st.subheader("Delivery Partner Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Create Delivery Partner", "View Partners", "Update Partner", "Delete Partner"])
    
    with tab1:
        with st.form("create_delivery_partner"):
            st.markdown("#### Create New Delivery Partner")
            
            users = user_ops.read_by_role('delivery_partner')
            available_users = [u for u in users if not any(dp['user_id'] == u['id'] for dp in delivery_partner_ops.read_all())]
            user_options = {f"{u['username']} (ID: {u['id']})": u['id'] for u in available_users} if available_users else {}
            
            if user_options:
                selected_user = st.selectbox("User*", list(user_options.keys()))
            else:
                st.warning("No available delivery partner users. Please create a user with 'delivery_partner' role first.")
                selected_user = None
            
            vehicle_type = st.selectbox("Vehicle Type*", ["bike", "car", "bicycle"])
            vehicle_number = st.text_input("Vehicle Number*")
            license_number = st.text_input("License Number")
            
            if st.form_submit_button("Create Delivery Partner", type="primary"):
                if selected_user and vehicle_type and vehicle_number:
                    try:
                        user_id = user_options[selected_user]
                        delivery_partner_ops.create(user_id, vehicle_type, vehicle_number, license_number)
                        st.success("Delivery partner created successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error creating delivery partner: {str(e)}")
                else:
                    st.warning("Please fill all required fields")
    
    with tab2:
        partners = delivery_partner_ops.read_all()
        if partners:
            st.dataframe(partners, use_container_width=True)
        else:
            st.info("No delivery partners found")
    
    with tab3:
        partners = delivery_partner_ops.read_all()
        if partners:
            partner_options = {f"{p['username']} (ID: {p['id']})": p['id'] for p in partners}
            selected_partner = st.selectbox("Select Partner", list(partner_options.keys()))
            
            if selected_partner:
                partner_id = partner_options[selected_partner]
                partner = delivery_partner_ops.read_by_id(partner_id)
                
                if partner:
                    with st.form("update_partner"):
                        is_online = st.checkbox("Online", value=bool(partner['is_online']))
                        rating = st.number_input("Rating", value=float(partner['rating']), min_value=0.0, max_value=5.0, step=0.1)
                        
                        if st.form_submit_button("Update Partner"):
                            try:
                                delivery_partner_ops.update_online_status(partner_id, is_online)
                                delivery_partner_ops.update_rating(partner_id, rating)
                                st.success("Delivery partner updated successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error updating delivery partner: {str(e)}")
        else:
            st.info("No delivery partners available")
    
    with tab4:
        partners = delivery_partner_ops.read_all()
        if partners:
            partner_options = {f"{p['username']} (ID: {p['id']})": p['id'] for p in partners}
            selected_partner = st.selectbox("Select Partner to Delete", list(partner_options.keys()))
            
            if st.button("Delete Partner", type="primary"):
                partner_id = partner_options[selected_partner]
                try:
                    delivery_partner_ops.delete(partner_id)
                    st.success("Delivery partner deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting delivery partner: {str(e)}")
        else:
            st.info("No delivery partners available")

def render_system_overview(user_ops, restaurant_ops, order_ops):
    st.subheader("System Overview")
    
    users = user_ops.read_all()
    restaurants = restaurant_ops.read_all()
    orders = order_ops.read_all()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Users", len(users))
        
        role_counts = {}
        for user in users:
            role = user['role']
            role_counts[role] = role_counts.get(role, 0) + 1
        
        st.markdown("**Users by Role:**")
        for role, count in role_counts.items():
            st.write(f"- {role.replace('_', ' ').title()}: {count}")
    
    with col2:
        st.metric("Total Restaurants", len(restaurants))
        
        active_restaurants = len([r for r in restaurants if r['is_active']])
        st.write(f"Active Restaurants: {active_restaurants}")
        
        if restaurants:
            avg_rating = sum(r['rating'] for r in restaurants) / len(restaurants)
            st.write(f"Average Rating: {avg_rating:.1f} ⭐")
    
    with col3:
        st.metric("Total Orders", len(orders))
        
        if orders:
            total_revenue = sum(order['total_amount'] for order in orders if order['payment_status'] == 'paid')
            st.write(f"Total Revenue: ₹{total_revenue:.2f}")
            
            avg_order_value = total_revenue / len(orders) if orders else 0
            st.write(f"Average Order Value: ₹{avg_order_value:.2f}")
    
    st.markdown("#### Recent Orders")
    
    recent_orders = sorted(orders, key=lambda x: x['created_at'], reverse=True)[:5]
    
    if recent_orders:
        for order in recent_orders:
            st.write(f"**Order #{order['id']}** - {order['customer_username']} - {order['restaurant_name']} - ₹{order['total_amount']:.2f} - {order['status'].replace('_', ' ').title()}")
    else:
        st.info("No recent orders")
