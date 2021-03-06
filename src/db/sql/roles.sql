CREATE ROLE Client NOCREATEDB NOSUPERUSER ;
CREATE ROLE Administrator NOSUPERUSER NOCREATEDB;
CREATE ROLE Analyzist NOSUPERUSER NOCREATEDB;

GRANT ALL PRIVILEGES ON BK.games TO Client;
GRANT ALL PRIVILEGES ON BK.bet TO Client;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA BK TO Client;

GRANT ALL PRIVILEGES ON BK.games TO Analyzist;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA BK TO Analyzist;
GRANT ALL PRIVILEGES ON BK.bet TO Analyzist;
GRANT ALL PRIVILEGES ON BK.teams TO Analyzist;

GRANT ALL PRIVILEGES ON BK.account TO Administrator;
GRANT ALL PRIVILEGES ON BK.users TO Administrator;
GRANT ALL PRIVILEGES ON BK.bet TO Administrator;