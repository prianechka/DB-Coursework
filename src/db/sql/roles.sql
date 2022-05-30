CREATE ROLE Client NOCREATEDB NOSUPERUSER ;
CREATE ROLE Administrator NOSUPERUSER NOCREATEDB;
CREATE ROLE Analyzist NOSUPERUSER NOCREATEDB;

-- Игрок
GRANT ALL PRIVILEGES ON SCHEMA BK TO Client;
GRANT ALL PRIVILEGES ON BK.account TO Client;
GRANT ALL PRIVILEGES ON BK.game TO Client;

-- Анализатор
GRANT ALL PRIVILEGES ON SCHEMA BK TO Analyzist;
GRANT ALL PRIVILEGES ON BK.game TO Analyzist;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA BK TO Analyzist;
GRANT ALL PRIVILEGES ON BK.bet TO Analyzist;
GRANT ALL PRIVILEGES ON BK.account TO Analyzist;
GRANT ALL PRIVILEGES ON BK.team TO Analyzist;


-- Админ
GRANT ALL PRIVILEGES ON SCHEMA BK TO Administrator;
GRANT ALL PRIVILEGES ON BK.account TO Administrator;
GRANT ALL PRIVILEGES ON BK.webusers TO Administrator;
GRANT ALL PRIVILEGES ON BK.bet TO Administrator;