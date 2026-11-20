\getenv app_password STUDIO_DB_PASSWORD
BEGIN;
CREATE ROLE studio_app LOGIN PASSWORD :'app_password';
ALTER DATABASE studio_db OWNER TO studio_app;
COMMIT;
