

-- System Admin
INSERT INTO Users (username, password, email, phone, address, role) VALUES
('noel_admin', 'admin123', 'noel@fooddelivery.com', '9876543210', '123 Admin Street, Bangalore', 'system_admin');

-- Restaurant Admins
INSERT INTO Users (username, password, email, phone, address, role) VALUES
('jishnu_anand', 'rest123', 'jishnu@anandbhavan.com', '9876543211', '456 Restaurant Ave, Bangalore', 'restaurant_admin'),
('omshukla_kfc', 'rest123', 'om@kfcindia.com', '9876543212', '789 Food Court, Bangalore', 'restaurant_admin'),
('shubhom_dominos', 'rest123', 'shubhom@dominos.in', '9876543213', '321 Culinary Road, Bangalore', 'restaurant_admin'),
('noel_pizza', 'rest123', 'noel@pizzahut.in', '9876543214', '654 Asian Street, Bangalore', 'restaurant_admin');

-- Customers
INSERT INTO Users (username, password, email, phone, address, role) VALUES
('rahul_sharma', 'cust123', 'rahul.sharma@email.com', '9876543221', '123 Customer Lane, Bangalore', 'customer'),
('priya_patel', 'cust123', 'priya.patel@email.com', '9876543222', '456 User Avenue, Bangalore', 'customer'),
('amit_kumar', 'cust123', 'amit.kumar@email.com', '9876543223', '789 Patron Road, Bangalore', 'customer'),
('sneha_reddy', 'cust123', 'sneha.reddy@email.com', '9876543224', '321 Guest Street, Bangalore', 'customer'),
('vikram_singh', 'cust123', 'vikram.singh@email.com', '9876543225', '654 Client Boulevard, Bangalore', 'customer');

-- Delivery Partners
INSERT INTO Users (username, password, email, phone, address, role) VALUES
('rajesh_delivery', 'del123', 'rajesh.rider@delivery.com', '9876543231', '111 Delivery Point, Bangalore', 'delivery_partner'),
('suresh_rider', 'del123', 'suresh.rider@delivery.com', '9876543232', '222 Rider Street, Bangalore', 'delivery_partner'),
('mukesh_delivery', 'del123', 'mukesh.rider@delivery.com', '9876543233', '333 Transport Avenue, Bangalore', 'delivery_partner');

-- Restaurants
INSERT INTO Restaurants (name, address, phone, email, cuisine_type, opening_hours, rating, admin_id) VALUES
('Anand Bhavan', 'MG Road, Bangalore', '0801234561', 'info@anandbhavan.com', 'South Indian', '08:00 AM - 10:30 PM', 4.5, 2),
('KFC', 'Brigade Road, Bangalore', '0801234562', 'info@kfcindia.com', 'Fast Food', '11:00 AM - 11:00 PM', 4.3, 3),
('Domino''s Pizza', 'Indiranagar, Bangalore', '0801234563', 'info@dominos.in', 'Pizza', '11:00 AM - 12:00 AM', 4.7, 4),
('Pizza Hut', 'Koramangala, Bangalore', '0801234564', 'info@pizzahut.in', 'Pizza', '11:30 AM - 11:30 PM', 4.2, 5);

-- Menu Items for Anand Bhavan
INSERT INTO MenuItems (restaurant_id, name, description, price, category, is_vegetarian, preparation_time) VALUES
(1, 'Masala Dosa', 'Crispy rice crepe with potato filling and sambar', 89.00, 'Main Course', TRUE, 15),
(1, 'Idli Sambar', 'Steamed rice cakes with lentil soup', 69.00, 'Breakfast', TRUE, 10),
(1, 'Vada Sambar', 'Fried lentil donuts with sambar', 79.00, 'Breakfast', TRUE, 12),
(1, 'Plain Uttapam', 'Thick rice pancake with toppings', 99.00, 'Main Course', TRUE, 15),
(1, 'Filter Coffee', 'Traditional South Indian coffee', 39.00, 'Beverage', TRUE, 5),
(1, 'Medu Vada', 'Crispy savory donut', 59.00, 'Breakfast', TRUE, 10);

-- Menu Items for KFC
INSERT INTO MenuItems (restaurant_id, name, description, price, category, is_vegetarian, preparation_time) VALUES
(2, 'Original Recipe Chicken', 'Famous fried chicken with 11 herbs and spices', 249.00, 'Chicken', FALSE, 15),
(2, 'Chicken Bucket', '8 pieces of crispy fried chicken', 599.00, 'Meal', FALSE, 18),
(2, 'Veg Zinger Burger', 'Crispy vegetarian burger', 189.00, 'Burger', TRUE, 12),
(2, 'French Fries', 'Crispy golden potato fries', 99.00, 'Side', TRUE, 8),
(2, 'Hot Wings', '6 spicy chicken wings', 179.00, 'Chicken', FALSE, 15),
(2, 'Veg Strips', 'Crispy vegetarian strips', 149.00, 'Snack', TRUE, 10);

-- Menu Items for Domino's Pizza
INSERT INTO MenuItems (restaurant_id, name, description, price, category, is_vegetarian, preparation_time) VALUES
(3, 'Margherita Pizza', 'Classic pizza with tomato sauce and mozzarella', 299.00, 'Pizza', TRUE, 20),
(3, 'Pepperoni Pizza', 'Pizza topped with pepperoni and cheese', 349.00, 'Pizza', FALSE, 20),
(3, 'Veg Extravaganza', 'Loaded with capsicum, mushroom, onion and tomato', 399.00, 'Pizza', TRUE, 22),
(3, 'Garlic Breadsticks', 'Baked breadsticks with garlic seasoning', 129.00, 'Starter', TRUE, 10),
(3, 'Choco Lava Cake', 'Chocolate cake with molten center', 149.00, 'Dessert', TRUE, 5),
(3, 'Taco Paneer Pizza', 'Indo-Mexican fusion with paneer', 429.00, 'Pizza', TRUE, 25);

-- Menu Items for Pizza Hut
INSERT INTO MenuItems (restaurant_id, name, description, price, category, is_vegetarian, preparation_time) VALUES
(4, 'Pan Pizza', 'Classic pan pizza with thick crust', 329.00, 'Pizza', TRUE, 18),
(4, 'Stuffed Crust Pizza', 'Pizza with cheese-filled crust', 389.00, 'Pizza', TRUE, 22),
(4, 'Veggie Lover''s Pizza', 'Loaded with fresh vegetables', 359.00, 'Pizza', TRUE, 20),
(4, 'Garlic Bread', 'Toasted bread with garlic butter', 109.00, 'Starter', TRUE, 8),
(4, 'Chocolate Mousse', 'Rich chocolate dessert', 169.00, 'Dessert', TRUE, 5),
(4, 'Chicken Wings', 'Spicy chicken wings', 219.00, 'Chicken', FALSE, 15);

-- Delivery Partners Details
INSERT INTO DeliveryPartners (user_id, vehicle_type, vehicle_number, license_number, is_online, rating, total_deliveries) VALUES
(6, 'bike', 'KA-01-AB-1234', 'DL123456789', TRUE, 4.6, 156),
(7, 'bike', 'KA-02-CD-5678', 'DL987654321', TRUE, 4.4, 89),
(8, 'bicycle', 'KA-03-EF-9012', 'DL456789123', FALSE, 4.8, 234);

-- Sample Orders
INSERT INTO Orders (customer_id, restaurant_id, delivery_address, total_amount, status, payment_status, payment_method, delivery_partner_id) VALUES
(9, 1, '123 Customer Lane, Bangalore', 178.00, 'delivered', 'paid', 'Credit Card', 6),
(10, 2, '456 User Avenue, Bangalore', 748.00, 'picked_up', 'paid', 'UPI', 7),
(11, 3, '789 Patron Road, Bangalore', 828.00, 'preparing', 'pending', 'Cash', NULL),
(9, 4, '123 Customer Lane, Bangalore', 797.00, 'confirmed', 'paid', 'Net Banking', NULL);

-- Order Items
INSERT INTO OrderItems (order_id, menu_item_id, quantity, price_per_item, subtotal) VALUES
(1, 1, 2, 89.00, 178.00),
(2, 8, 1, 599.00, 599.00),
(2, 10, 1, 149.00, 149.00),
(3, 13, 1, 399.00, 399.00),
(3, 15, 1, 429.00, 429.00),
(4, 19, 1, 359.00, 359.00),
(4, 20, 1, 109.00, 109.00),
(4, 22, 1, 329.00, 329.00);

-- Sample Ratings
INSERT INTO RestaurantRatings (restaurant_id, customer_id, rating, review) VALUES
(1, 9, 5, 'Amazing South Indian food! Authentic dosas and filter coffee.'),
(2, 10, 4, 'Great KFC experience, chicken was fresh and crispy.'),
(3, 11, 5, 'Best pizza in Bangalore! Quick delivery too.');

INSERT INTO ItemRatings (menu_item_id, customer_id, rating, review) VALUES
(1, 9, 5, 'Best masala dosa in Bangalore! Perfectly crispy.'),
(8, 10, 4, 'Fresh chicken bucket, good value for money.'),
(13, 11, 5, 'Veg extravaganza pizza was loaded with toppings!');

-- Sample Cart Data (for active customer sessions)
INSERT INTO Cart (customer_id, menu_item_id, quantity) VALUES
(12, 3, 1),
(12, 4, 2),
(13, 14, 1);

-- Sample Delivery Tracking
INSERT INTO DeliveryTracking (order_id, delivery_partner_id, latitude, longitude, status) VALUES
(1, 6, 12.9716, 77.5946, 'delivered'),
(2, 7, 12.9352, 77.6245, 'picked_up');
