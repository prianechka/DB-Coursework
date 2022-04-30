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