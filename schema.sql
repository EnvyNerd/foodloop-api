CREATE DATABASE IF NOT EXISTS foodloop;
USE foodloop;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('buyer','vendor','admin') DEFAULT 'buyer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS vendors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(150) NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(150),
    hours VARCHAR(100),
    lat DECIMAL(10,7),
    lng DECIMAL(10,7),
    rating DECIMAL(3,1) DEFAULT 0,
    review_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS bags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id INT NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    contents TEXT,
    category VARCHAR(50),
    halal ENUM('halal','mixed','non-halal') DEFAULT 'halal',
    price_now DECIMAL(10,2) NOT NULL,
    price_original DECIMAL(10,2) NOT NULL,
    pickup_start VARCHAR(10),
    pickup_end VARCHAR(10),
    pickup_address TEXT,
    quantity_total INT NOT NULL,
    quantity_left INT NOT NULL,
    tags TEXT,
    image_url VARCHAR(500),
    lat DECIMAL(10,7),
    lng DECIMAL(10,7),
    active TINYINT(1) DEFAULT 1,
    views INT DEFAULT 0,
    orders_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vendor_id) REFERENCES vendors(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bag_id INT NOT NULL,
    buyer_id INT NOT NULL,
    vendor_id INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    status ENUM('paid','ready','collected','cancelled') DEFAULT 'paid',
    pickup_code VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (bag_id) REFERENCES bags(id),
    FOREIGN KEY (buyer_id) REFERENCES users(id),
    FOREIGN KEY (vendor_id) REFERENCES vendors(id)
);

CREATE TABLE IF NOT EXISTS payouts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending','completed','failed') DEFAULT 'pending',
    reference VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vendor_id) REFERENCES vendors(id)
);

CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT,
    type VARCHAR(50),
    `read` TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
