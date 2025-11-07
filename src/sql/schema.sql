
-- Food Delivery System Database Schema

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    role ENUM('system_admin', 'restaurant_admin', 'customer', 'delivery_partner') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role)
);

-- Restaurants table
CREATE TABLE Restaurants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    cuisine_type VARCHAR(50),
    opening_hours VARCHAR(100),
    rating DECIMAL(3,2) DEFAULT 0.00,
    is_active BOOLEAN DEFAULT TRUE,
    admin_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES Users(id) ON DELETE CASCADE,
    INDEX idx_name (name),
    INDEX idx_cuisine (cuisine_type),
    INDEX idx_admin (admin_id)
);

-- Menu items (Food) table
CREATE TABLE MenuItems (
    id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(50),
    is_vegetarian BOOLEAN DEFAULT TRUE,
    is_available BOOLEAN DEFAULT TRUE,
    preparation_time INT DEFAULT 15,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(id) ON DELETE CASCADE,
    INDEX idx_restaurant (restaurant_id),
    INDEX idx_category (category),
    INDEX idx_price (price),
    INDEX idx_available (is_available)
);

-- Orders table
CREATE TABLE Orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    delivery_address TEXT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'confirmed', 'preparing', 'ready', 'picked_up', 'delivered', 'cancelled') DEFAULT 'pending',
    payment_status ENUM('pending', 'paid', 'failed', 'refunded') DEFAULT 'pending',
    payment_method VARCHAR(50),
    delivery_partner_id INT NULL,
    estimated_delivery_time TIMESTAMP,
    actual_delivery_time TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(id) ON DELETE CASCADE,
    FOREIGN KEY (delivery_partner_id) REFERENCES Users(id) ON DELETE SET NULL,
    INDEX idx_customer (customer_id),
    INDEX idx_restaurant (restaurant_id),
    INDEX idx_status (status),
    INDEX idx_delivery_partner (delivery_partner_id),
    INDEX idx_created (created_at)
);

-- Order items table (many-to-many relationship)
CREATE TABLE OrderItems (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    price_per_item DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES MenuItems(id) ON DELETE CASCADE,
    INDEX idx_order (order_id),
    INDEX idx_menu_item (menu_item_id)
);

-- Delivery partners table (extends Users with delivery-specific info)
CREATE TABLE DeliveryPartners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    vehicle_type ENUM('bike', 'car', 'bicycle') NOT NULL,
    vehicle_number VARCHAR(20) NOT NULL,
    license_number VARCHAR(50),
    is_online BOOLEAN DEFAULT FALSE,
    current_latitude DECIMAL(10,8),
    current_longitude DECIMAL(11,8),
    rating DECIMAL(3,2) DEFAULT 0.00,
    total_deliveries INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user (user_id),
    INDEX idx_online (is_online),
    INDEX idx_rating (rating),
    INDEX idx_location (current_latitude, current_longitude)
);

-- Delivery tracking table
CREATE TABLE DeliveryTracking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    delivery_partner_id INT NOT NULL,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    status ENUM('assigned', 'picked_up', 'on_the_way', 'delivered') NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES Orders(id) ON DELETE CASCADE,
    FOREIGN KEY (delivery_partner_id) REFERENCES Users(id) ON DELETE CASCADE,
    INDEX idx_order (order_id),
    INDEX idx_partner (delivery_partner_id),
    INDEX idx_timestamp (timestamp)
);

-- Restaurant ratings table
CREATE TABLE RestaurantRatings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT NOT NULL,
    customer_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES Users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_rating (restaurant_id, customer_id),
    INDEX idx_restaurant (restaurant_id),
    INDEX idx_rating (rating)
);

-- Food item ratings table
CREATE TABLE ItemRatings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    menu_item_id INT NOT NULL,
    customer_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (menu_item_id) REFERENCES MenuItems(id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES Users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_item_rating (menu_item_id, customer_id),
    INDEX idx_menu_item (menu_item_id),
    INDEX idx_rating (rating)
);

-- Cart table for active customer sessions
CREATE TABLE Cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES MenuItems(id) ON DELETE CASCADE,
    UNIQUE KEY unique_cart_item (customer_id, menu_item_id),
    INDEX idx_customer (customer_id)
);

-- Triggers for automatic rating updates
DELIMITER //
CREATE TRIGGER update_restaurant_rating 
AFTER INSERT ON RestaurantRatings
FOR EACH ROW
BEGIN
    UPDATE Restaurants 
    SET rating = (
        SELECT COALESCE(AVG(rating), 0) 
        FROM RestaurantRatings 
        WHERE restaurant_id = NEW.restaurant_id
    )
    WHERE id = NEW.restaurant_id;
END//
DELIMITER ;
