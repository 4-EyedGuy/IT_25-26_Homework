ALTER TABLE order_raw RENAME TO orders;

ALTER TABLE orders
    ALTER COLUMN amount_cents TYPE numeric(12,2) USING amount_cents / 100.0;

ALTER TABLE orders
    RENAME COLUMN amount_cents TO amount;

ALTER TABLE orders
    ADD COLUMN order_code text;

UPDATE orders
SET order_code = 'ORD-' || to_char(placed_at, 'YYYYMM') || '-' || lpad(id::text, 5, '0');

ALTER TABLE orders
    DROP COLUMN deprecated;
