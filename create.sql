-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2024-11-22 19:30:17.697

-- tables
-- Table: Channel
CREATE TABLE Channel (
    channel_id int  NOT NULL,
    message_id int  NOT NULL,
    CONSTRAINT channel_id PRIMARY KEY (channel_id)
);

-- Table: Messages
CREATE TABLE Messages (
    message_id int  NOT NULL,
    message_content text  NOT NULL,
    time timestamp  NOT NULL,
    is_Pinned boolean  NOT NULL,
    cid int  NOT NULL,
    uid int  NOT NULL,
    CONSTRAINT Messages_pk PRIMARY KEY (message_id)
);

-- Table: Users
CREATE TABLE Users (
    user_ID int  NOT NULL,
    user_name text  NOT NULL,
    CONSTRAINT Users_pk PRIMARY KEY (user_ID)
);

-- foreign keys
-- Reference: Channel_Messages (table: Messages)
ALTER TABLE Messages ADD CONSTRAINT Channel_Messages
    FOREIGN KEY (cid)
    REFERENCES Channel (channel_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Messages_Users (table: Messages)
ALTER TABLE Messages ADD CONSTRAINT Messages_Users
    FOREIGN KEY (uid)
    REFERENCES Users (user_ID)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

