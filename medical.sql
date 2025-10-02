-- Medical database with cascading foreign keys
CREATE DATABASE IF NOT EXISTS medical CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE medical;

-------------------------------------------------
-- Table: addmp (Medicines Master)
-------------------------------------------------
CREATE TABLE IF NOT EXISTS addmp (
  sno INT(11) NOT NULL AUTO_INCREMENT,
  medicine VARCHAR(500) NOT NULL,
  PRIMARY KEY (sno)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO addmp (sno, medicine) VALUES
(1, 'Dolo 650'),
(2, 'Carpel 250 mg'),
(3, 'Aspirin'),
(4, 'Amoxicillin'),
(5, 'Cetirizine'),
(6, 'B-Complex'),
(7, 'Saradon'),
(8, 'Action 500');

-------------------------------------------------
-- Table: addpd (Products Master)
-------------------------------------------------
CREATE TABLE IF NOT EXISTS addpd (
  sno INT(11) NOT NULL AUTO_INCREMENT,
  product VARCHAR(200) NOT NULL,
  PRIMARY KEY (sno)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO addpd (sno, product) VALUES
(1, 'Bandages'),
(2, 'Antiseptic wipes'),
(3, 'Deodrants'),
(4, 'Talcum Powder');

-------------------------------------------------
-- Table: posts (Medical Stores)
-------------------------------------------------
CREATE TABLE IF NOT EXISTS posts (
  mid INT(11) NOT NULL AUTO_INCREMENT,
  medical_name VARCHAR(100) NOT NULL,
  owner_name VARCHAR(100) NOT NULL,
  phone_no VARCHAR(15) NOT NULL,
  address TEXT NOT NULL,
  PRIMARY KEY (mid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO posts (mid, medical_name, owner_name, phone_no, address) VALUES
(1001, 'Minerva', 'Ojas Gambheera', '7760115498', 'Chintamani');

-------------------------------------------------
-- Table: medicines (Orders)
-- Improved: Added order status and normalized references
-------------------------------------------------
CREATE TABLE IF NOT EXISTS medicines (
  id INT(11) NOT NULL AUTO_INCREMENT,
  amount INT(11) NOT NULL,
  name VARCHAR(100) NOT NULL,
  medicines VARCHAR(500) NOT NULL,
  products VARCHAR(500) NOT NULL,
  email VARCHAR(50) NOT NULL,
  mid INT(11) NOT NULL,
  status ENUM('Pending','Accepted','Cancelled') NOT NULL DEFAULT 'Pending',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  CONSTRAINT fk_medicines_posts FOREIGN KEY (mid)
    REFERENCES posts(mid)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-------------------------------------------------
-- Table: logs (Action Logs)
-- Improved: action type ENUM and proper datetime
-------------------------------------------------
CREATE TABLE IF NOT EXISTS logs (
  id INT(11) NOT NULL AUTO_INCREMENT,
  mid INT(11) NOT NULL,
  action ENUM('INSERTED','DELETED','UPDATED','ACCEPTED') NOT NULL,
  date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  CONSTRAINT fk_logs_posts FOREIGN KEY (mid)
    REFERENCES posts(mid)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO logs (id, mid, action, date) VALUES
(1, 1001, 'INSERTED', NOW()),
(2, 1001, 'DELETED', NOW());

-------------------------------------------------
-- Triggers for medicines table
-- Improved: Unique trigger names, logs ACCEPTED status
-------------------------------------------------
DELIMITER $$

CREATE TRIGGER medicines_before_delete
BEFORE DELETE ON medicines
FOR EACH ROW
BEGIN
  INSERT INTO logs(mid, action, date) VALUES (OLD.mid, 'DELETED', NOW());
END;
$$

CREATE TRIGGER medicines_after_insert
AFTER INSERT ON medicines
FOR EACH ROW
BEGIN
  INSERT INTO logs(mid, action, date) VALUES (NEW.mid, 'INSERTED', NOW());
END;
$$

CREATE TRIGGER medicines_after_update
AFTER UPDATE ON medicines
FOR EACH ROW
BEGIN
  INSERT INTO logs(mid, action, date) VALUES (NEW.mid, 'UPDATED', NOW());
END;
$$

DELIMITER ;

-------------------------------------------------
-- AUTO_INCREMENT adjustments
-------------------------------------------------
ALTER TABLE addmp AUTO_INCREMENT = 9;
ALTER TABLE addpd AUTO_INCREMENT = 5;
ALTER TABLE logs AUTO_INCREMENT = 3;
ALTER TABLE medicines AUTO_INCREMENT = 3;
ALTER TABLE posts AUTO_INCREMENT = 1002;

-------------------------------------------------
-- Optional: Indexes for faster queries
-------------------------------------------------
CREATE INDEX idx_medicines_mid ON medicines(mid);
CREATE INDEX idx_medicines_email ON medicines(email);
