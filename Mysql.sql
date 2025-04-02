CREATE TABLE Students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- Create Attendance Table
CREATE TABLE Attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    date DATE NOT NULL,
    status ENUM('Present', 'Absent') NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE
);

-- Create Performance Table
CREATE TABLE Performance (
    performance_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    subject VARCHAR(50) NOT NULL,
    marks INT CHECK (marks BETWEEN 0 AND 100),
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE
);

--  TRIGGER: Update Performance if Attendance is Poor
DELIMITER //
CREATE TRIGGER Check_Attendance_Before_Insert
BEFORE INSERT ON Performance
FOR EACH ROW
BEGIN
    DECLARE attendance_count INT;
    SELECT COUNT(*) INTO attendance_count FROM Attendance
    WHERE student_id = NEW.student_id AND status = 'Present';

    IF attendance_count < 5 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Student has insufficient attendance to be evaluated';
    END IF;
END;
//
DELIMITER ;

--  STORED PROCEDURE: Get Student Performance Report
DELIMITER //
CREATE PROCEDURE GetStudentPerformance(IN stu_id INT)
BEGIN
    SELECT S.name, P.subject, P.marks 
    FROM Students S
    JOIN Performance P ON S.student_id = P.student_id
    WHERE S.student_id = stu_id;
END;
//
DELIMITER ;

--  FUNCTION: Calculate Average Marks
DELIMITER //
CREATE FUNCTION GetAverageMarks(stu_id INT) RETURNS DECIMAL(5,2)
DETERMINISTIC
BEGIN
    DECLARE avg_marks DECIMAL(5,2);
    SELECT AVG(marks) INTO avg_marks FROM Performance WHERE student_id = stu_id;
    RETURN IFNULL(avg_marks, 0);
END;
//
DELIMITER ;

-- 🔥 CURSOR: List Students with Low Attendance
DELIMITER //
CREATE PROCEDURE ListLowAttendanceStudents()
BEGIN
    DECLARE stu_id INT;
    DECLARE stu_name VARCHAR(100);
    DECLARE attendance_count INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE student_cursor CURSOR FOR 
        SELECT S.student_id, S.name, COUNT(A.attendance_id) 
        FROM Students S
        LEFT JOIN Attendance A ON S.student_id = A.student_id AND A.status = 'Present'
        GROUP BY S.student_id, S.name
        HAVING COUNT(A.attendance_id) < 5;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN student_cursor;
    
    read_loop: LOOP
        FETCH student_cursor INTO stu_id, stu_name, attendance_count;
        IF done THEN
            LEAVE read_loop;
        END IF;
        SELECT CONCAT(stu_name, ' has low attendance (', attendance_count, ' days)');
    END LOOP;
    
    CLOSE student_cursor;
END;
//
DELIMITER ;