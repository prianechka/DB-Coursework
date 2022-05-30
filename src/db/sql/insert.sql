CALL BK.registrate('priany', 'ghzyz28052001', 'Александр', 'Прянишников', '28.05.2001', '+79080120098', '0415786283', 'mrpriany@mail.ru');

INSERT INTO BK.users(userlogin, userpassword, userrole) VALUES
('admin', 'admin', 'Admin');

INSERT INTO BK.users(userlogin, userpassword, userrole) VALUES
('analyze', '12345', 'Analyzer');

copy Bk.teams FROM '/home/prianechka/Education/BMSTU/DB-CourseWork/DB-Coursework/src/csv/clubsInfo.csv' DELIMITER ',' CSV HEADER;
