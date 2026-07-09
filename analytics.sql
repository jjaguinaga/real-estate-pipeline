CREATE VIEW count_by_type AS 
SELECT listing_type, COUNT(listing_type) AS total_count
FROM properties
GROUP BY 1;

CREATE VIEW total_commission AS
SELECT status, SUM(commission_earned) AS total_earned
FROM transactions
WHERE status = 'closed'
GROUP BY 1;

CREATE VIEW city_listing_rank AS
SELECT city, COUNT(city) AS total_listings
FROM properties
WHERE is_available = TRUE
GROUP BY 1
ORDER BY 2 DESC;

CREATE VIEW top_closing_agents AS 
SELECT a.first_name, a.last_name, COUNT(t.status) AS total_closed
FROM agents AS a
JOIN transactions AS t
	ON a.agent_id = t.agent_id
WHERE t.status = 'closed'
GROUP BY 1, 2
ORDER BY 3 DESC
LIMIT 5;

CREATE VIEW average_sale_price AS
SELECT p.property_type, ROUND(AVG(t.sale_price)::numeric, 2) AS avg_sale_price
FROM properties AS p
JOIN transactions AS t
	ON p.property_id = t.property_id
WHERE t.status = 'closed'
GROUP BY 1;

CREATE VIEW status_percents AS
SELECT status, ROUND(COUNT(status) * 100.0 / SUM(COUNT(status)) OVER (), 2) AS percent
FROM transactions
GROUP BY 1;

CREATE VIEW top_agents AS
SELECT a.first_name, a.last_name, a.specialization, ROUND(SUM(t.commission_earned)::numeric, 2) AS total_commission
FROM agents AS a
JOIN transactions AS t
	ON a.agent_id = t.agent_id
WHERE t.status = 'closed'
GROUP BY 1, 2, 3
ORDER BY 4 DESC;

CREATE VIEW days_on_market AS 
SELECT p.city, AVG(t.close_date - p.listed_date) AS days
FROM properties AS p
JOIN transactions AS t
	ON p.property_id = t.property_id
WHERE t.status = 'closed'
GROUP BY 1;

CREATE VIEW returning_clients AS
SELECT c.first_name, c.last_name, c.client_type, COUNT(t.status) AS total
FROM clients AS c
JOIN transactions AS t
	ON c.client_id = t.client_id
WHERE t.status = 'closed'
GROUP BY 1, 2, 3
HAVING COUNT(t.status) > 1
ORDER BY 4 DESC;