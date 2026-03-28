CREATE DATABASE productivity_dashboard;

USE productivity_dashboard;

CREATE TABLE study_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject VARCHAR(100) NOT NULL,
    study_hours FLOAT NOT NULL,
    study_date DATE NOT NULL,
    notes VARCHAR(255)
);
