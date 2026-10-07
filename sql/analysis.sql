SELECT
    o.order_id,
    c.customer_name,
    p.product_name,
    o.quantity,
    p.inventory_qty,
    o.quantity - p.inventory_qty AS shortage
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN products p
    ON o.product_id = p.product_id
WHERE o.quantity > p.inventory_qty;


SELECT
    c.customer_name,
    SUM(o.quantity * p.unit_price) AS order_value
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN products p
    ON o.product_id = p.product_id
GROUP BY c.customer_name
ORDER BY order_value DESC;