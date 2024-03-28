create database company;
use company;

CREATE TABLE employees (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    salary INT(10) NOT NULL
);


INSERT INTO `company`.`employees`
(
`name`,
`address`,
`salary`)
VALUES
('Linh','Quan 12, TPHCM','5000000'),
('Chien','Quan 1, TPHCM','1000000'),
('Thong','Quan 9, TPHCM','20000000'),
('Hai Huy','Quan 13, TPHCM','5000000');

select * from  employees;

update employees set salary = 30000000 where id = 3;

delete from employees where id = 2;

-- SIMULATE SLOW QUERY
DELIMITER $$
DROP FUNCTION IF EXISTS `iterateSleep` $$
CREATE FUNCTION `iterateSleep` (iterations INT)
RETURNS INT DETERMINISTIC
BEGIN
    DECLARE remainder INT;

    SET remainder = iterations;

    read_loop: LOOP     
        IF remainder=0 THEN
            LEAVE read_loop;
        END IF;

        SELECT SLEEP(2) INTO @test;
        SET remainder = remainder - 1;          
    END LOOP;

    RETURN iterations;
END $$
DELIMITER ;

-- TO TEST IT OUT
SELECT iterateSleep(2);