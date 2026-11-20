\getenv site_role SITE_ROLE
\getenv site_password SITE_PASSWORD
\getenv site_db POSTGRES_DB
BEGIN;
CREATE ROLE :"site_role" LOGIN PASSWORD :'site_password';
ALTER DATABASE :"site_db" OWNER TO :"site_role";
REVOKE CONNECT ON DATABASE :"site_db" FROM PUBLIC;
GRANT CONNECT ON DATABASE :"site_db" TO :"site_role";
COMMIT;
