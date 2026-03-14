CREATE DATABASE wildlife_monitoring;
USE wildlife_monitoring;

CREATE TABLE Animals (
    Animal_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Species VARCHAR(50) NOT NULL,
    Age INT NOT NULL,
    Gender ENUM('M','F') NOT NULL,
    Health_Status ENUM('Healthy','Sick') DEFAULT 'Healthy',
    Enclosure_ID INT,
    FOREIGN KEY (Enclosure_ID) REFERENCES Enclosures(Enclosure_ID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);