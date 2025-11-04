DROP DATABASE IF EXISTS restaurant_db;
CREATE DATABASE restaurant_db;
USE restaurant_db;

CREATE TABLE Admin (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    email VARCHAR(100) UNIQUE NOT NULL,
    phoneno VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Restaurant (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    address VARCHAR(255),
    openingHours VARCHAR(100),
    admin_id INT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES Admin(id) ON DELETE SET NULL
);

CREATE TABLE Food (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    ingredients TEXT,
    category VARCHAR(50),
    isNonVeg BOOLEAN DEFAULT FALSE,
    admin_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES Admin(id) ON DELETE SET NULL
);

CREATE TABLE Customer (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    email VARCHAR(100) UNIQUE NOT NULL,
    phoneno VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Payment (
    id INT PRIMARY KEY AUTO_INCREMENT,
    type VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    customer_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Customer(id) ON DELETE CASCADE
);

CREATE TABLE `Order` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    price DECIMAL(10, 2) NOT NULL,
    address VARCHAR(255),
    customer_id INT,
    restaurant_id INT,
    payment_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Customer(id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(id) ON DELETE SET NULL,
    FOREIGN KEY (payment_id) REFERENCES Payment(id) ON DELETE SET NULL
);

CREATE TABLE OrderFood (
    order_id INT,
    food_id INT,
    quantity INT DEFAULT 1,
    PRIMARY KEY (order_id, food_id),
    FOREIGN KEY (order_id) REFERENCES `Order`(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES Food(id) ON DELETE CASCADE
);

CREATE INDEX idx_admin_username ON Admin(username);
CREATE INDEX idx_customer_username ON Customer(username);
CREATE INDEX idx_food_category ON Food(category);
CREATE INDEX idx_order_customer ON `Order`(customer_id);
CREATE INDEX idx_order_restaurant ON `Order`(restaurant_id);
CREATE INDEX idx_payment_customer ON Payment(customer_id);
