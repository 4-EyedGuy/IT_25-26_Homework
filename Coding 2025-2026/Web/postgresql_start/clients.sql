CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL CHECK (POSITION('@' IN email) > 0),
    discount_percent NUMERIC(5,2) CHECK (discount_percent >= 0 AND discount_percent <= 50)
);

INSERT INTO clients (full_name, email, discount_percent) VALUES
('Иван Петров', 'ivan.petrov@gmail.com', 10),
('Мария Сидорова', 'maria.sidorova@mail.ru', 25),
('Антон Кузнецов', 'anton.kuznetsov@gmail.com', 0),
('Екатерина Орлова', 'ekaterina.orlova@yandex.ru', 50);