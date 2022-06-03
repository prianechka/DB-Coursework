-- Триггер на выполнение ставки
-- Если в таблицу ставок добавилась новая, то с счёта выполнения нужно списать количество денег,
-- равное сумме ставки

CREATE OR REPLACE FUNCTION BK.MakeBet()
returns trigger
AS
    $$
    BEGIN
        UPDATE BK.Account as Acc
        SET Balance = Balance - new.BetSize
        WHERE AccountID = new.AccountID;

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
        if (new.gamestatus = 'Finished') then
            UPDATE Bk.Bet as B
            SET BetStatus = 1
            WHERE B.GameID = new.GameID AND
                  B.ChoosedResult = Bk.getresult(new.GameResult);
            UPDATE Bk.Bet as B
            SET PayoutAmount = B.BetSize * B.koef
            WHERE B.gameid = new.gameid AND betstatus = 1;

            UPDATE BK.Bet as B
            SET betstatus = -1
            WHERE B.GameID = new.GameID AND
                  B.ChoosedResult != Bk.getresult(new.GameResult);

            CALL BK.UpdateBalance(new.gameid);
        end if;
        return new;
    END;
    $$ language plpgsql;
DROP trigger if exists UpdateBetTrigger on BK.Games;
CREATE TRIGGER UpdateBetTrigger AFTER UPDATE ON BK.Games
FOR ROW EXECUTE PROCEDURE BK.UpdateBet();