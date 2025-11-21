import mysql.connector
from mysql.connector import Error

SQL_SCRIPT = """
CREATE DATABASE IF NOT EXISTS rental_services
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE rental_services;

CREATE TABLE IF NOT EXISTS users (
  id int NOT NULL AUTO_INCREMENT,
  name varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  email varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  phone varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  address varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  isDeleted tinyint(1) NOT NULL DEFAULT '0',
  password varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  role varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT 'user',
  PRIMARY KEY (id),
  KEY ix_users_id (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS technicians (
  id int NOT NULL AUTO_INCREMENT,
  name varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  phone varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  email varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  specialties json DEFAULT NULL,
  PRIMARY KEY (id),
  KEY ix_technicians_id (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS services (
  id int NOT NULL AUTO_INCREMENT,
  icon varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  title varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  description text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (id),
  KEY ix_services_id (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS agendas (
  id int NOT NULL AUTO_INCREMENT,
  email varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  phone varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  address varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  date varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  observation text COLLATE utf8mb4_unicode_ci,
  technician_id int DEFAULT NULL,
  technicianObservation text COLLATE utf8mb4_unicode_ci,
  status varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  service varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  userId int DEFAULT NULL,
  userName varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (id),
  KEY technician_id (technician_id),
  KEY ix_agendas_id (id),
  KEY fk_agenda_user (userId),
  CONSTRAINT agendas_ibfk_1 FOREIGN KEY (technician_id)
    REFERENCES technicians (id),
  CONSTRAINT fk_agenda_user FOREIGN KEY (userId)
    REFERENCES users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

def run_script():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''  # si tu MySQL tiene contraseña, ponla aquí
        )

        cursor = connection.cursor()
        print("Conectado a MySQL")

        for statement in SQL_SCRIPT.split(';'):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt + ';')

        connection.commit()
        print("Base de datos y tablas creadas correctamente.")

    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión cerrada.")


if __name__ == "__main__":
    run_script()
