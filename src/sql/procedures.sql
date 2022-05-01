CREATE OR REPLACE PROCEDURE BK.insertUsers(userEmail TEXT, login TEXT, password TEXT)
AS
    $$
    BEGIN
        INSERT INTO BK.WebUsers(email, webuserlogin, webuserpassword, createdat, userrole) VALUES
        (userEmail, login, password, CURRENT_TIMESTAMP, 'Player');
    END;

    $$ language plpgsql;

CREATE OR REPLACE PROCEDURE BK.insertAccount(id INT, name TEXT, surname TEXT, birth DATE, phone TEXT, passport TEXT, mail TEXT)
AS
    $$
    BEGIN
        INSERT INTO Bk.Account(webuserid, username, usersurname, dateofbirth, phonenumber, passportnumber, email, creationdate, userstatus, balance, maxbet) VALUES
        (id, name, surname, birth, phone, passport, mail, CURRENT_TIMESTAMP, 'On Verify', 0, 1000);
    END;

    $$ language plpgsql;

CREATE OR REPLACE PROCEDURE BK.registrate(login TEXT, password TEXT, name TEXT, surname TEXT, birth DATE, phone TEXT, passport TEXT, mail TEXT)
AS
    $$
    DECLARE
        id INT;
    BEGIN
        CALL BK.InsertUsers(mail, login, password);
        SELECT into id W.WebUserID from BK.WebUsers as W WHERE W.webuserlogin = login;
        CALL BK.InsertAccount(id, name, surname, birth, phone, passport, mail);
        COMMIT;
    END;
$$ language plpgsql;

CREATE OR REPLACE PROCEDURE BK.updateStatus(id INT, status TEXT)
AS
    $$
    BEGIN
        UPDATE Bk.Account
        SET userstatus = status
        WHERE  accountid = id;
    END;
$$ language plpgsql;

CREATE OR REPLACE PROCEDURE BK.addGame(id1 INT, id2 INT, w1 FLOAT, x FLOAT, w2 FLOAT, matchDate DATE, matchTime TIME)
AS
    $$
    BEGIN
        INSERT INTO BK.game(gamestatus, team1id, team2id, w1coef, drawcoef, w2coef, gameresult, gamedate, gametime) VALUES
        ('Plain', id1, id2, w1, x, w2, '0:0', matchDate, matchTime);
    END;
$$ language plpgsql;

CREATE OR REPLACE PROCEDURE BK.changeGameState(id INT)
AS
    $$
    DECLARE
        stat TEXT;
    BEGIN
        SELECT G.gamestatus into stat FROM BK.game as G WHERE G.gameid = id;
        if stat = 'Live'
            THEN stat = 'Finished';
        END if;
        if stat = 'Plain' THEN
            stat = 'Live';
        END if;

        UPDATE BK.game
        SET gamestatus = stat
        WHERE gameid = id;
    END;
    $$ language plpgsql;

CREATE OR REPLACE PROCEDURE BK.changeGameResult(id INT, result TEXT)
AS
    $$
    BEGIN
        UPDATE BK.game
        SET gameresult = result
        WHERE gameid = id;
    END;
    $$ language plpgsql;

CREATE OR REPLACE PROCEDURE BK.changeGameCoef(id INT, w1 FLOAT, x FLOAT, w2 FLOAT)
AS
    $$
    BEGIN
        UPDATE BK.game
        SET w1coef = w1, w2coef = w2, drawcoef = x
        WHERE gameid = id;
    END;
    $$ language plpgsql;

CALL BK.changeGameCoef(11, 2.86, 2.86, 2.86);