DROP SCHEMA BK cascade;

CREATE SCHEMA BK;

CREATE TABLE BK.WebUsers
(
    WebUserID SERIAL PRIMARY KEY,
    Email TEXT,
    WebUserLogin TEXT,
    WebUserPassword TEXT,
    CreatedAt TIMESTAMP,
    UserRole TEXT
);

CREATE TABLE Bk.Account
(
    AccountId    SERIAL PRIMARY KEY,
    WebUserID INT,
    UserName TEXT,
    UserSurname TEXT,
    DateOfBirth DATE,
    PhoneNumber TEXT,
    PassportNumber TEXT,
    Email TEXT,
    CreationDate DATE,
    UserStatus TEXT,
    Balance      FLOAT,
    MaxBet       INT,
    FOREIGN KEY (WebUserID) references BK.WebUsers(WebUserID)
);

CREATE TABLE BK.Team
(
    TeamId SERIAL PRIMARY KEY,
    TeamName TEXT,
    TeamCity TEXT,
    Logo TEXT -- будут храниться локальные пути к фоткам
);

CREATE TABLE BK.Game
(
    GameID SERIAL PRIMARY KEY,
    GameStatus TEXT,
    Team1ID INT,
    Team2ID INT,
    W1Coef FLOAT,
    DrawCoef FLOAT,
    W2Coef FLOAT,
    GameResult TEXT,
    GameDate DATE,
    GameTime TIME,
    FOREIGN KEY (Team1ID) references BK.Team(TeamID) on DELETE CASCADE,
    FOREIGN KEY (Team2ID) references BK.Team(TeamID) on DELETE CASCADE
);

CREATE TABLE BK.Bet
(
    BetID SERIAL PRIMARY KEY,
    GameID INT,
    ChoosedResult INT,
    AccountID INT,
    BetDate TIMESTAMP,
    BetSize FLOAT,
    Koef FLOAT,
    BetStatus INT,
    PayoutAmount FLOAT,
    FOREIGN KEY (GameID) references BK.Game(GameID),
    FOREIGN KEY (AccountID) references BK.Account(AccountId)
);