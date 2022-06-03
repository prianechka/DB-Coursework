DROP SCHEMA BK cascade;
CREATE SCHEMA BK;

CREATE TABLE BK.Users
(
    UserID SERIAL PRIMARY KEY,
    UserLogin TEXT UNIQUE,
    UserPassword TEXT,
    UserRole TEXT);

CREATE TABLE Bk.Account
(
    AccountId SERIAL PRIMARY KEY,
    UserID INT,
    UserName TEXT,
    UserSurname TEXT,
    DateOfBirth DATE,
    PhoneNumber TEXT,
    PassportNumber TEXT,
    Email TEXT,
    CreationDate DATE,
    UserStatus TEXT,
    Balance FLOAT,
    MaxBet INT,
    FOREIGN KEY (UserID) references BK.Users(UserID));

CREATE TABLE BK.Teams
(
    TeamId SERIAL PRIMARY KEY,
    TeamName TEXT,
    TeamCity TEXT,
    Logo TEXT);

CREATE TABLE BK.Games
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
    FOREIGN KEY (Team1ID) references BK.Teams(TeamID) on DELETE CASCADE,
    FOREIGN KEY (Team2ID) references BK.Teams(TeamID) on DELETE CASCADE
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
    FOREIGN KEY (GameID) references BK.Games(GameID),
    FOREIGN KEY (AccountID) references BK.Account(AccountId)
);