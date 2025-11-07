import streamlit as st
from typing import Dict, Any

def render_customer_view(user_ops, restaurant_ops, menu_item_ops, order_ops, cart_ops, rating_ops):
    st.header("Food Delivery - Customer View")
    
    if 'current_customer_id' not in st.session_state:
        st.session_state.current_customer_id = 6  # Default customer for demo
    
    customer_id = st.session_state.current_customer_id
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Browse Food", "Cart", "My Orders", "Rate & Review", "Profile"])
    
    with tab1:
        render_food_browsing(restaurant_ops, menu_item_ops, cart_ops, customer_id)
    
    with tab2:
        render_cart(cart_ops, order_ops, customer_id)
    
    with tab3:
        render_customer_orders(order_ops, customer_id)
    
    with tab4:
        render_ratings(rating_ops, restaurant_ops, menu_item_ops, customer_id)
    
    with tab5:
        render_customer_profile(user_ops, customer_id)

def render_food_browsing(restaurant_ops, menu_item_ops, cart_ops, customer_id):
    st.subheader("Browse Restaurants & Menu")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_term = st.text_input("Search for food or restaurants...")
        
    with col2:
        filter_veg = st.checkbox("Vegetarian Only")
        filter_category = st.selectbox("Category", ["All", "Appetizer", "Main Course", "Dessert", "Beverage", "Side", "Starter"])
    
    restaurants = restaurant_ops.read_all()
    if not restaurants:
        st.info("No restaurants available")
        return
    
    selected_restaurant = st.selectbox(
        "Select Restaurant",
        options=[r['name'] for r in restaurants],
        index=0
    )
    
    restaurant = next(r for r in restaurants if r['name'] == selected_restaurant)
    
    st.markdown(f"### {restaurant['name']}")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.write(f"**Cuisine:** {restaurant['cuisine_type'] or 'Not specified'}")
    with col_b:
        st.write(f"**Rating:** {restaurant['rating']} ({'★' * int(restaurant['rating'])})")
    with col_c:
        st.write(f"**Hours:** {restaurant['opening_hours'] or 'Not specified'}")
    
    menu_items = menu_item_ops.read_available_by_restaurant(restaurant['id'])
    
    if not menu_items:
        st.info("No menu items available")
        return
    
    if filter_veg:
        menu_items = [item for item in menu_items if item['is_vegetarian']]
    
    if filter_category != "All":
        menu_items = [item for item in menu_items if item['category'] == filter_category]
    
    if search_term:
        search_term = search_term.lower()
        menu_items = [item for item in menu_items if search_term in item['name'].lower()]
    
    st.markdown("#### Menu Items")
    
    for item in menu_items:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                veg_indicator = "[Veg]" if item['is_vegetarian'] else "[Non-Veg]"
                st.markdown(f"**{veg_indicator} {item['name']}**")
                st.write(item['description'] or "No description available")
                st.write(f"Category: {item['category'] or 'Not specified'}")
            
            with col2:
                st.markdown(f"**₹{item['price']:.2f}**")
                st.write(f"Time: {item['preparation_time']} min")
            
            with col3:
                quantity = st.number_input(
                    "Qty",
                    min_value=1,
                    max_value=10,
                    value=1,
                    key=f"qty_{item['id']}"
                )
            
            with col4:
                if st.button("Add to Cart", key=f"add_{item['id']}"):
                    cart_ops.add_item(customer_id, item['id'], quantity)
                    st.success(f"Added {quantity} x {item['name']} to cart!")
                    st.rerun()
            
            st.divider()

def render_cart(cart_ops, order_ops, customer_id):
    st.subheader("Your Cart")
    
    cart_items = cart_ops.get_cart(customer_id)
    
    if not cart_items:
        st.info("Your cart is empty")
        return
    
    total_amount = cart_ops.get_cart_total(customer_id)
    
    st.markdown("#### Cart Items")
    
    for item in cart_items:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.markdown(f"**{item['item_name']}**")
            st.write(f"From: {item['restaurant_name']}")
        
        with col2:
            st.write(f"₹{item['price']:.2f}")
        
        with col3:
            new_quantity = st.number_input(
                "Quantity",
                min_value=0,
                max_value=10,
                value=item['quantity'],
                key=f"cart_qty_{item['id']}"
            )
            
            if new_quantity != item['quantity']:
                cart_ops.update_quantity(customer_id, item['menu_item_id'], new_quantity)
                st.rerun()
        
        with col4:
            if st.button("Remove", key=f"remove_{item['id']}"):
                cart_ops.remove_item(customer_id, item['menu_item_id'])
                st.rerun()
        
        st.divider()
    
    st.markdown(f"### Total: ₹{total_amount:.2f}")
    
    with st.form("checkout_form"):
        st.subheader("Delivery Information")
        delivery_address = st.text_area("Delivery Address*", height=100)
        payment_method = st.selectbox("Payment Method*", ["Cash", "Credit Card", "Debit Card", "UPI", "Net Banking"])
        
        if st.form_submit_button("Place Order", type="primary"):
            if not delivery_address:
                st.error("Please provide delivery address")
            else:
                try:
                    restaurant_id = cart_items[0]['restaurant_id']
                    order_id = order_ops.create(customer_id, restaurant_id, delivery_address, total_amount, payment_method)
                    
                    for item in cart_items:
                        order_ops.add_item(order_id, item['menu_item_id'], item['quantity'], item['price'])
                    
                    cart_ops.clear_cart(customer_id)
                    st.success(f"Order placed successfully! Order ID: {order_id}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error placing order: {str(e)}")

def render_customer_orders(order_ops, customer_id):
    st.subheader("Your Orders")
    
    orders = order_ops.read_by_customer(customer_id)
    
    if not orders:
        st.info("No orders found")
        return
    
    for order in orders:
        with st.expander(f"Order #{order['id']} - {order['restaurant_name']} - ₹{order['total_amount']:.2f}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Status:** {order['status'].replace('_', ' ').title()}")
                st.write(f"**Payment:** {order['payment_status'].title()}")
                st.write(f"**Method:** {order['payment_method'] or 'Not specified'}")
            
            with col2:
                st.write(f"**Delivery Address:**")
                st.write(order['delivery_address'])
            
            with col3:
                if order['estimated_delivery_time']:
                    st.write(f"**Estimated:** {order['estimated_delivery_time']}")
                if order['actual_delivery_time']:
                    st.write(f"**Delivered:** {order['actual_delivery_time']}")
            
            order_items = order_ops.get_order_items(order['id'])
            
            if order_items:
                st.markdown("**Order Items:**")
                for item in order_items:
                    st.write(f"- {item['item_name']} x{item['quantity']} = ₹{item['subtotal']:.2f}")

def render_ratings(rating_ops, restaurant_ops, menu_item_ops, customer_id):
    st.subheader("Rate & Review")
    
    tab_restaurant, tab_items = st.tabs(["Rate Restaurants", "Rate Food Items"])
    
    with tab_restaurant:
        restaurants = restaurant_ops.read_all()
        if restaurants:
            selected_restaurant = st.selectbox(
                "Select Restaurant",
                options=[(r['id'], r['name']) for r in restaurants],
                format_func=lambda x: x[1]
            )
            
            restaurant_id = selected_restaurant[0]
            
            with st.form("rate_restaurant"):
                rating = st.slider("Rating", 1, 5, 5)
                review = st.text_area("Review (optional)")
                
                if st.form_submit_button("Submit Rating"):
                    try:
                        rating_ops.create_restaurant_rating(restaurant_id, customer_id, rating, review)
                        st.success("Rating submitted successfully!")
                    except Exception as e:
                        st.error(f"Error submitting rating: {str(e)}")
            
            existing_ratings = rating_ops.get_restaurant_ratings(restaurant_id)
            if existing_ratings:
                st.markdown("#### Recent Reviews")
                for rating in existing_ratings[:5]:
                    st.write(f"**{'★' * rating['rating']}** - {rating['customer_username']}")
                    if rating['review']:
                        st.write(f"_{rating['review']}_")
                    st.divider()
    
    with tab_items:
        menu_items = menu_item_ops.read_all()
        if menu_items:
            selected_item = st.selectbox(
                "Select Food Item",
                options=[(item['id'], f"{item['name']} - {item['restaurant_name']}") for item in menu_items],
                format_func=lambda x: x[1]
            )
            
            item_id = selected_item[0]
            
            with st.form("rate_item"):
                rating = st.slider("Rating", 1, 5, 5)
                review = st.text_area("Review (optional)")
                
                if st.form_submit_button("Submit Rating"):
                    try:
                        rating_ops.create_item_rating(item_id, customer_id, rating, review)
                        st.success("Rating submitted successfully!")
                    except Exception as e:
                        st.error(f"Error submitting rating: {str(e)}")
            
            existing_ratings = rating_ops.get_item_ratings(item_id)
            if existing_ratings:
                st.markdown("#### Recent Reviews")
                for rating in existing_ratings[:5]:
                    st.write(f"**{'★' * rating['rating']}** - {rating['customer_username']}")
                    if rating['review']:
                        st.write(f"_{rating['review']}_")
                    st.divider()

def render_customer_profile(user_ops, customer_id):
    st.subheader("My Profile")
    
    customer = user_ops.read_by_id(customer_id)
    
    if customer:
        with st.form("update_profile"):
            username = st.text_input("Username", value=customer['username'])
            email = st.text_input("Email", value=customer['email'])
            phone = st.text_input("Phone", value=customer['phone'] or "")
            address = st.text_area("Address", value=customer['address'] or "")
            
            if st.form_submit_button("Update Profile"):
                try:
                    user_ops.update(customer_id, username=username, email=email, phone=phone, address=address)
                    st.success("Profile updated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error updating profile: {str(e)}")
        
        st.markdown("#### Account Information")
        st.write(f"**User ID:** {customer['id']}")
        st.write(f"**Role:** {customer['role'].replace('_', ' ').title()}")
        st.write(f"**Member Since:** {customer['created_at']}")
