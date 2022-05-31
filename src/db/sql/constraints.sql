ALTER TABLE Bk.Account
    ADD CONSTRAINT correctBalance CHECK (Balance >= 0);

ALTER TABLE BK.Account
    ADD CONSTRAINT correctDateBirth CHECK (DateOfBirth <= '2003-12-31'::date);

ALTER TABLE BK.Account
    ADD CONSTRAINT correctPassport CHECK (LENGTH(passportNumber) = 10);

ALTER TABLE BK.Account
    ADD CONSTRAINT correctStatus CHECK (UserStatus = 'Active' OR UserStatus = 'On Verify' OR UserStatus = 'Blocked');

ALTER TABLE BK.Games
    ADD CONSTRAINT correctCoefs CHECK (W1Coef > 1 AND W2Coef > 1 AND DrawCoef > 1);

ALTER TABLE BK.Games
    ADD CONSTRAINT correctSumCoef CHECK ((1 / W1Coef + 1 / W2Coef + 1 / DrawCoef) > 1);

ALTER TABLE BK.Games
    ADD CONSTRAINT correctStatus CHECK (GameStatus = 'Plain' OR GameStatus = 'Live' OR GameStatus = 'Finished')

ALTER TABLE BK.Bet
    ADD CONSTRAINT correctBetResult CHECK (ChoosedResult = 0 OR ChoosedResult = 1 OR ChoosedResult = 2);

ALTER TABLE BK.Bet
    ADD CONSTRAINT correctBetSize CHECK (BetSize >= 10 AND BetSize <= 1000);

ALTER TABLE BK.Bet 
    ADD CONSTRAINT correctCoefBet CHECK (Koef > 1);

ALTER TABLE BK.Bet
    ADD CONSTRAINT correctBetStatus CHECK (BetStatus = 0 OR BetStatus = 1 OR BetStatus = -1);

ALTER TABLE BK.Users
    ADD CONSTRAINT correctLogin CHECK (LENGTH(UserLogin) > 4);

ALTER TABLE BK.Users
    ADD CONSTRAINT correctPassword CHECK (LENGTH(UserPassword) > 4);