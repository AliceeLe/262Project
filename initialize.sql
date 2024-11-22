-- drop the Discord database if it exists
DROP database if EXISTS project;

-- create it afresh
CREATE database project;
\c project


\i create.SQL

-- load the data

\copy Users (user_ID, user_name) FROM data/user.csv csv header;
\copy Channel (channel_id, server_id) FROM data/channel.csv csv header;
\copy Messages (message_id,message_content,time,is_pinned,user_id,channel_id) FROM data/message.csv csv header;

