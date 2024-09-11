DROP TABLE IF EXISTS seller;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS sale;
DROP TABLE IF EXISTS sale_item;
DROP TABLE IF EXISTS costumer;
DROP TABLE IF EXISTS cash_register;

CREATE TABLE seller (
    id VARCHAR PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    birthday DATE NOT NULL,
    phone_number INTEGER NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE product (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    publisher TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT NOT NULL,
    quantity INTEGER NOT NULL
);

CREATE TABLE sale (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    seller_id VARCHAR NOT NULL,
    cash_register_id INTEGER NOT NULL,
    costumer_id VARCHAR DEFAULT 'Sem cliente cadastrado',
    sale_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sale_total_price DECIMAL(10,2) NOT NULL DEFAULT 0,
    itens_quantity INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'Não concluída',
    payment_method VARCHAR(50) NOT NULL DEFAULT 'Nenhum',
    change DECIMAL(10,2) DEFAULT 0,
    FOREIGN KEY (seller_id) REFERENCES seller (id),
    FOREIGN KEY (costumer_id) REFERENCES costumer (id)
);

CREATE TABLE sale_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    product_id INTEGER NOT NULL,
    product_price DECIMAL(10,2) NOT NULL,
    quantity INTEGER NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    sale_id INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product (id),
    FOREIGN KEY (product_price) REFERENCES product (price),
    FOREIGN KEY (sale_id) REFERENCES sale (id)
);

CREATE TABLE costumer (
    id VARCHAR PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    birthday DATE,
    phone_number INTEGER,
    email TEXT
);

CREATE TABLE cash_register (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    seller_id VARCHAR NOT NULL,
    cash_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'Fechado',
    cash_fund DECIMAL(10,2) NOT NULL DEFAULT 0,
    revenue DECIMAL(10,2) NOT NULL DEFAULT 0,
    revenue_declared DECIMAL(10,2) NOT NULL DEFAULT 0,
    expenses DECIMAL(10,2) NOT NULL DEFAULT 0,
    expenses_declared DECIMAL(10,2) NOT NULL DEFAULT 0,
    sales_number INTEGER NOT NULL DEFAULT 0,
    products_sold INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (seller_id) REFERENCES seller (id)
)