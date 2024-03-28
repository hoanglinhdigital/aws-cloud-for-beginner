-- search base on name
SELECT * 
FROM "student"
WHERE CONTAINS(name, 'Linh');

-- search base on is_married
SELECT * 
FROM "student"
WHERE is_married = false;

-- search base on skill
SELECT * 
FROM "student"
WHERE CONTAINS (skills, 'guitar');

-- search base on hobbies
SELECT * 
FROM "student"
WHERE CONTAINS (hobbies, 'piano');