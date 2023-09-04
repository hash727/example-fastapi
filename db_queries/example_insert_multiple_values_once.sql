INSERT INTO products (name, price, is_sale, inventory)
VALUES ('CAR', 50000, true, 45),
	   ('AUTO' , 4000, false, 50),
	   ('LAPTOP', 500, true, 5),
	   ('Monitor', 400, false, 45)
		RETURNING *;