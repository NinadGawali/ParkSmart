CREATE DATABASE IF NOT EXISTS parksmart CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE parksmart;

CREATE TABLE IF NOT EXISTS users (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(150) NOT NULL UNIQUE,
  email VARCHAR(255),
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Parking spaces posted by owners
CREATE TABLE IF NOT EXISTS parking_spaces (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  owner_id BIGINT NOT NULL,
  title VARCHAR(255) NOT NULL,
  address VARCHAR(512),
  lat DOUBLE,
  lng DOUBLE,
  google_map_url VARCHAR(1024),
  price_per_hour DECIMAL(8,2) DEFAULT 0,
  is_available TINYINT(1) NOT NULL DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_parking_owner FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- Bookings: time window is optional; NULL means an indefinite exclusive lock
CREATE TABLE IF NOT EXISTS bookings (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT NOT NULL,
  parking_id BIGINT NOT NULL,
  time_start DATETIME NULL,
  time_end DATETIME NULL,
  duration_hours DECIMAL(6,2) NULL,
  total_amount DECIMAL(10,2) DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_booking_user FOREIGN KEY (user_id) REFERENCES users(id),
  CONSTRAINT fk_booking_parking FOREIGN KEY (parking_id) REFERENCES parking_spaces(id)
);

CREATE INDEX IF NOT EXISTS idx_booking_parking_time ON bookings (parking_id, time_start, time_end);
