CREATE DATABASE duck_collector;

CREATE USER duck_admin WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE duck_collector TO duck_admin;

