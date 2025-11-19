-- Run these statements in your MySQL client to create the DB and user
CREATE DATABASE rental_services CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'rental_user'@'localhost' IDENTIFIED BY 'rental_pass';
GRANT ALL PRIVILEGES ON rental_services.* TO 'rental_user'@'localhost';
FLUSH PRIVILEGES;
