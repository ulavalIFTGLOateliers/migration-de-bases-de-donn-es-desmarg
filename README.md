# Atelier sur l'utilisation d'une base de données partagée

## Introduction

Le but de cet atelier est de vous familiariser avec les bonnes pratiques de travail en équipe sur une même base de données - que celle-ci soit hébergée localement sur l'ordinateur de chacun, ou qu'elle soit hébergée dans le cloud.

L'atelier aborde deux sujets:

- La configuration de votre environnement de travail
- La migration de schéma d'une base de données partagée

## Déroulement et correction

Ce document vous indique étape par étape les tâches à réaliser. À tout moment, vous pouvez rouler le script *grading.py* afin d'avoir un aperçu du nombre de tests qui réussissent ou qui échouent.
Afin de lancer le script, il suffit de rouler le main() du fichier, ou de taper la commande:
```shell
python grading.py
```

La correction finale se fera de manière automatique en utilisant les mêmes tests que ceux du script *grading.py*. Vous pouvez donc vous fier à ce script pour savoir si votre code fonctionne ou non.

## Prérequis

Vous devez avoir [MySQL8](https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/) et Python installés sur votre machine.

Plusieurs packages Python sont requis pour ce projet. Afin de tous les installer facilement, roulez la commande:
```shell
pip install -r requirements.txt
```

## Mise en situation et structure du code

Ce projet représente une application web simple représentant un domaine musical. L'application comprend un serveur Flask, une interface HTML ainsi qu'une base de données. Cependant, cette base de données n'est pas encore configurée ni connectée au projet. Ceci sera votre première tâche. Au cours de l'atelier, vous aurez à modifier le fichier *database.py* ainsi que les fichiers migrate_.sql et rollback_.sql situés dans le dossier *scripts/*. Vous n'aurez pas à modifier les autres fichiers. Le schéma initial de la base de données ainsi que les schémas cibles vers lesquels vous aurez à migrer sont illustrés dans le fichier [SCHEMA.md](SCHEMA.md).


## Étape 1 - Configurer votre environnement de travail

Le but de cette étape est de comprendre comment travailler sur une même base de données en équipe. Cet atelier s'effectue sur une base de données hébergée en local sur votre machine, cependant les principes restent les mêmes pour une base de données hébergée sur un cloud.

Lorsque vous travaillez en équipe sur une base de code partagée, vous utilisez un système de gestion du versionnage tel que *Git*. Dans un tel projet, le code servant d'interface vers la BD est commun à tous. Dans le cas de cet atelier, ce code se trouve dans la classe **Database** dans le dossier *database.py*. Cependant, puisque chaque membre de l'équipe héberge sa propre version de la base de données en local sur sa machine, il est impossible d'écrire les informations de connexion directement dans le code, puisque celles-ci diffèrent pour chaque machine. De plus, ceci constituerait une faille de sécurité car n'importe qui ayant accès au repo Github pourrait lire les identifiants de connexion. Comment procéder?

### Utiliser des variables d'environnement

La solution à ce problème est d'utiliser des variables d'environnement. Celles-ci sont des variables externes au programme, dont les valeurs peuvent être récupérées au moment de l'exécution du programme. Chaque membre de l'équipe aura donc ses propres variables d'environnement contenant les informations de connexion à leur BD locale.

Pour commencer, vous devez créer une nouvelle base de données nommée *atelier_bd* sur votre serveur MySQL local:
```sql
CREATE DATABASE atelier_bd;
USE atelier_bd;
```

Maintenant, vous devez créer les variables d'environnement propices à la bonne connexion de l'application à cette base de données. Pour ce faire, une bonne pratique est de mettre ces variables dans un fichier **.env** qui se trouve à la racine de votre projet. Par la suite, il sera possible d'indiquer à l'application d'aller récupérer les valeurs souhaitées directement dans ce fichier.

**Créez un fichier .env à la racine de votre projet.**

**À l'intérieur de ce fichier, vous devez ajouter les variables d'environnement**. Le format d'un fichier **.env** est une paire clé-valeur (nom de la variable ainsi que sa valeur) par ligne:
```
VAR1=VALEUR1
VAR2=VALEUR2
```

Vous devez ajouter les 5 variables d'environnement suivantes, nommées exactement comme ceci:

- HOST: l'adresse de votre serveur SQL. En local, ceci est 127.0.0.1
- PORT: le numéro de port de votre serveur SQL. Par défaut, MySQL roule sur le port 3306
- DATABASE: le nom de votre BD. Dans notre cas, **atelier_bd**
- USER: votre nom d'utilisateur pour votre serveur
- PASSWORD: votre mot de passe


**ATTENTION! Votre fichier .env vous est unique. Il ne doit pas être ajouté au repo Git, car cela constituerait la même faille de sécurité que d'écrire vos identifiants directement dans le code!** Pour que Git ignore ce fichier, il suffit de l'ajouter dans le fichier *.gitignore*. Dans cet atelier, ceci est déjà fait pour vous.


### Récupérer des variables d'environnement

Maintenant que vos variables sont bien créées, il faut les récupérer dans le code de notre application. En Python, il est possible de récupérer une variable d'environnement grâce à la fonction *get()* du module *os.environ*:
```python
import os 

os.environ.get("NOM DE LA VARIABLE")
```
**Remplissez donc les lignes 15 à 19 afin de récupérer les bonnes variables d'environnement telles que vous les avez créées. Attention: la fonction *os.environ.get()* retourne une *string*. Cependant, certaines variables telles que le PORT doivent être un *int*. Vous aurez donc une petite opération à effectuer.**

Par défaut, Python va chercher les variables d'environnement dans votre système. Afin de charger les variables contenues dans un fichier **.env**, il suffit d'utiliser la fonction *load_dotenv()* du package **python-dotenv**:

```python
from dotenv import load_dotenv

load_dotenv()
```
**Placez la fonction *load_dotenv()* à la ligne 14, juste avant de récupérer les valeurs.**


### Tester le tout

La classe *Database* contient tout le code pour se connecter à la BD et l'initialiser à son schéma initial. Si vous avez bien suivi les étapes précédentes, vous pouvez lancer le serveur en tapant la commande:

```shell
python server.py
```
ou en roulant le fichier directement depuis votre IDE. Puis, naviguez à l'URL 127.0.0.1:5000 dans votre navigateur, cliquez sur le bouton *(Re)créer la BD* puis sur le bouton *Rafraîchir*. Vous devriez voir le schéma de départ de la BD.

Si vous souhaitez voir les instructions exactes de mise en route de la BD, référez-vous au fichier *db_scripts/up.sql*.


## Travailler sur une base de données partagée

Maintenant que tous les membres de l'équipe peuvent se connecter à leur instance de BD en roulant le même code, nous allons voir comment apporter des modifications au schéma et aux données afin que tout le monde travaille sur le même état de base de données.

**À noter que dans le contexte d'une base de données hébergée dans un cloud distant, les mêmes principent s'appliquent. Les prochaines étapes s'appliqueraient uniquement à la BD distante au lieu de s'appliquer à chaque membre de l'équipe respectivement.**

### Grands principes

Afin que tous les membres de l'équipe puissent travailler sur le même état de base de données, chaque changement d'un état vers un autre doit être programmé et ajouté au Git afin que tous les membres puissent appliquer la modification. Par exemple, dans ce projet, plusieurs fichiers *.sql* sont présents dans le dossier *db_scripts/*. Ceux-ci permettent à tous les membres d'appliquer les mêmes opérations sur la base de données. Par exemple, le fichier *up.sql* permet d'initialiser la BD à son schéma initial. Afin de rouler ce fichier, vous pouvez à tout moment cliquer sur le bouton *(Re)créer la BD* dans l'interface graphique. Le fichier *drop.sql*, quant à lui, sert à effacer tout le contenu de la BD. Les deux autres fichiers sont vides pour le moment. Vous devrez les compléter dans les prochaines étapes.

## Migration de schéma

Migrer le schéma d'une BD signifie changer les définitions de ses tables. Par exemple, on peut vouloir renommer des attributs, ajouter ou supprimer des colonnes, ajouter des tables, modifier des clés etc. Une migration doit être définie par une suite d'instructions qui peuvent être appliquées au schéma actuel afin de l'amener vers le schéma cible. Dans le contexte d'un travail en équipe, tout changement au schéma de la BD doit être répertorié dans un fichier de migration, afin que tous les membres puissent appliquer les mêmes changements de leur côté. Dans le contexte d'une BD distante, ceci devrait être fait une fois uniquement.

En général, tout changement de schéma doit pouvoir être annulé. C'est ce que l'on appelle une migration arrière, ou *rollback*. En parallèle du fichier de migration, il est important de créer un fichier de *rollback* afin de pouvoir revenir à l'état précédent si cela est nécessaire.

## Empilage de migrations

Grâce à ce processus, il est possible de créer une pile de migrations, c'est-à-dire que plusieurs migrations peuvent être appliquées l'une à la suite de l'autre. En définissant un *rollback* pour chaque migration, il est donc possible de dépiler une migration en appliquant son *rollback*.


## Étape 2 - Première migration

### Migration

Vous allez mettre ce processus en pratique. Vous devez migrer le schéma de la base de données de l'état initial vers l'état numéro 1, défini dans [SCHEMA.md](SCHEMA.md).

Pour ce faire, remplissez le fichier migrate_1.sql avec une suite d'instructions SQL, afin d'obtenir le schéma désiré.

Par exemple, la table *singer* est renommée à *musician*. Vous pouvez faire ceci en écrivant la commande suivante dans le fichier:

```sql
ALTER TABLE singer RENAME TO musician;
```

À tout moment, vous pouvez tester votre migration en cliquant sur le bouton *Migrer* dans l'interface. **Attention: une fois une migration appliquée, si vous souhaitez recommencer ou retester, vous devez remettre la BD dans son état initial en cliquant sur le bouton *(Re)créer la BD*, sinon vous tenterez d'appliquer votre migration au nouveau schéma!**

Si vous obtenez une erreur lors de la migration, regardez la console de votre IDE. Une exception a probablement été lancée.

### Rollback

Une fois votre migration réussie, remplissez le fichier *rollback_1.sql* afin de passer du nouvel état post-migration à l'état initial. Attention, l'ordre des opérations SQL peut avoir une importance!

À chaque test de rollback, assurez-vous de remettre la BD à l'état initial et de ré-appliquer votre migration 1, afin d'être sûr de travailler sur un état propre.


### Tester

Si vous avez bien rempli les deux fichiers, le script de correction devrait afficher que les tests des états *up, migration_1, after_migration_1, rollback_1* et *after_rollback_1* sont tous réussis.


## Effectuer une soumission

Lorsque vous souhaitez effectuer une soumission, il vous suffit de créer un commit et de *push* votre branche master:

```shell
git add -A
git commit -m "Message de commit"
git push origin master
```
