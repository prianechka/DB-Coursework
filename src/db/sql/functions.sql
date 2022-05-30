CREATE OR REPLACE FUNCTION BK.viewTeams(myTeamName TEXT)
RETURNS TABLE (
                teamid INT,
                teamname TEXT,
                teamcity TEXT
              )
AS $$
    BEGIN
        RETURN query
        SELECT T.teamid, T.teamname, T.teamcity
        FROM BK.Teams as T
        WHERE T.teamname like myTeamName;
    END
$$ language plpgsql;

CREATE OR REPLACE FUNCTION BK.verifyAccs(surnameString TEXT)
RETURNS TABLE (
                AccountId  INT,
                UserName TEXT,
                UserSurname TEXT,
                PassportNumber TEXT,
                PhoneNumber TEXT,
                Email TEXT
              )
AS $$
    BEGIN
        RETURN QUERY
        SELECT A.accountid, A.username, A.usersurname, A.passportnumber, A.phonenumber, A.email
        FROM BK.Account as A
        WHERE A.userstatus = 'On Verify' and A.usersurname like surnameString;
    END
$$ language plpgsql;

CREATE OR REPLACE FUNCTION BK.getUserInfo(webUserLog TEXT)
RETURNS TABLE (
                WebUserID  INT,
                AccountID INT,
                UserStatus TEXT,
                Balance FLOAT,
                MaxBet INT
              )
AS $$
    BEGIN
        RETURN QUERY
        SELECT W.userid, A.accountid, A.userStatus, A.balance, A.maxbet
        FROM BK.Account as A JOIN BK.Users as W on (A.userid = W.userid) WHERE W.UserLogin = webUserLog;
    END
$$ language plpgsql;

CREATE OR REPLACE FUNCTION BK.auth(login TEXT, password TEXT)
RETURNS TABLE (
                WebUserLogin TEXT,
                WebUserPassword TEXT,
                UserRole TEXT
              )
AS $$
    BEGIN
        RETURN QUERY
        SELECT W.UserLogin, W.UserPassword, W.UserRole
        FROM BK.Users as W
        WHERE W.UserLogin = login AND W.UserPassword = password;
    END
$$ language plpgsql;

CREATE OR REPLACE FUNCTION BK.findLogin(login TEXT)
RETURNS TABLE (
                WebUserLogin TEXT
              )
AS $$
    BEGIN
        RETURN QUERY
        SELECT W.UserLogin
        FROM BK.Users as W
        WHERE W.UserLogin = login;
    END
$$ language plpgsql;

CREATE OR REPLACE FUNCTION BK.viewGamesAnalyze(name TEXT)
RETURNS TABLE (
                id int,
                matchdate DATE,
                matchtime TIME,
                t1name TEXT,
                t2name TEXT,
                status TEXT,
                result TEXT,
                w1cf FLOAT,
                xcf FLOAT,
                w2cf FLOAT
              )
AS $$
    BEGIN
        RETURN QUERY
        SELECT gameid, gamedate, gametime, tmp.teamname, T2.teamname, gamestatus, gameresult, w1coef, drawcoef, w2coef
            FROM (BK.Games as G JOIN BK.Teams T on (t.teamid = G.team1id)) as tmp
                JOIN BK.Teams as T2 on (tmp.team2id = T2.teamid)
        WHERE (tmp.teamname like name OR T2.teamname like name)
          AND (gamestatus = 'Live' OR gamestatus = 'Plain')
        ORDER BY gamedate, gametime;
    END;
$$ language plpgsql;

CREATE OR REPLACE FUNCTION BK.GetBetHistory(id INT)
RETURNS TABLE (
                betID INT,
                BetDate TIMESTAMP,
                firstTeam TEXT,
                secondTeam TEXT,
                choosedRes INT,
                koef FLOAT,
                betSize FLOAT,
                result INT,
                pay FLOAT
              )
AS $$
    BEGIN
        RETURN QUERY
        SELECT B.betid, B.betdate, tmp.teamname, t2.teamname, B.choosedresult, B.koef, B.betsize, B.betstatus, B.payoutamount
        FROM BK.account as A JOIN Bk.Bet as B on (A.accountid = b.accountid)
            JOIN (BK.Games as G JOIN BK.Teams T on (t.teamid = G.team1id)) as tmp on (tmp.gameid = B.gameid)
                JOIN BK.Teams as T2 on (tmp.team2id = T2.teamid)
        WHERE A.accountid = id
        ORDER BY B.betdate;
    end;
$$ language plpgsql;

CREATE OR REPLACE FUNCTION BK.GetResult(gameResult TEXT)
RETURNS integer
AS
$$
    DECLARE firstGoal TEXT;
            secondGoal TEXT;
            middlePos INT;
            len INT;
    BEGIN
        len = length(gameResult);
        middlePos = position(':' in gameResult);
        firstGoal = substring(gameResult from 0 for middlePos);
        secondGoal = substring(gameResult from middlePos + 1 for len);

        if firstGoal > secondGoal
            then return 1;
        end if;
        if firstGoal < secondGoal
            then return 2;
        end if;
        if firstGoal = secondGoal
            then return 0;
        end if;
    END;
$$ language plpgsql;

CREATE OR REPLACE FUNCTION BK.GetROI(id int)
RETURNS FLOAT
AS
    $$
    DECLARE Result int;
    BEGIN
        SELECT sum(payoutamount) - sum(betsize) into Result
        FROM BK.bet as B
        WHERE accountid = id;

        RETURN Result;
    end;
    $$ language plpgsql;


CREATE OR REPLACE FUNCTION BK.GetAllActiveAccs()
RETURNS TABLE (
                accId int,
                accLogin TEXT,
                accName TEXT,
                accSurname TEXT,
                accBalance FLOAT,
                accROI FLOAT
              )
AS $$
    BEGIN
        RETURN QUERY
        SELECT A.accountid, W.userlogin, A.username, A.usersurname, A.balance, sum(B.payoutamount) - sum(B.betsize)
        FROM BK.account as A JOIN BK.users as W on (A.userid = W.userid)
        FULL OUTER JOIN BK.bet as B on (A.accountid = b.accountid)
        WHERE A.userstatus = 'Active'
        GROUP BY A.accountid, W.userlogin;
    end;
$$ language plpgsql;
