-- drop the Discord database if it exists
DROP database if EXISTS Discord;

-- create it afresh
CREATE database Discord;
\c Discord


\i create.SQL

-- load the data

\copy Users (user_ID, user_name) FROM data/users.csv csv header;
\copy Messages (message_id, message_content, time, is_Pinned, cid, uid) FROM data/issues.csv csv header;
\copy Channel (channel_id, message_id) FROM data/bugs.csv csv header;
