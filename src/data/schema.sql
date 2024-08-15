DROP TABLE IF EXISTS seller;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS sale;
DROP TABLE IF EXISTS order_item;
DROP TABLE IF EXISTS costumer;

CREATE TABLE seller (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    birthday DATE NOT NULL,
    phone_number INTEGER NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    price DECIMAL(10,2),
    publisher TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT NOT NULL
);

CREATE TABLE sale (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_item_id INTEGER NOT NULL,
    seller_id INTEGER NOT NULL,
    costumer_id INTEGER NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    price DECIMAL(10,2),
    FOREIGN KEY (order_item_id) REFERENCES order_item (id),
    FOREIGN KEY (seller_id) REFERENCES seller (id),
    FOREIGN KEY (costumer_id) REFERENCES costumer (id)
);

CREATE TABLE order_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product (id),
    FOREIGN KEY (order_id) REFERENCES sale (id)
);

CREATE TABLE costumer (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    birthday DATE NOT NULL,
    phone_number INTEGER NOT NULL,
    email TEXT NOT NULL
);