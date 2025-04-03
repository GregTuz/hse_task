CREATE DATABASE airflow_meta;

\connect airflow_meta;

CREATE USER airflow_writer WITH PASSWORD 'airflow_writer_password';
GRANT CONNECT ON DATABASE airflow_meta TO airflow_writer;
GRANT CREATE ON SCHEMA public TO airflow_writer;
GRANT USAGE, SELECT ON SEQUENCE log_id_seq TO airflow_writer;
GRANT USAGE ON SCHEMA public TO airflow_writer;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT INSERT, UPDATE, SELECT ON TABLES TO airflow_writer;

CREATE TABLE IF NOT EXISTS log (
    id SERIAL PRIMARY KEY,
    dttm TIMESTAMPTZ NOT NULL,     -- Время события
    event VARCHAR(255) NOT NULL,    -- Событие
    owner VARCHAR(255) NOT NULL,    -- Владелец
    extra JSON NOT NULL             -- Дополнительная информация (например, контекст ошибки)
);