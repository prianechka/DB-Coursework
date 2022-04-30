-- Триггер на выполнение ставки
-- Если в таблицу ставок добавилась новая, то с счёта выполнения нужно списать количество денег,
-- равное сумме ставки

CREATE OR REPLACE FUNCTION BK.MakeBet()
returns trigger
AS
    $$
    BEGIN
        UPDATE BK.Account as Acc
        SET Acc.Balance = Acc.Balance - new.BetSize
        WHERE Acc.AccountID = new.AccountID;

        return new;
    END;
    $$ language plpgsql;

DROP trigger if exists MakeBetTrigger on BK.Bet;
CREATE TRIGGER MakeBetTrigger AFTER INSERT ON BK.Bet
FOR ROW EXECUTE PROCEDURE BK.MakeBet();

-- Триггер, если для матча стал известен исход, то нужно обновить счета пользователей
CREATE OR REPLACE FUNCTION BK.UpdateBet()
returns trigger
AS
    $$
    BEGIN
        -- Обновляем по ID матча строки ставок с этим матчем
        UPDATE Bk.Bet as B
        SET B.BetStatus = 1 AND B.PayoutAmount = B.BetSize * B.Coef
        WHERE B.GameID = new.GameID AND B.ChoosedResult = new.GameResult;

        UPDATE BK.Bet as B
        SET B.BetStatus = -1
        WHERE B.GameID = new.GameID AND B.ChoosedResult != new.GameResult;

        -- Меняем количество средств на счету игроков
        UPDATE BK.Account as Acc
        SET Acc.Balance = Acc.Balance + BK.Bet.PayoutAmount
        WHERE BK.Bet.GameID = new.GameID AND Acc.AccountID = new.AccountID;
        return new;

    END;
    $$ language plpgsql;

DROP trigger if exists UpdateBetTrigger on BK.Game;
CREATE TRIGGER UpdateBetTrigger AFTER UPDATE ON BK.Game
FOR ROW EXECUTE PROCEDURE BK.UpdateBet();