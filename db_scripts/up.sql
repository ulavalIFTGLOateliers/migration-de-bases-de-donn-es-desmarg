CREATE TABLE IF NOT EXISTS singer (     singerName varchar(50),
                                        firstName varchar(50),
                                        lastName varchar(50),
                                        age int,
                                        PRIMARY KEY(singerName));
CREATE TABLE IF NOT EXISTS label (      labelName varchar(50),
                                        creation YEAR,
                                        genre varchar(50),
                                        PRIMARY KEY (labelName));
CREATE TABLE IF NOT EXISTS album (      albumName varchar(50),
                                        singerName varchar(50),
                                        year YEAR,
                                        labelName varchar(50),
                                        PRIMARY KEY (albumName),
                                        CONSTRAINT FK_A_singerName FOREIGN KEY (singerName) REFERENCES singer (singerName),
                                        FOREIGN KEY (labelName) REFERENCES label (labelName));

INSERT INTO singer VALUES ("Alina", "Darcy", "Boles", 32), ("Mysterio","Jessie","Chancey",23), ("Rainbow", "Sarah", "Derrick", 47), ("Luna", "Emily", "Seibold", 31);
INSERT INTO label VALUES ("World Music", 2002, "pop"), ("Dark Matter", 2015, "rock"), ("Four Seasons", 1999, "classical");
INSERT INTO album VALUES ("World of Mysteries", "Mysterio", 2019, "Dark Matter"), ("Second Mystery", "Mysterio", 2021, "World Music"), ("Concertos", "Luna", 2009, "Four Seasons");