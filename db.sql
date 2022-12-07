-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION pg_database_owner;

-- DROP SEQUENCE public.cart_item_id_seq;

CREATE SEQUENCE public.cart_item_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.cart_item_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE public.cart_item_id_seq TO postgres;

-- DROP SEQUENCE public.cart_user_id_seq;

CREATE SEQUENCE public.cart_user_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.cart_user_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE public.cart_user_id_seq TO postgres;

-- DROP SEQUENCE public.order_details_item_id_seq;

CREATE SEQUENCE public.order_details_item_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.order_details_item_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE public.order_details_item_id_seq TO postgres;

-- DROP SEQUENCE public.order_details_order_id_seq;

CREATE SEQUENCE public.order_details_order_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.order_details_order_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE public.order_details_order_id_seq TO postgres;

-- DROP SEQUENCE public.orders_order_id_seq;

CREATE SEQUENCE public.orders_order_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.orders_order_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE public.orders_order_id_seq TO postgres;

-- DROP SEQUENCE public.orders_user_id_seq;

CREATE SEQUENCE public.orders_user_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.orders_user_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE public.orders_user_id_seq TO postgres;

-- DROP SEQUENCE public.product_details_product_id_seq;

CREATE SEQUENCE public.product_details_product_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.product_details_product_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE public.product_details_product_id_seq TO postgres;

-- DROP SEQUENCE public.product_info_item_id_seq;

CREATE SEQUENCE public.product_info_item_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.product_info_item_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE public.product_info_item_id_seq TO postgres;

-- DROP SEQUENCE public.product_info_product_id_seq;

CREATE SEQUENCE public.product_info_product_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;

-- Permissions

ALTER SEQUENCE public.product_info_product_id_seq OWNER TO postgres;
GRANT ALL ON SEQUENCE public.product_info_product_id_seq TO postgres;
-- public.product_details definition

-- Drop table

-- DROP TABLE product_details;

CREATE TABLE product_details (
	product_id bigserial NOT NULL,
	product_name varchar NOT NULL,
	product_desc text NOT NULL,
	product_gender varchar NOT NULL,
	product_category varchar NOT NULL,
	CONSTRAINT product_details_pk PRIMARY KEY (product_id),
	CONSTRAINT product_name_unique_key UNIQUE (product_name)
);

-- Permissions

ALTER TABLE public.product_details OWNER TO postgres;
GRANT ALL ON TABLE public.product_details TO postgres;


-- public.status definition

-- Drop table

-- DROP TABLE status;

CREATE TABLE status (
	status_id int4 NOT NULL,
	status_name varchar NOT NULL,
	CONSTRAINT status_pk PRIMARY KEY (status_id)
);

-- Permissions

ALTER TABLE public.status OWNER TO postgres;
GRANT ALL ON TABLE public.status TO postgres;


-- public.orders definition

-- Drop table

-- DROP TABLE orders;

CREATE TABLE orders (
	order_id bigserial NOT NULL,
	user_id bigserial NOT NULL,
	total_price numeric NULL,
	date_of_purchase timestamp NOT NULL,
	status_id int4 NULL,
	CONSTRAINT orders_pk PRIMARY KEY (order_id),
	CONSTRAINT orders_un UNIQUE (user_id),
	CONSTRAINT orders_fk FOREIGN KEY (status_id) REFERENCES status(status_id) ON DELETE CASCADE
);

-- Permissions

ALTER TABLE public.orders OWNER TO postgres;
GRANT ALL ON TABLE public.orders TO postgres;


-- public.product_info definition

-- Drop table

-- DROP TABLE product_info;

CREATE TABLE product_info (
	product_id bigserial NOT NULL,
	item_size varchar NOT NULL,
	color varchar NOT NULL,
	quantity int4 NOT NULL,
	discount numeric NOT NULL,
	price numeric NOT NULL,
	item_id bigserial NOT NULL,
	rating int4 NULL DEFAULT 0,
	"primary" bool NULL DEFAULT false,
	CONSTRAINT product_info_pk PRIMARY KEY (item_id),
	CONSTRAINT product_info_fk FOREIGN KEY (product_id) REFERENCES product_details(product_id) ON DELETE CASCADE
);

-- Permissions

ALTER TABLE public.product_info OWNER TO postgres;
GRANT ALL ON TABLE public.product_info TO postgres;


-- public.cart definition

-- Drop table

-- DROP TABLE cart;

CREATE TABLE cart (
	quantity int4 NOT NULL,
	user_id bigserial NOT NULL,
	item_id bigserial NOT NULL,
	CONSTRAINT cart_fk FOREIGN KEY (item_id) REFERENCES product_info(item_id) ON DELETE CASCADE
);

-- Permissions

ALTER TABLE public.cart OWNER TO postgres;
GRANT ALL ON TABLE public.cart TO postgres;


-- public.order_details definition

-- Drop table

-- DROP TABLE order_details;

CREATE TABLE order_details (
	order_id bigserial NOT NULL,
	item_id bigserial NOT NULL,
	quantity int4 NOT NULL,
	CONSTRAINT order_details_fk FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
	CONSTRAINT order_details_fk_2 FOREIGN KEY (item_id) REFERENCES product_info(item_id)
);

-- Permissions

ALTER TABLE public.order_details OWNER TO postgres;
GRANT ALL ON TABLE public.order_details TO postgres;




-- Permissions;
