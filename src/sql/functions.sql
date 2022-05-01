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
        FROM BK.Team as T
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
        SELECT W.webuserid, A.accountid, A.userStatus, A.balance, A.maxbet
        FROM BK.Account as A JOIN BK.WebUsers as W on (A.webuserid = W.webuserid) WHERE W.webUserLogin = webUserLog;
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
        SELECT W.WebUserLogin, W.WebUserPassword, W.UserRole
        FROM BK.WebUsers as W
        WHERE W.WebUserLogin = login AND W.WebUserPassword = password;
    END
$$ language plpgsql;

CREATE OR REPLACE FUNCTION BK.findLogin(login TEXT)
RETURNS TABLE (
                WebUserLogin TEXT
              )
AS $$
    BEGIN
        RETURN QUERY
        SELECT W.WebUserLogin
        FROM BK.WebUsers as W
        WHERE W.WebUserLogin = login;
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
            FROM (BK.Game as G JOIN BK.Team T on (t.teamid = G.team1id)) as tmp JOIN BK.Team as T2 on (tmp.team2id = T2.teamid)
        WHERE (tmp.teamname like name OR T2.teamname like name) AND (gamestatus = 'Live' OR gamestatus = 'Plain')
        ORDER BY gamedate, gametime;
    END;
$$ language plpgsql;

SELECT * FROM BK.viewGamesAnalyze('%')