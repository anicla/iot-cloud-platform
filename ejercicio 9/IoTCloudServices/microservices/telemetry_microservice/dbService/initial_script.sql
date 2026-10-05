CREATE DATABASE IF NOT EXISTS fic_data;
USE fic_data;

CREATE TABLE IF NOT EXISTS telemetry (
  id MEDIUMINT NOT NULL AUTO_INCREMENT,
  container_id VARCHAR(50) NOT NULL,
  latitude FLOAT NOT NULL,
  longitude FLOAT NOT NULL,
  temperature FLOAT NOT NULL,
  humidity FLOAT NOT NULL,
  door_open TINYINT,
  current_driver_id VARCHAR(50) NOT NULL,
  refrigerator_fan FLOAT NOT NULL,
  time_stamp VARCHAR(50) NOT NULL,
  PRIMARY KEY (id)
);
