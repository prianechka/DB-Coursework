CALL BK.registrate('priany', 'ghzyz28052001', 'Александр', 'Прянишников', '28.05.2001', '+79080120098', '0415786283', 'mrpriany@mail.ru');

INSERT INTO BK.webusers(email, webuserlogin, webuserpassword, createdat, userrole) VALUES
('admin@mail.ru', 'admin', 'admin', CURRENT_TIMESTAMP, 'Admin');

INSERT INTO BK.webusers(email, webuserlogin, webuserpassword, createdat, userrole) VALUES
('manager@mail.ru', 'manager', '12345', CURRENT_TIMESTAMP, 'Manager');

INSERT INTO BK.webusers(email, webuserlogin, webuserpassword, createdat, userrole) VALUES
('admin@mail.ru', 'analyze', '12345', CURRENT_TIMESTAMP, 'Analyzer');

copy Bk.team FROM '/home/prianechka/Education/BMSTU/DB-CourseWork/DB-Coursework/src/csv/clubsInfo.csv' DELIMITER ',' CSV HEADER;
