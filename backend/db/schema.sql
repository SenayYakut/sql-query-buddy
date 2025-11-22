-- Customers Table
CREATE TABLE customers (
 customer_id INTEGER PRIMARY KEY,
 name TEXT NOT NULL,
 email TEXT UNIQUE,
 region TEXT,
 signup_date DATE
);

-- Products Table
CREATE TABLE products (
 product_id INTEGER PRIMARY KEY,
 name TEXT NOT NULL,
 category TEXT,
 price DECIMAL(10,2)
);

-- Orders Table
CREATE TABLE orders (
 order_id INTEGER PRIMARY KEY,
 customer_id INTEGER,
 order_date DATE,
 total_amount DECIMAL(10,2),
 FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Order Items Table
CREATE TABLE order_items (
 item_id INTEGER PRIMARY KEY,
 order_id INTEGER,
 product_id INTEGER,
 quantity INTEGER,
 subtotal DECIMAL(10,2),
 FOREIGN KEY (order_id) REFERENCES orders(order_id),
 FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Sample Customers
INSERT INTO customers (customer_id, name, email, region, signup_date) VALUES
(1, 'Alice Chen', 'alice.chen@example.com', 'California', '2023-02-01'),
(2, 'John Patel', 'john.patel@example.com', 'New York', '2023-05-15'),
(3, 'Maria Lopez', 'maria.lopez@example.com', 'Texas', '2022-11-30'),
(4, 'David Johnson', 'david.johnson@example.com', 'Florida', '2023-07-22'),
(5, 'Sofia Khan', 'sofia.khan@example.com', 'Illinois', '2023-04-10');

-- Sample Products
INSERT INTO products (product_id, name, category, price) VALUES
(1, 'Laptop Pro 15', 'Electronics', 1200.00),
(2, 'Wireless Mouse', 'Accessories', 40.00),
(3, 'Standing Desk', 'Furniture', 300.00),
(4, 'Noise Cancelling Headphones', 'Electronics', 150.00),
(5, 'Office Chair Deluxe', 'Furniture', 180.00);

-- Sample Orders
INSERT INTO orders (order_id, customer_id, order_date, total_amount) VALUES
(101, 1, '2024-01-12', 1240.00),
(102, 2, '2024-03-05', 340.00),
(103, 3, '2024-02-20', 1600.00),
(104, 1, '2024-04-02', 330.00),
(105, 4, '2024-05-15', 480.00),
(106, 5, '2024-06-10', 180.00);

-- Sample Order Items
INSERT INTO order_items (item_id, order_id, product_id, quantity, subtotal) VALUES
(1, 101, 1, 1, 1200.00),
(2, 101, 2, 1, 40.00),
(3, 102, 2, 2, 80.00),
(4, 102, 4, 1, 150.00),
(5, 103, 3, 5, 1500.00),
(6, 103, 2, 2, 80.00),
(7, 104, 5, 1, 180.00),
(8, 104, 2, 3, 120.00),
(9, 105, 4, 3, 450.00),
(10, 106, 5, 1, 180.00);
