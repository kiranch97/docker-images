SELECT 'CREATE DATABASE odk'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'odk')\gexec