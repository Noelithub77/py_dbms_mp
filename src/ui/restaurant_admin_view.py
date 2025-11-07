import streamlit as st
from typing import Dict, Any

def render_restaurant_admin_view(user_ops, restaurant_ops, menu_item_ops, order_ops, rating_ops):
    st.header("Restaurant Admin View")
    
    if 'current_restaurant_admin_id' not in st.session_state:
        st.session_state.current_restaurant_admin_id = 2  # Default restaurant admin for demo
    
    admin_id = st.session_state.current_restaurant_admin_id
    
    admin_restaurants = restaurant_ops.read_by_admin(admin_id)
    
    if not admin_restaurants:
        st.error("No restaurants assigned to this admin")
        return
    
    if len(admin_restaurants) == 1:
        selected_restaurant = admin_restaurants[0]
    else:
        restaurant_names = [r['name'] for r in admin_restaurants]
        selected_name = st.selectbox("Select Restaurant", restaurant_names)
        selected_restaurant = next(r for r in admin_restaurants if r['name'] == selected_name)
    
    st.markdown(f"### Managing: {selected_restaurant['name']}")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Menu Management", "Orders", "Restaurant Info", "Ratings & Reviews", "Analytics"])
    
    with tab1:
        render_menu_management(menu_item_ops, selected_restaurant['id'])
    
    with tab2:
        render_restaurant_orders(order_ops, selected_restaurant['id'])
    
    with tab3:
        render_restaurant_info(restaurant_ops, selected_restaurant)
    
    with tab4:
        render_restaurant_ratings(rating_ops, selected_restaurant['id'])
    
    with tab5:
        render_analytics(order_ops, menu_item_ops, selected_restaurant['id'])

def render_menu_management(menu_item_ops, restaurant_id):
    st.subheader("Menu Management")
    
    tab_add, tab_view, tab_edit = st.tabs(["Add Item", "View Menu", "Edit Items"])
    
    with tab_add:
        with st.form("add_menu_item"):
            st.markdown("#### Add New Menu Item")
            
            name = st.text_input("Item Name*")
            description = st.text_area("Description")
            price = st.number_input("Price*", min_value=0.0, step=0.01)
            category = st.selectbox("Category", ["Appetizer", "Main Course", "Dessert", "Beverage", "Side", "Starter", "Other"])
            is_vegetarian = st.checkbox("Vegetarian", value=True)
            preparation_time = st.number_input("Preparation Time (minutes)", min_value=5, max_value=120, value=15)
            is_available = st.checkbox("Available", value=True)
            
            if st.form_submit_button("Add Item", type="primary"):
                if name and price > 0:
                    try:
                        menu_item_ops.create(
                            restaurant_id, name, description, price, 
                            category, is_vegetarian, preparation_time
                        )
                        st.success(f"Item '{name}' added successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error adding item: {str(e)}")
                else:
                    st.warning("Please fill in all required fields")
    
    with tab_view:
        menu_items = menu_item_ops.read_by_restaurant(restaurant_id)
        
        if not menu_items:
            st.info("No menu items found")
            return
        
        st.markdown("#### Current Menu")
        
        for item in menu_items:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                veg_indicator = "[Veg]" if item['is_vegetarian'] else "[Non-Veg]"
                availability = "[Available]" if item['is_available'] else "[Unavailable]"
                st.markdown(f"**{veg_indicator} {availability} {item['name']}**")
                st.write(item['description'] or "No description")
                st.write(f"Category: {item['category'] or 'Not specified'}")
            
            with col2:
                st.markdown(f"**₹{item['price']:.2f}**")
            
            with col3:
                st.write(f"Time: {item['preparation_time']} min")
            
            with col4:
                st.write(f"ID: {item['id']}")
            
            st.divider()
    
    with tab_edit:
        menu_items = menu_item_ops.read_by_restaurant(restaurant_id)
        
        if not menu_items:
            st.info("No menu items to edit")
            return
        
        item_options = {f"{item['name']} (ID: {item['id']})": item['id'] for item in menu_items}
        selected_item_name = st.selectbox("Select Item to Edit", list(item_options.keys()))
        
        if selected_item_name:
            item_id = item_options[selected_item_name]
            item = menu_item_ops.read_by_id(item_id)
            
            if item:
                with st.form("edit_menu_item"):
                    name = st.text_input("Item Name", value=item['name'])
                    description = st.text_area("Description", value=item['description'] or "")
                    price = st.number_input("Price", value=float(item['price']), min_value=0.0, step=0.01)
                    category = st.selectbox("Category", ["Appetizer", "Main Course", "Dessert", "Beverage", "Side", "Starter", "Other"], 
                                          index=["Appetizer", "Main Course", "Dessert", "Beverage", "Side", "Starter", "Other"].index(item['category']) if item['category'] in ["Appetizer", "Main Course", "Dessert", "Beverage", "Side", "Starter", "Other"] else 6)
                    is_vegetarian = st.checkbox("Vegetarian", value=bool(item['is_vegetarian']))
                    preparation_time = st.number_input("Preparation Time (minutes)", min_value=5, max_value=120, value=int(item['preparation_time']))
                    is_available = st.checkbox("Available", value=bool(item['is_available']))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Update Item"):
                            try:
                                menu_item_ops.update(
                                    item_id, name, description, price, category, 
                                    is_vegetarian, preparation_time, is_available
                                )
                                st.success("Item updated successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error updating item: {str(e)}")
                    
                    with col2:
                        if st.form_submit_button("Delete Item", type="secondary"):
                            try:
                                menu_item_ops.delete(item_id)
                                st.success("Item deleted successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error deleting item: {str(e)}")

def render_restaurant_orders(order_ops, restaurant_id):
    st.subheader("Restaurant Orders")
    
    orders = order_ops.read_by_restaurant(restaurant_id)
    
    if not orders:
        st.info("No orders found")
        return
    
    status_filter = st.selectbox("Filter by Status", ["All", "pending", "confirmed", "preparing", "ready", "picked_up", "delivered", "cancelled"])
    
    if status_filter != "All":
        orders = [order for order in orders if order['status'] == status_filter]
    
    for order in orders:
        with st.expander(f"Order #{order['id']} - {order['customer_username']} - ₹{order['total_amount']:.2f} - {order['status'].replace('_', ' ').title()}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Customer:** {order['customer_username']}")
                st.write(f"**Status:** {order['status'].replace('_', ' ').title()}")
                st.write(f"**Payment:** {order['payment_status'].title()}")
                st.write(f"**Method:** {order['payment_method'] or 'Not specified'}")
            
            with col2:
                st.write(f"**Delivery Address:**")
                st.write(order['delivery_address'])
                if order['delivery_partner_username']:
                    st.write(f"**Delivery Partner:** {order['delivery_partner_username']}")
            
            order_items = order_ops.get_order_items(order['id'])
            
            if order_items:
                st.markdown("**Order Items:**")
                for item in order_items:
                    st.write(f"- {item['item_name']} x{item['quantity']} = ₹{item['subtotal']:.2f}")
            
            st.markdown("**Update Order Status:**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Confirm", key=f"confirm_{order['id']}", disabled=order['status'] != 'pending'):
                    order_ops.update_status(order['id'], 'confirmed')
                    st.rerun()
            
            with col2:
                if st.button("Start Preparing", key=f"prepare_{order['id']}", disabled=order['status'] != 'confirmed'):
                    order_ops.update_status(order['id'], 'preparing')
                    st.rerun()
            
            with col3:
                if st.button("Ready for Pickup", key=f"ready_{order['id']}", disabled=order['status'] != 'preparing'):
                    order_ops.update_status(order['id'], 'ready')
                    st.rerun()
            
            if order['status'] in ['ready', 'picked_up', 'delivered']:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Mark Picked Up", key=f"picked_{order['id']}", disabled=order['status'] not in ['ready']):
                        order_ops.update_status(order['id'], 'picked_up')
                        st.rerun()
                with col2:
                    if st.button("Mark Delivered", key=f"delivered_{order['id']}", disabled=order['status'] not in ['picked_up']):
                        order_ops.update_status(order['id'], 'delivered')
                        st.rerun()

def render_restaurant_info(restaurant_ops, restaurant):
    st.subheader("Restaurant Information")
    
    with st.form("update_restaurant_info"):
        name = st.text_input("Restaurant Name", value=restaurant['name'])
        address = st.text_area("Address", value=restaurant['address'] or "")
        phone = st.text_input("Phone", value=restaurant['phone'] or "")
        email = st.text_input("Email", value=restaurant['email'] or "")
        cuisine_type = st.text_input("Cuisine Type", value=restaurant['cuisine_type'] or "")
        opening_hours = st.text_input("Opening Hours", value=restaurant['opening_hours'] or "")
        is_active = st.checkbox("Restaurant Active", value=bool(restaurant['is_active']))
        
        if st.form_submit_button("Update Restaurant Info"):
            try:
                restaurant_ops.update(
                    restaurant['id'], name, address, phone, email, 
                    cuisine_type, opening_hours, restaurant['admin_id'], is_active
                )
                st.success("Restaurant information updated successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error updating restaurant: {str(e)}")
    
    st.markdown("#### Current Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Restaurant ID:** {restaurant['id']}")
        st.write(f"**Admin ID:** {restaurant['admin_id']}")
        st.write(f"**Current Rating:** {restaurant['rating']} ({'★' * int(restaurant['rating'])})")
        st.write(f"**Status:** {'Active' if restaurant['is_active'] else 'Inactive'}")
    
    with col2:
        st.write(f"**Created:** {restaurant['created_at']}")

def render_restaurant_ratings(rating_ops, restaurant_id):
    st.subheader("Ratings & Reviews")
    
    ratings = rating_ops.get_restaurant_ratings(restaurant_id)
    
    if not ratings:
        st.info("No ratings yet")
        return
    
    avg_rating = rating_ops.get_restaurant_average_rating(restaurant_id)
    
    st.markdown(f"### Average Rating: {avg_rating:.1f} ({'★' * int(avg_rating)})")
    
    st.markdown("#### Customer Reviews")
    
    for rating in ratings:
        with st.expander(f"{'★' * rating['rating']} - {rating['customer_username']} - {rating['created_at']}"):
            if rating['review']:
                st.write(rating['review'])
            else:
                st.write("No review provided")

def render_analytics(order_ops, menu_item_ops, restaurant_id):
    st.subheader("Restaurant Analytics")
    
    orders = order_ops.read_by_restaurant(restaurant_id)
    menu_items = menu_item_ops.read_by_restaurant(restaurant_id)
    
    if not orders:
        st.info("No orders to analyze")
        return
    
    total_orders = len(orders)
    total_revenue = sum(order['total_amount'] for order in orders if order['payment_status'] == 'paid')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Orders", total_orders)
    
    with col2:
        st.metric("Total Revenue", f"₹{total_revenue:.2f}")
    
    with col3:
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        st.metric("Average Order Value", f"₹{avg_order_value:.2f}")
    
    st.markdown("#### Order Status Distribution")
    
    status_counts = {}
    for order in orders:
        status = order['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    for status, count in status_counts.items():
        st.write(f"**{status.replace('_', ' ').title()}:** {count}")
    
    st.markdown("#### Popular Items")
    
    item_sales = {}
    for order in orders:
        order_items = order_ops.get_order_items(order['id'])
        for item in order_items:
            item_name = item['item_name']
            item_sales[item_name] = item_sales.get(item_name, 0) + item['quantity']
    
    if item_sales:
        sorted_items = sorted(item_sales.items(), key=lambda x: x[1], reverse=True)
        for item_name, quantity in sorted_items[:10]:
            st.write(f"**{item_name}:** {quantity} sold")
