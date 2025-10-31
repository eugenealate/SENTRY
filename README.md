

# &nbsp;SENTRY - Host Intrusion Detection System



Système de détection d'intrusion avancé - Protection temps réel 



&nbsp;  **Table des matières**

\- Installation Rapide (installation-rapide)

\- Fichiers du Projet  (fichiers-du-projet)

\- Confidentialité     (confidentialité)

\- Sécurité            (sécurité)

\- Fonctionnalités     (fonctionnalités)

\- Architecture        (architecture)

\- Performances        (performances) 

\- Contribution        (contribution)

\- Contact



#### &nbsp;**Installation Rapide**



**bash**

&nbsp;1. Installer les dépendances

pip install -r requirements.txt



&nbsp;2. Lancer l'installation

python sentry\_installateur.py



&nbsp;3. Utiliser SENTRY

python sentry\_interface.py





#### &nbsp;**Fichiers du Projet**



· sentry.py - Moteur principal de détection

· sentry\_interface.py - Interface graphique

· sentry\_installateur.py - Script d'installation

· sentry\_liaison.py - Communication entre modules

· requirements.txt - Bibliothèques nécessaires



#### &nbsp; **Confidentialité**



Toutes vos données restent sur votre machine :



·  Aucune information envoyée à l'extérieur

·  Logs chiffrés et stockés localement

·  Aucune collecte de données personnelles

·  Conformité RGPD



#### &nbsp; **Sécurité**



· Chiffrement : AES-256-GCM pour les logs et configurations

· Modules Avancés : Détection comportementale et analyse heuristique

· Protection : Anti-désactivation et persistance automatique

· Intégrité : Vérification des processus et signature numérique



#### &nbsp;**Fonctionnalités**



&nbsp; **Détection Temps Réel**



· Keyloggers : pynput, keylogger.exe

· Ransomwares : Processus suspects

· Cryptominers : Utilisation CPU anormale

· Outils hacking : netcat, mimikatz, metasploit

· Ports backdoor : 4444, 9999, 1337, 31337, 12345



&nbsp; **Surveillance Complète**



· Processus système et comportements

· Connexions réseau et ports

· Utilisation CPU/RAM en temps réel

· Détection de comportements suspects



&nbsp; **Interface Graphique**



· Tableau de bord temps réel

· Alertes visuelles colorées

· Historique des événements

· Paramètres accessibles



#### &nbsp; **Architecture**

#### 



SENTRY/

├── sentry.py               (Cœur du système de détection)

├── sentry\_interface.py     (Interface utilisateur graphique)

├── sentry\_installateur.py  (Installation automatique)

├── sentry\_liaison.py       (Communication entre modules)

└── requirements.txt        ( Dépendances techniques)





#### &nbsp; **Performances**



· CPU : < 3% en utilisation moyenne

· Mémoire : < 80 MB

· Détection : < 5 secondes

· Démarrage : Immédiat

· Stabilité : 24/7 sans intervention



#### &nbsp;**Contribution**



Les retours sont les bienvenues :



·  Signaler un bug

·  Suggérer une amélioration

·  Donner une étoile au projet



#### &nbsp;Contact



Développeur : K. Eugene Alate

Email : eugenealate@gmail.com





SENTRY - La sécurité simplifiée, la protection assurée.

Documentation version 1.0 - Octobre 2025



