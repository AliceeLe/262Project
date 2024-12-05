-- drop the Discord database if it exists
DROP database if EXISTS project;

-- create it afresh
CREATE database project;
\c project


\i create.SQL

-- load the data

\copy Users (user_id, user_name) FROM data/user.csv csv header;
\copy Servers (server_id, tag, num_of_member, region, theme) FROM data/server.csv csv header;
\copy Channel (channel_id, server_id) FROM data/channel.csv csv header;
\copy Membership (user_id, server_id) FROM data/membership.csv csv header;
\copy Messages (message_id,message_content,time,is_pinned,user_id,channel_id) FROM data/message.csv csv header;
\copy Posts (post_id, post_content, post_time, tag, title, user_id, channel_id) FROM data/posts.csv csv header;
\copy Bots (bots_id,commands) FROM data/bot.csv csv header;
\copy APIDevelopment (channel_id,bots_id) FROM data/api.csv csv header;


