-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2024-11-27 18:50:47.925

-- tables
-- Table: Channel
CREATE TABLE Channel (
    channel_id int  NOT NULL,
    server_id int  NOT NULL,
    CONSTRAINT channel_id PRIMARY KEY (channel_id)
);

-- Table: Messages
CREATE TABLE Messages (
    message_id int  NOT NULL,
    message_content text  NOT NULL,
    time timestamp  NOT NULL,
    is_pinned boolean  NOT NULL,
    user_id int  NOT NULL,
    channel_id int  NOT NULL,
    CONSTRAINT Messages_pk PRIMARY KEY (message_id)
);

-- Table: Servers
CREATE TABLE Servers (
    server_id int  NOT NULL,
    tag text  NOT NULL,
    num_of_member int  NOT NULL,
    region text  NOT NULL,
    CONSTRAINT Servers_pk PRIMARY KEY (server_id)
);

-- Table: Users
CREATE TABLE Users (
    user_id int  NOT NULL,
    user_name text  NOT NULL,
    CONSTRAINT Users_pk PRIMARY KEY (user_id)
);

-- Table: membership
CREATE TABLE Membership (
    server_id int  NOT NULL,
    user_id int  NOT NULL,
    CONSTRAINT Membership_pk PRIMARY KEY (server_id,user_id)
);

-- foreign keys
-- Reference: Channel_Messages (table: Messages)
ALTER TABLE Messages ADD CONSTRAINT Channel_Messages
    FOREIGN KEY (channel_id)
    REFERENCES Channel (channel_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Messages_Users (table: Messages)
ALTER TABLE Messages ADD CONSTRAINT Messages_Users
    FOREIGN KEY (user_id)
    REFERENCES Users (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Membership_Servers (table: Membership)
ALTER TABLE Membership ADD CONSTRAINT Membership_Servers
    FOREIGN KEY (server_id)
    REFERENCES Servers (server_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: membership_Users (table: membership)
ALTER TABLE Membership ADD CONSTRAINT Membership_Users
    FOREIGN KEY (user_id)
    REFERENCES Users (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

