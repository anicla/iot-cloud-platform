CREATE DATABASE IF NOT EXISTS fic_data;
USE fic_data;

CREATE TABLE IF NOT EXISTS containers (
  id MEDIUMINT NOT NULL AUTO_INCREMENT,
  container_id VARCHAR(50) NOT NULL UNIQUE,
  container_hostname VARCHAR(80) DEFAULT '',
  active TINYINT DEFAULT 0,
  telemetry_rate FLOAT DEFAULT 10,
  sensors_rate FLOAT DEFAULT 10,
  PRIMARY KEY (id)
);

INSERT IGNORE INTO containers (container_id, active, telemetry_rate, sensors_rate)
VALUES
('UC3M-Container-1', 0, 10, 10),
('UC3M-Container-2', 0, 10, 10),
('UC3M-Container-3', 0, 10, 10),
('UC3M-Container-4', 0, 10, 10),
('UC3M-Container-5', 0, 10, 10);
