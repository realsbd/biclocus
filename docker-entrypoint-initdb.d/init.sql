DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'biclocus') THEN
        CREATE DATABASE biclocus;
    END IF;
END $$;
