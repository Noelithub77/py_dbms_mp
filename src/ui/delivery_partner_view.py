import streamlit as st
from typing import Dict, Any

def render_delivery_partner_view(user_ops, order_ops, delivery_partner_ops):
    st.header("Delivery Partner View")
    
    if 'current_delivery_partner_id' not in st.session_state:
        st.session_state.current_delivery_partner_id = 1  # Default delivery partner for demo
    
    partner_id = st.session_state.current_delivery_partner_id
    partner = delivery_partner_ops.read_by_id(partner_id)
    
    if not partner:
        st.error("Delivery partner not found")
        return
    
    st.markdown(f"### Welcome, {partner['username']}!")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Deliveries", partner['total_deliveries'])
    
    with col2:
        st.metric("Rating", f"{partner['rating']:.1f} ({'★' * int(partner['rating'])})")
    
    with col3:
        status = "[Online]" if partner['is_online'] else "[Offline]"
        st.metric("Status", status)
    
    with col4:
        st.metric("Vehicle", partner['vehicle_type'].title())
    
    tab1, tab2, tab3, tab4 = st.tabs(["Available Orders", "My Orders", "Profile", "Earnings"])
    
    with tab1:
        render_available_orders(order_ops, delivery_partner_ops, partner_id)
    
    with tab2:
        render_my_orders(order_ops, partner_id)
    
    with tab3:
        render_partner_profile(user_ops, delivery_partner_ops, partner)
    
    with tab4:
        render_earnings(order_ops, partner_id)

def render_available_orders(order_ops, delivery_partner_ops, partner_id):
    st.subheader("Available Orders")
    
    partner = delivery_partner_ops.read_by_id(partner_id)
    
    if not partner['is_online']:
        st.warning("You are currently offline. Go online to see available orders.")
        return
    
    if st.button("Go Offline", type="secondary"):
        delivery_partner_ops.update_online_status(partner_id, False)
        st.rerun()
    
    orders = order_ops.read_all()
    available_orders = [order for order in orders if order['status'] == 'confirmed' and not order['delivery_partner_id']]
    
    if not available_orders:
        st.info("No orders available for pickup")
        return
    
    st.markdown(f"#### {len(available_orders)} Orders Available")
    
    for order in available_orders:
        with st.expander(f"Order #{order['id']} - {order['restaurant_name']} - ₹{order['total_amount']:.2f}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Customer:** {order['customer_username']}")
                st.write(f"**Restaurant:** {order['restaurant_name']}")
                st.write(f"**Total Amount:** ₹{order['total_amount']:.2f}")
                st.write(f"**Payment:** {order['payment_status'].title()}")
            
            with col2:
                st.write(f"**Delivery Address:**")
                st.write(order['delivery_address'])
                st.write(f"**Order Time:** {order['created_at']}")
            
            order_items = order_ops.get_order_items(order['id'])
            
            if order_items:
                st.markdown("**Order Items:**")
                for item in order_items:
                    st.write(f"- {item['item_name']} x{item['quantity']} = ₹{item['subtotal']:.2f}")
            
            if st.button("Accept Order", key=f"accept_{order['id']}", type="primary"):
                try:
                    order_ops.assign_delivery_partner(order['id'], partner_id)
                    st.success(f"Order #{order['id']} assigned to you!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error accepting order: {str(e)}")

def render_my_orders(order_ops, partner_id):
    st.subheader("My Orders")
    
    orders = order_ops.read_by_delivery_partner(partner_id)
    
    if not orders:
        st.info("No orders assigned to you")
        return
    
    status_filter = st.selectbox("Filter by Status", ["All", "confirmed", "preparing", "ready", "picked_up", "delivered"])
    
    if status_filter != "All":
        orders = [order for order in orders if order['status'] == status_filter]
    
    for order in orders:
        with st.expander(f"Order #{order['id']} - {order['restaurant_name']} → {order['customer_username']} - ₹{order['total_amount']:.2f}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Status:** {order['status'].replace('_', ' ').title()}")
                st.write(f"**Restaurant:** {order['restaurant_name']}")
                st.write(f"**Customer:** {order['customer_username']}")
                st.write(f"**Payment:** {order['payment_status'].title()}")
            
            with col2:
                st.write(f"**Delivery Address:**")
                st.write(order['delivery_address'])
                st.write(f"**Order Time:** {order['created_at']}")
            
            order_items = order_ops.get_order_items(order['id'])
            
            if order_items:
                st.markdown("**Order Items:**")
                for item in order_items:
                    st.write(f"- {item['item_name']} x{item['quantity']} = ₹{item['subtotal']:.2f}")
            
            st.markdown("**Update Order Status:**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Pick Up Order", key=f"pickup_{order['id']}", 
                           disabled=order['status'] not in ['confirmed', 'preparing', 'ready']):
                    order_ops.update_status(order['id'], 'picked_up')
                    st.success("Order picked up!")
                    st.rerun()
            
            with col2:
                if st.button("On the Way", key=f"onway_{order['id']}", 
                           disabled=order['status'] != 'picked_up'):
                    order_ops.update_status(order['id'], 'picked_up')  # Keep as picked_up for simplicity
                    st.success("Updated status!")
                    st.rerun()
            
            with col3:
                if st.button("Mark Delivered", key=f"delivered_{order['id']}", 
                           disabled=order['status'] not in ['picked_up']):
                    order_ops.update_status(order['id'], 'delivered')
                    st.success("Order delivered! Great job!")
                    st.rerun()

def render_partner_profile(user_ops, delivery_partner_ops, partner):
    st.subheader("My Profile")
    
    user = user_ops.read_by_id(partner['user_id'])
    
    if user:
        with st.form("update_profile"):
            st.markdown("#### Personal Information")
            
            username = st.text_input("Username", value=user['username'], disabled=True)
            email = st.text_input("Email", value=user['email'])
            phone = st.text_input("Phone", value=user['phone'] or "")
            address = st.text_area("Address", value=user['address'] or "")
            
            st.markdown("#### Vehicle Information")
            
            vehicle_type = st.selectbox("Vehicle Type", ["bike", "car", "bicycle"], 
                                      index=["bike", "car", "bicycle"].index(partner['vehicle_type']))
            vehicle_number = st.text_input("Vehicle Number", value=partner['vehicle_number'])
            license_number = st.text_input("License Number", value=partner['license_number'] or "")
            
            if st.form_submit_button("Update Profile"):
                try:
                    user_ops.update(partner['user_id'], email=email, phone=phone, address=address)
                    st.success("Profile updated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error updating profile: {str(e)}")
    
    st.markdown("#### Account Statistics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Partner ID:** {partner['id']}")
        st.write(f"**User ID:** {partner['user_id']}")
        st.write(f"**Total Deliveries:** {partner['total_deliveries']}")
    
    with col2:
        st.write(f"**Current Rating:** {partner['rating']:.1f} ({'★' * int(partner['rating'])})")
        st.write(f"**Vehicle:** {partner['vehicle_type'].title()}")
        st.write(f"**Member Since:** {partner['created_at']}")
    
    st.markdown("#### Online Status")
    
    if partner['is_online']:
        st.success("You are currently online and available for orders")
        if st.button("Go Offline", type="secondary"):
            delivery_partner_ops.update_online_status(partner['id'], False)
            st.rerun()
    else:
        st.warning("You are currently offline")
        if st.button("Go Online", type="primary"):
            delivery_partner_ops.update_online_status(partner['id'], True)
            st.rerun()
    
    st.markdown("#### Location Update")
    
    with st.form("update_location"):
        st.write("Update your current location for better order assignments")
        
        col1, col2 = st.columns(2)
        with col1:
            latitude = st.number_input("Latitude", value=12.9716, format="%.6f")
        with col2:
            longitude = st.number_input("Longitude", value=77.5946, format="%.6f")
        
        if st.form_submit_button("Update Location"):
            try:
                delivery_partner_ops.update_location(partner['id'], latitude, longitude)
                st.success("Location updated successfully!")
            except Exception as e:
                st.error(f"Error updating location: {str(e)}")

def render_earnings(order_ops, partner_id):
    st.subheader("My Earnings")
    
    orders = order_ops.read_by_delivery_partner(partner_id)
    delivered_orders = [order for order in orders if order['status'] == 'delivered' and order['payment_status'] == 'paid']
    
    if not delivered_orders:
        st.info("No delivered orders found")
        return
    
    total_earnings = 0
    total_deliveries = len(delivered_orders)
    
    st.markdown("#### Earnings Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Deliveries", total_deliveries)
    
    with col2:
        estimated_earnings = total_deliveries * 40  # Assuming ₹40 per delivery
        st.metric("Estimated Earnings", f"₹{estimated_earnings:.2f}")
    
    with col3:
        avg_per_delivery = estimated_earnings / total_deliveries if total_deliveries > 0 else 0
        st.metric("Avg per Delivery", f"₹{avg_per_delivery:.2f}")
    
    st.markdown("#### Recent Deliveries")
    
    recent_deliveries = sorted(delivered_orders, key=lambda x: x['created_at'], reverse=True)[:10]
    
    if recent_deliveries:
        for order in recent_deliveries:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**Order #{order['id']}** - {order['restaurant_name']} → {order['customer_username']}")
            
            with col2:
                st.write(f"₹{order['total_amount']:.2f}")
            
            with col3:
                st.write(f"₹40.00")
            
            st.write(f"Delivered on: {order['created_at']}")
            st.divider()
    else:
        st.info("No recent deliveries")
    
    st.markdown("#### Payment Information")
    
    st.info("Payment is processed weekly. Current week's earnings will be added to your account.")
    
    with st.expander("Payment Details"):
        st.write("**Payment Rate:** ₹40 per delivery")
        st.write("**Payment Cycle:** Weekly (Every Monday)")
        st.write("**Payment Method:** Bank transfer to registered account")
        st.write("**Minimum Payout:** ₹500")
        
        if estimated_earnings < 500:
            st.warning(f"Current earnings (₹{estimated_earnings:.2f}) are below minimum payout threshold. They will be carried forward to next week.")
        else:
            st.success(f"Current earnings (₹{estimated_earnings:.2f}) will be processed in next payment cycle.")
