CREATE DATABASE IF NOT EXISTS waitlist;

USE waitlist;

DROP TABLE IF EXISTS `course`;
DROP TABLE IF EXISTS `student`;
DROP TABLE IF EXISTS `wait_requests`;

-- Create the 'student' table
CREATE TABLE `student` (
    `student_id` INT AUTO_INCREMENT PRIMARY KEY,
    `first_name` VARCHAR(255),
    `last_name` VARCHAR(255)
);

-- Create the 'course' table
CREATE TABLE `course` (
    `course_code` VARCHAR(255),
    `term` VARCHAR(255),
    `title` VARCHAR(255),
    `campus` VARCHAR(255),
    `credits` VARCHAR(255),
    `date` VARCHAR(255),
    `day` VARCHAR(255),
    `faculty` VARCHAR(255),
    `room` VARCHAR(255),
    `seats` VARCHAR(255),
    `status` VARCHAR(255),
    `time` VARCHAR(255),
    PRIMARY KEY (`course_code`, `term`)
);

-- Create the 'wait_requests' table
CREATE TABLE `wait_requests` (
    `wait_id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_id` INT,
    `course_code` VARCHAR(255),
    `term` VARCHAR(255),
    `time` DATETIME,
    FOREIGN KEY (`student_id`) REFERENCES `student`(`student_id`),
    FOREIGN KEY (`course_code`, `term`) REFERENCES `course`(`course_code`, `term`)
);
