CREATE OR REPLACE PROCEDURE BK.insertUsers(userEmail TEXT, login TEXT, password TEXT)
AS
    $$
    BEGIN
        INSERT INTO BK.Users(userlogin, userpassword, userrole) VALUES
        (login, password, 'Player');
    END;

    $$ language plpgsql;

CREATE OR REPLACE PROCEDURE BK.insertAccount(id INT, name TEXT, surname TEXT, birth DATE, phone TEXT, passport TEXT, mail TEXT)
AS
    $$
    BEGIN
        INSERT INTO Bk.Account(userid, username, usersurname, dateofbirth, phonenumber, passportnumber, email, creationdate, userstatus, balance, maxbet) VALUES
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
        SELECT into id W.UserID from BK.Users as W WHERE W.userlogin = login;
        CALL BK.InsertAccount(id, name, surname, birth, phone, passport, mail);
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
        INSERT INTO BK.games(gamestatus, team1id, team2id, w1coef, drawcoef, w2coef, gameresult, gamedate, gametime) VALUES
        ('Plain', id1, id2, w1, x, w2, '0:0', matchDate, matchTime);
    END;
$$ language plpgsql;

CREATE OR REPLACE PROCEDURE BK.changeGameState(id INT)
AS
    $$
    DECLARE
        stat TEXT;
    BEGIN
        SELECT G.gamestatus into stat FROM BK.games as G WHERE G.gameid = id;
        if stat = 'Live'
            THEN stat = 'Finished';
        END if;
        if stat = 'Plain' THEN
            stat = 'Live';
        END if;

        UPDATE BK.games
        SET gamestatus = stat
        WHERE gameid = id;
    END;
    $$ language plpgsql;

CREATE OR REPLACE PROCEDURE BK.changeGameResult(id INT, result TEXT)
AS
    $$
    BEGIN
        UPDATE BK.games
        SET gameresult = result
        WHERE gameid = id;
    END;
    $$ language plpgsql;

CREATE OR REPLACE PROCEDURE BK.changeGameCoef(id INT, w1 FLOAT, x FLOAT, w2 FLOAT)
AS
    $$
    BEGIN
        UPDATE BK.games
        SET w1coef = w1, w2coef = w2, drawcoef = x
        WHERE gameid = id;
    END;
    $$ language plpgsql;

CREATE OR REPLACE PROCEDURE BK.MakeBet(choosedGameId INT, result INT, accID INT, betSum FLOAT, kf FLOAT)
AS
    $$
    BEGIN
        INSERT INTO Bk.bet(gameid, choosedresult, accountid, betdate, betsize, koef, betstatus, payoutamount) VALUES
        (choosedGameId, result, accID, CURRENT_TIMESTAMP, betSum, kf, 0, 0);
    END;
    $$ language plpgsql;


CREATE OR REPLACE PROCEDURE BK.Donate(id INT, value FLOAT)
AS
    $$
        BEGIN
            UPDATE Bk.account
            SET balance = balance + value
            WHERE accountid = id;
        END;
    $$ language plpgsql;

CREATE OR REPLACE PROCEDURE BK.UpdateBalance(id int)
AS
    $$
        DECLARE
            tmpAcc RECORD;
            allAccs CURSOR for
            SELECT Acc.accountid, B.payoutamount
            FROM BK.bet as B JOIN BK.Account as Acc on Acc.accountid = B.accountid
            WHERE B.GameID = id and B.betstatus = 1;
        BEGIN
            OPEN allAccs;
            LOOP
                fetch allAccs into tmpAcc;
                UPDATE Bk.account
                SET balance = balance + tmpAcc.payoutamount
                WHERE accountid = tmpAcc.accountid;
                EXIT When not found;
            end loop;
            close allAccs;
        END;
$$ language plpgsql;