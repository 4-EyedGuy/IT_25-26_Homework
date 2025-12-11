DROP TABLE IF EXISTS iot_ingest_lines;
CREATE TABLE iot_ingest_lines (
  id SERIAL PRIMARY KEY,
  source_file TEXT NOT NULL,
  line_no INT NOT NULL,
  raw_line TEXT NOT NULL,
  received_at TIMESTAMPTZ DEFAULT NOW(),
  note TEXT
);

INSERT INTO iot_ingest_lines (source_file, line_no, raw_line, note) VALUES
('gateway_A_2025_11.log', 1, 'DEV_ID: DEV-AB12-3456; fw: v1.2.3; temp: 23.5C; support: ops@example.com', 'telemetry row'),
('gateway_A_2025_11.log', 2, 'device: abcd1234; fw: 1.02; humidity: "45,2"% ; support: help@iot-co.co', 'telemetry row'),
('gateway_B_2025_11.log', 3, 'ID: dev:XY_99-0001; fw: v01.2; size: "1,200" bytes; note: owner@example..com', 'telemetry with bad email'),

('factory_feed.csv', 10, 'serial: SN-0001; version: 2.0.1; storage: "1 024"', 'factory row'),
('factory_feed.csv', 11, 'serial: SN0002; version: v2.0; storage: "512"', 'factory row'),

('device_tags.csv', 1, 'tags: edge, sensor, temperature', 'tags row'),
('device_tags.csv', 2, 'tags: gateway, , backbone', 'tags with empty'),

('installations_dirty.csv', 5, '"Site, North","Rack 12, Unit 4","x:100,y:200"', 'dirty csv'),
('installations_dirty.csv', 6, '"O''Hara, Plant","Area A, Sector 7","notes: needs inspection"', 'dirty csv with apostrophe'),

('ingest_log.txt', 200, 'INFO: ingest started for gateway_A_2025_11.log', 'log'),
('ingest_log.txt', 201, 'Warning: missing fw version for SN0002', 'log'),
('ingest_log.txt', 202, 'error: failed to parse telemetry line 3', 'log'),
('ingest_log.txt', 203, 'Error: device id malformed', 'log'),

('gateway_A_2025_11.log', 20, 'DEV_ID: bad@-id; support: ops@@example.com; fw: v1..2', 'trap-bad-id-email-fw'),
('device_tags.csv', 3, 'tags: sensor,, ,temperature', 'trap-empty-tags');

SELECT id, source_file, line_no, raw_line
FROM iot_ingest_lines
WHERE raw_line ~ '([A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)';

SELECT id, source_file, line_no, raw_line
FROM iot_ingest_lines
WHERE raw_line !~ '([A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)';

SELECT
  id,
  source_file,
  line_no,
  (regexp_match(raw_line, '([A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)'))[1] AS email
FROM iot_ingest_lines
WHERE raw_line ~ '([A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)';

SELECT
  id,
  source_file,
  line_no,
  (regexp_match(raw_line,
    '((?:DEV-[A-Z0-9]{2,}-\d{3,6})|(?:SN-?\d{3,6})|(?:dev:[A-Za-z0-9_/-]+)|(?:\b[a-z0-9]{6,12}\b))',
    'i'))[1] AS device_id
FROM iot_ingest_lines
WHERE raw_line ~* 'DEV-[A-Z0-9]{2,}-\d{3,6}|SN-?\d{3,6}|dev:|[a-z0-9]{6,12}';

SELECT
  t.id,
  t.source_file,
  t.line_no,
  m.version
FROM iot_ingest_lines t
CROSS JOIN LATERAL regexp_matches(t.raw_line, '(v?\d+(?:\.\d+){1,2})', 'g') AS m(version)
ORDER BY t.id;

SELECT
  id,
  source_file,
  line_no,
  raw_line,
  (regexp_match(raw_line, '(?:storage|size):\s*"?([0-9][0-9,\s]*)"?'))[1] AS raw_number,
  CASE
    WHEN raw_line ~* '(?:storage|size):' THEN
      (regexp_replace(
         (regexp_match(raw_line, '(?:storage|size):\s*"?([0-9][0-9,\s]*)"?'))[1],
         '[^\d]', '', 'g'
       ))::bigint
    ELSE NULL
  END AS normalized_number
FROM iot_ingest_lines
WHERE raw_line ~* '(?:storage|size):';

SELECT
  id,
  source_file,
  line_no,
  raw_line,
  (regexp_match(raw_line, 'tags:\s*(.*)'))[1] AS tags_raw,
  (
    SELECT array_agg(trim(both ' ' FROM t))
    FROM unnest(regexp_split_to_array((regexp_match(raw_line, 'tags:\s*(.*)'))[1], '\s*,\s*')) AS t
    WHERE trim(both ' ' FROM t) <> ''
  ) AS tags_array
FROM iot_ingest_lines
WHERE source_file = 'device_tags.csv' OR raw_line ~* 'tags:';

SELECT
  id,
  source_file,
  line_no,
  trim(both '"' FROM trim(both ' ' FROM field)) AS field_value
FROM iot_ingest_lines,
     regexp_split_to_table(raw_line, ',(?=(?:[^"]*"[^"]*")*[^"]*$)') AS field
WHERE source_file = 'installations_dirty.csv';

SELECT id, source_file, line_no, raw_line
FROM iot_ingest_lines
WHERE source_file = 'ingest_log.txt'
  AND raw_line ~* '\berror\b';

SELECT
  id,
  source_file,
  line_no,
  raw_line,
  regexp_replace(raw_line, 'error', 'ERROR', 'gi') AS raw_line_errors_normalized
FROM iot_ingest_lines
WHERE source_file = 'ingest_log.txt';