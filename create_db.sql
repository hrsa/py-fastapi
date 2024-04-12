SELECT 'CREATE DATABASE fast-api'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'fast_api') \gexec;
SELECT 'CREATE DATABASE testing_fast-api'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'testing_fast_api') \gexec