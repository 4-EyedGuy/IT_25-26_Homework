DROP TABLE IF EXISTS order_raw CASCADE;

CREATE TABLE order_raw (
    id             serial PRIMARY KEY,
    customer_name  text,
    amount_cents   integer,
    placed_at      timestamp DEFAULT now(),
    status         text DEFAULT 'new',
    deprecated     boolean DEFAULT false
);

INSERT INTO order_raw (customer_name, amount_cents, status, placed_at, deprecated) VALUES
('Alice Johnson',     1299,    'new',      now() - interval '30 days',  false),
('Bob Smith',         25999,   'paid',     now() - interval '28 days',  false),
('Charlie Brown',     4599,    'shipped',  now() - interval '25 days',  false),
('Diana Prince',      9999,    'new',      now() - interval '24 days',  false),
('Evan Lee',          209900,  'paid',     now() - interval '22 days',  false),
('Fiona Adams',       4999,    'canceled', now() - interval '20 days',  false),
('George Miller',     129900,  'paid',     now() - interval '18 days',  false),
('Hannah Davis',      3499,    'new',      now() - interval '17 days',  false),
('Ian Wright',        224999,  'shipped',  now() - interval '16 days',  false),
('Julia Stone',       8999,    'new',      now() - interval '15 days',  false),
('Kevin Park',        145999,  'paid',     now() - interval '14 days',  false),
('Laura Chen',        5599,    'new',      now() - interval '13 days',  false),
('Mark Green',        7999,    'paid',     now() - interval '12 days',  false),
('Nina Patel',        3799,    'canceled', now() - interval '11 days',  false),
('Oscar Diaz',        319900,  'paid',     now() - interval '10 days',  false),
('Paula Gomez',       2499,    'new',      now() - interval '9 days',   false),
('Quinn Baker',       10999,   'shipped',  now() - interval '8 days',   false),
('Rita Ora',          2899,    'new',      now() - interval '7 days',   false),
('Sam Young',         18999,   'paid',     now() - interval '6 days',   false),
('Tina King',         45999,   'paid',     now() - interval '5 days',   false),
('Uma Reed',          12999,   'new',      now() - interval '4 days',   false),
('Victor Hugo',       2399,    'canceled', now() - interval '3 days',   false),
('Wendy Frost',       6699,    'new',      now() - interval '2 days',   false),
('Yara Novak',        9999,    'paid',     now() - interval '1 days',   false),
('Zack Cole',         154999,  'shipped',  now() - interval '12 hours', false);