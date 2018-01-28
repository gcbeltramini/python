## Install

 $ brew install postgresql  # install PostgreSQL in MacOS
 $ initdb /usr/local/var/postgres  # init database

## Usage

### Start the postgres server
 $ postgres -D /usr/local/var/postgres
or
 $ pg_ctl -D /usr/local/var/postgres start
with log
 $ pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start

### Stop the server
 $ pg_ctl -D /usr/local/var/postgres stop

Necessary if you receive this error message after trying to start the server: `FATAL:  lock file "postmaster.pid" already exists`

### Terminal
Open another terminal window

#### Create database "<mydb>"
 $ createdb <mydb>

#### Create user "<my_username>" with password (optional)
 $ createuser -P <my_username>

#### Start interactive terminal

 $ psql <mydb>

 <mydb>=# help

Useful commands:
`\h` (help with SQL commands), `\?` (help with psql commands), `\dt` (list tables), `\d <tablename>` (describe table), `\du` (list roles), `\l` (list databases), `\c ...` (connect to new database).

Location of the database storage area:
 <mydb>=# SHOW data_directory;

SQL commands (remember to end all commands with `;`):

GRANT ALL PRIVILEGES ON ...
CREATE TABLE ...
INSERT INTO ...
COPY <table-bame> FROM '/path/to/file.csv' HEADER [if there is header] DELIMITER ',' CSV;
SELECT * FROM ...
DELETE FROM ...
COPY (SELECT ...) TO '/path/to/file.csv' HEADER DELIMITER ',' CSV;

References:
- https://gist.github.com/lxneng/741932
