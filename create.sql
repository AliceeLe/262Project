-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2024-11-28 16:21:26.862

-- tables
-- Table: APIDevelopment
CREATE TABLE APIDevelopment (
    channel_id int  NOT NULL,
    bots_id int  NOT NULL,
    CONSTRAINT APIDevelopment_pk PRIMARY KEY (bots_id,channel_id)
);

-- Table: Ads
CREATE TABLE Ads (
    ads_id int  NOT NULL,
    revenue int  NOT NULL,
    tag text  NOT NULL,
    CONSTRAINT Ads_pk PRIMARY KEY (ads_id)
);

-- Table: Bots
CREATE TABLE Bots (
    bots_id int  NOT NULL,
    commands text  NOT NULL,
    CONSTRAINT Bots_pk PRIMARY KEY (bots_id)
);

-- Table: Channel
CREATE TABLE Channel (
    channel_id int  NOT NULL,
    server_id int  NOT NULL,
    CONSTRAINT channel_id PRIMARY KEY (channel_id)
);

-- Table: Members
CREATE TABLE Members (
    user_id int  NOT NULL,
    is_muted boolean  NOT NULL,
    CONSTRAINT Members_pk PRIMARY KEY (user_id)
);

-- Table: Membership
CREATE TABLE Membership (
    server_id int  NOT NULL,
    user_id int  NOT NULL,
    CONSTRAINT Membership_pk PRIMARY KEY (server_id,user_id)
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

-- Table: Moderator
CREATE TABLE Moderator (
    user_id int  NOT NULL,
    CONSTRAINT Moderator_pk PRIMARY KEY (user_id)
);

-- Table: Partnership
CREATE TABLE Partnership (
    channel_id int  NOT NULL,
    ads_id int  NOT NULL,
    CONSTRAINT Partnership_pk PRIMARY KEY (channel_id,ads_id)
);

-- Table: Permisson
CREATE TABLE Permisson (
    user_id int  NOT NULL,
    server_id int  NOT NULL,
    able_customize boolean  NOT NULL,
    able_mute boolean  NOT NULL,
    CONSTRAINT Permisson_pk PRIMARY KEY (user_id,server_id)
);

-- Table: Posts
CREATE TABLE Posts (
    post_id int  NOT NULL,
    post_content text  NOT NULL,
    post_time timestamp  NOT NULL,
    tag text  NOT NULL,
    title text  NOT NULL,
    user_id int  NOT NULL,
    channel_id int  NOT NULL,
    CONSTRAINT Posts_pk PRIMARY KEY (post_id)
);

-- Table: Servers
CREATE TABLE Servers (
    server_id int  NOT NULL,
    tag text  NOT NULL,
    num_of_member int  NOT NULL,
    region text  NOT NULL,
    theme text  NOT NULL,
    CONSTRAINT Servers_pk PRIMARY KEY (server_id)
);

-- Table: Users
CREATE TABLE Users (
    user_id int  NOT NULL,
    user_name text  NOT NULL,
    CONSTRAINT Users_pk PRIMARY KEY (user_id)
);

-- foreign keys
-- Reference: APIDevelopment_Bots (table: APIDevelopment)
ALTER TABLE APIDevelopment ADD CONSTRAINT APIDevelopment_Bots
    FOREIGN KEY (bots_id)
    REFERENCES Bots (bots_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: APIDevelopment_Channel (table: APIDevelopment)
ALTER TABLE APIDevelopment ADD CONSTRAINT APIDevelopment_Channel
    FOREIGN KEY (channel_id)
    REFERENCES Channel (channel_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

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

-- Reference: Partnership_Ads (table: Partnership)
ALTER TABLE Partnership ADD CONSTRAINT Partnership_Ads
    FOREIGN KEY (ads_id)
    REFERENCES Ads (ads_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Partnership_Channel (table: Partnership)
ALTER TABLE Partnership ADD CONSTRAINT Partnership_Channel
    FOREIGN KEY (channel_id)
    REFERENCES Channel (channel_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Permisson_Moderator (table: Permisson)
ALTER TABLE Permisson ADD CONSTRAINT Permisson_Moderator
    FOREIGN KEY (user_id)
    REFERENCES Moderator (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Posts_Channel (table: Posts)
ALTER TABLE Posts ADD CONSTRAINT Posts_Channel
    FOREIGN KEY (channel_id)
    REFERENCES Channel (channel_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Servers_Channel (table: Channel)
ALTER TABLE Channel ADD CONSTRAINT Servers_Channel
    FOREIGN KEY (server_id)
    REFERENCES Servers (server_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Servers_Permisson (table: Permisson)
ALTER TABLE Permisson ADD CONSTRAINT Servers_Permisson
    FOREIGN KEY (server_id)
    REFERENCES Servers (server_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Users_Members (table: Members)
ALTER TABLE Members ADD CONSTRAINT Users_Members
    FOREIGN KEY (user_id)
    REFERENCES Users (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Users_Moderator (table: Moderator)
ALTER TABLE Moderator ADD CONSTRAINT Users_Moderator
    FOREIGN KEY (user_id)
    REFERENCES Users (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Users_Posts (table: Posts)
ALTER TABLE Posts ADD CONSTRAINT Users_Posts
    FOREIGN KEY (user_id)
    REFERENCES Users (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: membership_Servers (table: Membership)
ALTER TABLE Membership ADD CONSTRAINT membership_Servers
    FOREIGN KEY (server_id)
    REFERENCES Servers (server_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: membership_Users (table: Membership)
ALTER TABLE Membership ADD CONSTRAINT membership_Users
    FOREIGN KEY (user_id)
    REFERENCES Users (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

