# Schémas des différents états de la BD

Les attributs soulignés sont les clés primaires.

Les clés étrangères sont indiquées sous les tables. Soit une table **X** dont l'attribut **a** est une clé étrangère vers l'attribut **b** de la table **Y**:
a -> Y.b

## État initial

### singer

| **<ins>singerName</ins>**: varchar(50) | **firstName**: varchar(50) | **lastName**: varchar(50) | **age**: int |
| --- | --- | --- | --- |
| Alina | Darcy | Boles | 32 |
| Mysterio | Jessie | Chancey | 23 |
| Rainbow | Sarah | Derrick | 47 |
| Luna | Emily | Seibold | 31 |


### label

| **<ins>labelName</ins>**: varchar(50) | **creation**: YEAR | **genre**: varchar(50) |
| --- | --- | --- |
| World Music | 2002 | pop |
| Dark Matter | 2015 | rock |
| Four Seasons | 1999 | classical |


### album

| **<ins>albumName</ins>**: varchar(50) | **singerName**: varchar(50) | **year**: YEAR | **labelName**: varchar(50) |
| --- | --- | --- | --- |
| World of Mysteries | Mysterio | 2019 | Dark Matter |
| Second Mystery | Mysterio | 2021 | World Music |
| Concertos | Luna | 2009 | Four Seasons |


singerName -> singer.singerName

labelName -> label.labelName


## Migration 1

### band

| **<ins>bandName</ins>**: varchar(50) | **creation**: YEAR | **genre**: varchar(50) |
| --- | --- | --- |
| Crazy Duo | 2015 | rock |
| Luna | 2009 | classical |
| Mysterio | 2019 | pop |


### musician (ancienne table singer)

| **<ins>musicianName</ins>**: varchar(50) | **firstName**: varchar(50) | **lastName**: varchar(50) | **age**: int | role: varchar(50) | bandName: varchar(50) |
| --- | --- | --- | --- | --- | --- |
| Alina | Darcy | Boles | 32 | vocals | Crazy Duo |
| Mysterio | Jessie | Chancey | 23 | guitar | Mysterio |
| Rainbow | Sarah | Derrick | 47 | percussion | Crazy Duo |
| Luna | Emily | Seibold | 31 | piano | Luna |


### label

| **<ins>labelName</ins>**: varchar(50) | **creation**: YEAR | **genre**: varchar(50) |
| --- | --- | --- |
| World Music | 2002 | pop |
| Dark Matter | 2015 | rock |
| Four Seasons | 1999 | classical |


### album

| **<ins>albumName</ins>**: varchar(50) | **singerName**: varchar(50) | **year**: YEAR | **labelName**: varchar(50) |
| --- | --- | --- | --- |
| World of Mysteries | Mysterio | 2019 | Dark Matter |
| Second Mystery | Mysterio | 2021 | World Music |
| Concertos | Luna | 2009 | Four Seasons |


singerName -> musician.musicianName

labelName -> label.labelName