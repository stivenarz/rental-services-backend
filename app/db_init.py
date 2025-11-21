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

def init_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = conn.cursor()

        print("🔵 Ejecutando inicialización de la base de datos...")

        # Ejecutar creación de DB y tablas
        for stmt in SQL_SCRIPT.split(";"):
            s = stmt.strip()
            if s:
                cursor.execute(s + ";")

        conn.commit()
        print("🟢 Base de datos y tablas listas.")

        # ---------------------------------
        # 1. Verificar si el usuario existe
        # ---------------------------------
        check_query = """
            SELECT id FROM rental_services.users
            WHERE email = %s LIMIT 1;
        """
        email = "kgcarrillo10@gmail.com"
        cursor.execute(check_query, (email,))
        result = cursor.fetchone()

        # ---------------------------------
        # 2. Insertar usuario si no existe
        # ---------------------------------
        if not result:
            insert_query = """
                INSERT INTO rental_services.users
                (name, email, password, isDeleted, phone, address, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (
                "Karol Carrillo",
                "kgcarrillo10@gmail.com",
                "totumito",
                0,  # isDeleted
                "3006586484",
                "Cra 42 39C 23",
                "admin"
            ))
            conn.commit()
            print("🟢 Usuario 'Karol Carrillo' agregado correctamente.")
        else:
            print("ℹ️ El usuario ya existe, no se insertó nuevamente.")

    except Error as e:
        print("🔴 ERROR inicializando DB:", e)

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass
