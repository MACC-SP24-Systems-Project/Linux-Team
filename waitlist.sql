CREATE DATABASE IF NOT EXISTS waitlist;

USE waitlist;

DROP TABLE IF EXISTS `course`;
DROP TABLE IF EXISTS `student`;
DROP TABLE IF EXISTS `wait_requests`;

-- Create the 'student' table
CREATE TABLE `student` (
  `student_id` INT NOT NULL AUTO_INCREMENT,
  `email_address` VARCHAR(64) NOT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `student_id_UNIQUE` (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Create the 'course' table
CREATE TABLE `course` (
  `course_code` VARCHAR(45) NOT NULL,
  `term` VARCHAR(10) NOT NULL,
  `course_title` VARCHAR(45) NOT NULL,
  `instructor` VARCHAR(45) NOT NULL,
  `seats` VARCHAR(45) NOT NULL,
  `schedule` VARCHAR(45) NOT NULL,
  `location` VARCHAR(45) NOT NULL,
  `credits` DECIMAL(2,0) NOT NULL,
  PRIMARY KEY (`course_code`,`term`),
  KEY `term_idx` (`term`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Create the 'wait_requests' table
CREATE TABLE `wait_requests` (
  `wait_id` INT NOT NULL AUTO_INCREMENT,
  `student_id` INT NOT NULL,
  `course_code` VARCHAR(45) NOT NULL,
  `term` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`wait_id`),
  UNIQUE KEY `wait_id_UNIQUE` (`wait_id`),
  UNIQUE KEY `student_idx` (`student_id`),
  KEY `term_idx` (`term`),
  KEY `course_code_fk_idx` (`course_code`),
  CONSTRAINT `course_code_fk` FOREIGN KEY (`course_code`) REFERENCES `course_data` (`course_code`),
  CONSTRAINT `student_id_fk` FOREIGN KEY (`student_id`) REFERENCES `student_data` (`student_id`),
  CONSTRAINT `term_fk` FOREIGN KEY (`term`) REFERENCES `course_data` (`term`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
