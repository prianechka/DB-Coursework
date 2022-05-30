----------------------
-- User Constraints --
----------------------

-- Может быть только положительный баланс на счёте
ALTER TABLE Bk.Account
    ADD CONSTRAINT correctBalance CHECK (Balance >= 0);

-- Пользователям БК должно быть не менее 18 лет
ALTER TABLE BK.Account
    ADD CONSTRAINT correctDateBirth CHECK (DateOfBirth <= '2003-12-31'::date);

-- Паспорт должен быть корректен
ALTER TABLE BK.Account
    ADD CONSTRAINT correctPassport CHECK (LENGTH(passportNumber) = 10);

-- У аккаунта могут быть следующие состояния:
-- 1. Активный - может делать ставки
-- 2. На верификации - данные проверяются в органах
-- 3. Заблокирован - с аккаунта нельзя делать ставки
ALTER TABLE BK.Account
    ADD CONSTRAINT correctStatus CHECK (UserStatus = 'Active' OR UserStatus = 'On Verify' OR UserStatus = 'Blocked');

-- Максимальная ставка может меняться в зависимости от того, как ведёт себя пользователь.
ALTER TABLE BK.Account
    ADD CONSTRAINT correctMaxSum CHECK (MaxBet <= 1000 AND MaxBet >= 10);

----------------------
-- Game Constraints -- 
----------------------

-- Все коэффициенты на матч больше 1, так как в противоположном случае они бессмысленны
ALTER TABLE BK.Game
    ADD CONSTRAINT correctCoefs CHECK (W1Coef > 1 AND W2Coef > 1 AND DrawCoef > 1);

-- Здесь на уровне БД проверяется, что коэффициенты составлены с маржой, то есть вилки нет
ALTER TABLE BK.Game
    ADD CONSTRAINT correctSumCoef CHECK ((1 / W1Coef + 1 / W2Coef + 1 / DrawCoef) > 1);

ALTER TABLE BK.Game
    ADD CONSTRAINT correctStatus CHECK (GameStatus = 'Plain' OR GameStatus = 'Live' OR GameStatus = 'Finished')

---------------------
-- Bet Constraints -- 
---------------------

-- Возможные ставки:
--  0 - Ничья
--  1 - П1
--  2 - П2
ALTER TABLE BK.Bet
    ADD CONSTRAINT correctBetResult CHECK (ChoosedResult = 0 OR ChoosedResult = 1 OR ChoosedResult = 2);

-- Ставка всегда не меньше 10 единиц виртуальной валюты и не больше 1000
ALTER TABLE BK.Bet
    ADD CONSTRAINT correctBetSize CHECK (BetSize >= 10 AND BetSize <= 1000);

-- Правильный коэффициент
ALTER TABLE BK.Bet 
    ADD CONSTRAINT correctCoefBet CHECK (Koef > 1);

-- Возможные состояния ставки:
--  0 - принята
--  1 - выиграна
-- -1 - проиграна
ALTER TABLE BK.Bet
    ADD CONSTRAINT correctBetStatus CHECK (BetStatus = 0 OR BetStatus = 1 OR BetStatus = -1);

---------------------
-- Web Constraints --
---------------------

-- Стандартные требования к пользователю
ALTER TABLE BK.WebUsers
    ADD CONSTRAINT correctLogin CHECK (LENGTH(WebUserLogin) > 4);

ALTER TABLE BK.WebUsers
    ADD CONSTRAINT correctPassword CHECK (LENGTH(WebUserPassword) > 4);