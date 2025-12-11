CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    department TEXT NOT NULL CHECK (char_length(department) > 1),
    role TEXT NOT NULL CHECK (char_length(role) > 1),
    expected_salary NUMERIC(10,2) CHECK (expected_salary > 0),
    application_date DATE NOT NULL,
    stage TEXT NOT NULL CHECK (stage IN ('Applied', 'Screen', 'Interview', 'Offer', 'Rejected'))
);

INSERT INTO candidates (full_name, department, role, expected_salary, application_date, stage) VALUES
('Иван Петров', 'Data Science', 'Senior Data Analyst', 90000, '2021-01-01', 'Applied'),
('Мария Сидорова', 'Data Platform', 'Senior Data Engineer', 110000, '2023-12-31', 'Screen'),
('Антон Кузнецов', 'Marketing', 'Marketing Specialist', 70000, '2022-06-12', 'Applied'),
('Екатерина Орлова', 'Marketing', 'Marketing Intern', 65000, '2022-07-01', 'Applied'),
('Андрей Николаев', 'Marketing', 'Marketing Manager', 59999, '2022-01-01', 'Applied'),
('Ольга Иванова', 'Marketing', 'Senior Marketing Lead', 80001, '2022-02-01', 'Screen'),
('Григорий Серов', 'Data Analytics', 'Junior Data Analyst', 40000, '2023-03-05', 'Screen'),
('Павел Морозов', 'Operations', 'Operations Test Engineer', 50000, '2015-12-30', 'Rejected'),
('Сергей Тестов', 'Operations', 'Operations Test Manager', 52000, '2014-11-20', 'Rejected'),
('Алексей Кравцов', 'Operations', 'Operations Manager', 55000, '2016-01-01', 'Applied'),
('Тимофей Лисин', 'Engineering', 'Software Engineer', 120000, '2021-06-15', 'Offer'),
('Анна Козлова', 'HR', 'HR Specialist', 50000, '2020-03-10', 'Interview'),
('Елена Белова', 'Data Platform', 'Data Architect', 95000, '2021-05-12', 'Interview'),
('Фёдор Соколов', 'Data Science', 'Senior Data Scientist', 130000, '2022-11-01', 'Screen'),
('Михаил Власов', 'Data Engineering', 'Senior Developer', 100000, '2020-12-31', 'Applied'),
('Владимир Бойцов', 'Data Science', 'Senior Data Researcher', 115000, '2022-09-09', 'Offer'),
('Дмитрий Корнеев', 'Marketing', 'Marketing Coordinator', 65000, '2021-08-10', 'Screen'),
('Роман Романов', 'Marketing', 'Senior Marketing Strategist', 79000, '2023-03-11', 'Applied'),
('Никита Смирнов', 'Marketing', 'Marketing Lead', 80000, '2021-05-05', 'Screen'),
('Юлия Баранова', 'Marketing', 'Marketing Assistant', 60000, '2023-01-10', 'Screen'),
('Артём Чернов', 'Data Science', 'Junior ML Engineer', 85000, '2023-10-01', 'Rejected'),
('Светлана Синицына', 'Operations', 'Operations Test QA', 58000, '2013-02-12', 'Rejected'),
('Олег Новиков', 'Operations', 'Operations Test Helper', 45000, '2012-09-10', 'Rejected'),
('Инга Миронова', 'Data Platform', 'Data Tester', 75000, '2024-02-01', 'Applied'),
('Кирилл Дьяков', 'Engineering', 'Senior Backend Developer', 125000, '2022-04-01', 'Interview');

SELECT *
FROM candidates
WHERE department ILIKE '%data%'
  AND role ILIKE 'senior%'
  AND application_date BETWEEN '2021-01-01' AND '2023-12-31'
ORDER BY full_name;

UPDATE candidates
SET stage = CASE
    WHEN stage = 'Applied' THEN 'Screen'
    WHEN stage = 'Screen' THEN 'Interview'
    WHEN stage = 'Interview' THEN 'Offer'
    ELSE stage
END
WHERE department ILIKE 'marketing'
  AND expected_salary BETWEEN 60000 AND 80000
  AND role NOT ILIKE '%intern%';

DELETE FROM candidates
WHERE department ILIKE 'operations'
  AND application_date < '2016-01-01'
  AND full_name ILIKE '%test%';