SELECT 'CREATE DATABASE fast-api'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'fast_api') \gexec