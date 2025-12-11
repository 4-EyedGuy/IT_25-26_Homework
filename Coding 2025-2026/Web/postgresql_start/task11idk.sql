-- Схема

DROP TABLE IF EXISTS views;
CREATE TABLE views (
  view_id        SERIAL PRIMARY KEY,
  view_date      DATE        NOT NULL,
  region         TEXT        NOT NULL CHECK (region IN ('Nordics', 'DACH', 'CEE', 'UK')),
  device         TEXT        NOT NULL CHECK (device IN ('mobile', 'desktop', 'tv')),
  membership     TEXT        NOT NULL CHECK (membership IN ('free', 'standard', 'premium')),
  content_type   TEXT        NOT NULL CHECK (content_type IN ('movie', 'series', 'live')),
  status         TEXT        NOT NULL CHECK (status IN ('started', 'completed', 'abandoned', 'refunded')),
  minutes        INT         NOT NULL CHECK (minutes > 0),
  base_price     NUMERIC(6,2) NOT NULL CHECK (base_price >= 0),
  ad_revenue     NUMERIC(6,2) NOT NULL CHECK (ad_revenue >= 0),
  discount       NUMERIC(6,2) NOT NULL CHECK (discount >= 0)
);

-- Наполнение (26 строк)

INSERT INTO views (view_date,region,device,membership,content_type,status,minutes,base_price,ad_revenue,discount) VALUES
('2025-01-03','Nordics','tv','premium','movie','completed',     118,  0,   0,   0),
('2025-01-04','Nordics','mobile','free','series','completed',    52,  0,  1.8,  0),
('2025-01-05','Nordics','desktop','standard','movie','abandoned',34,  0,  0.6,  0),
('2025-01-07','Nordics','mobile','free','live','completed',      45,  0,  2.2,  0),
('2025-01-10','Nordics','tv','standard','movie','refunded',      95,  6.99,0.0, 1.00),

('2025-02-01','DACH','tv','premium','movie','completed',        131,  0,   0,   0),
('2025-02-02','DACH','desktop','free','series','abandoned',      22,  0,  0.9,  0),
('2025-02-03','DACH','mobile','standard','live','completed',     60,  0,  0.5,  0),
('2025-02-05','DACH','tv','standard','movie','completed',       102,  4.99,0.0, 1.00),
('2025-02-08','DACH','mobile','free','movie','completed',        70,  0,  2.5,  0),
('2025-02-09','DACH','desktop','premium','series','completed',   47,  0,   0,   0),

('2025-03-02','CEE','mobile','free','series','completed',        51,  0,  1.6,  0),
('2025-03-03','CEE','desktop','standard','movie','completed',    94,  3.99,0.0, 0.50),
('2025-03-04','CEE','tv','premium','movie','completed',         123,  0,   0,   0),
('2025-03-06','CEE','mobile','free','live','abandoned',          18,  0,  0.7,  0),
('2025-03-09','CEE','desktop','standard','series','refunded',    40,  0,  0.0,  0),

('2025-04-01','UK','tv','premium','movie','completed',          142,  0,   0,   0),
('2025-04-02','UK','desktop','free','series','completed',        58,  0,  1.9,  0),
('2025-04-03','UK','mobile','standard','movie','completed',      88,  5.99,0.0, 1.00),
('2025-04-04','UK','tv','standard','live','completed',           72,  0,  0.4,  0),
('2025-04-06','UK','mobile','free','movie','started',            12,  0,  0.5,  0),
('2025-04-07','UK','desktop','premium','series','completed',     49,  0,   0,   0),

('2025-04-10','Nordics','tv','standard','movie','completed',    100,  4.99,0.0, 0.50),
('2025-04-12','DACH','mobile','free','live','completed',         38,  0,  1.1,  0),
('2025-04-14','CEE','desktop','standard','movie','abandoned',    41,  2.99,0.0, 0.00),
('2025-04-15','UK','mobile','free','series','completed',         55,  0,  1.5,  0);

SELECT 
    view_id,
    region,
    status,
    CASE 
        WHEN status = 'completed' THEN base_price - discount + ad_revenue
        WHEN status = 'refunded'   THEN 0
        ELSE ad_revenue
    END AS net_revenue,
    CASE 
        WHEN minutes <= 30 THEN 'short'
        WHEN minutes <= 60 THEN 'mid'
        ELSE 'long'
    END AS length_band
FROM views
ORDER BY view_date, view_id;


SELECT 
    view_id,
    content_type,
    minutes
FROM views
WHERE minutes > CASE 
    WHEN content_type = 'movie'  THEN 60
    WHEN content_type = 'series' THEN 45
    ELSE 30
END
ORDER BY minutes DESC;


SELECT 
    region,
    COUNT(*)                  AS sessions,
    SUM(minutes)              AS sum_minutes,
    ROUND(AVG(ad_revenue), 4) AS avg_ads,
    MAX(base_price)           AS max_price
FROM views
GROUP BY region
ORDER BY sum_minutes DESC;


SELECT 
    region,
    SUM(base_price - discount + ad_revenue) FILTER (WHERE status = 'completed') AS delivered_revenue,
    COUNT(*) FILTER (WHERE status = 'refunded')                                AS refund_cnt,
    ROUND(
        COUNT(*) FILTER (WHERE status = 'refunded')::NUMERIC / COUNT(*), 4
    )                                                                          AS refund_rate
FROM views
GROUP BY region
ORDER BY refund_rate DESC NULLS LAST;


SELECT 
    membership,
    COUNT(*)                                                               AS total_sessions,
    COUNT(*) FILTER (WHERE status = 'refunded')                            AS refund_cnt,
    SUM(base_price - discount + ad_revenue) FILTER (WHERE status = 'completed') AS delivered_revenue
FROM views
GROUP BY membership
HAVING 
    COUNT(*) FILTER (WHERE status = 'refunded')::NUMERIC / COUNT(*) > 0.08
    OR 
    SUM(base_price - discount + ad_revenue) FILTER (WHERE status = 'completed') > 12
ORDER BY delivered_revenue DESC;