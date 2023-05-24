-- SQL-команды для создания таблиц
CREATE TABLE employees
(
	employee_id serial PRIMARY KEY,
	first_name varchar(100) UNIQUE,
	last_name varchar(100) UNIQUE,
	title varchar(100),
	birth_date date,
	notes text
);

CREATE TABLE customers
(
	customer_id char(5) PRIMARY KEY,
	company_name varchar(100),
	contact_name varchar(100)
);

CREATE TABLE orders
(
	order_id int PRIMARY KEY,
	customer_id char(5) REFERENCES customers(customer_id),
	employee_id serial REFERENCES employees(employee_id),
	order_date date,
	ship_city varchar(100)
);