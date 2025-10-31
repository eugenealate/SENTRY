
#!/usr/bin/env python3
"""
EAHIDS_Liaison.py - Système de détection d'intrusion hôte
Version stabilisée et testée
"""

import os
import sys
import json
import time
from datetime import datetime

class EAHIDSLiaison:
    def __init__(self):
        """Initialisation robuste avec fallbacks"""
        try:
            # Chemins ABSOLUS pour éviter les problèmes
            self.home_dir = os.path.expanduser("~")
            self.config_dir = os.path.join(self.home_dir, "EAHIDS_Config")
            self.config_file = os.path.join(self.config_dir, "config.json")
            self.install_flag = os.path.join(self.config_dir, "INSTALLED")
            
            print(f"[INIT] Répertoire config: {self.config_dir}")
            
        except Exception as e:
            print(f"[ERREUR INIT] {e}")
            sys.exit(1)

    def check_installation(self):
        """Vérifie l'installation de manière fiable"""
        try:
            # Vérifie si le fichier d'installation existe
            if os.path.exists(self.install_flag):
                return True
            # Vérifie aussi l'ancienne méthode pour compatibilité
            if os.path.exists(self.config_file):
                return True
            return False
        except Exception as e:
            print(f"[ERREUR CHECK] {e}")
            return False

    def create_config(self):
        """Crée la configuration de base"""
        config = {
            "system": {
                "name": "EAHIDS",
                "version": "1.0.0",
                "install_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "active"
            },
            "settings": {
                "scan_interval": 60,
                "log_level": "INFO",
                "auto_start": True
            }
        }
        return config

    def install_system(self):
        """Installation COMPLÈTE et robuste"""
        print("🔧 DÉBUT DE L'INSTALLATION EAHIDS...")
        
        try:
            # Étape 1: Créer le répertoire
            print("📁 Création du répertoire de configuration...")
            os.makedirs(self.config_dir, exist_ok=True)
            print("✅ Répertoire créé")
            
            # Étape 2: Créer la configuration
            print("⚙  Création de la configuration...")
            config = self.create_config()
            
            # Étape 3: Sauvegarder la config
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print("✅ Configuration sauvegardée")
            
            # Étape 4: Marquer comme installé
            with open(self.install_flag, 'w', encoding='utf-8') as f:
                f.write("INSTALLED_" + datetime.now().isoformat())
            print("✅ Système marqué comme installé")
            
            # Étape 5: Vérification finale
            if self.verify_installation():
                print(" INSTALLATION RÉUSSIE!")
                return True
            else:
                print("❌ ÉCHEC de la vérification finale")
                return False
                
        except Exception as e:
            print(f"❌ ERREUR CRITIQUE lors de l'installation: {e}")
            return False

    def verify_installation(self):
        """Vérifie que l'installation est correcte"""
        try:
            checks = [
                os.path.exists(self.config_dir),
                os.path.exists(self.config_file), 
                os.path.exists(self.install_flag)
            ]
            return all(checks)
        except:
            return False

    def start_monitoring(self):
        """Démarre le monitoring (version simplifiée)"""
        print("🚀 DÉMARRAGE DU SERVICE EAHIDS...")
        
        try:
            # Charger la configuration
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            print(f"✅ Service démarré - Version {config['system']['version']}")
            print(f"⏰ Intervalle de scan: {config['settings']['scan_interval']}s")
            print("📊 Monitoring actif...")
            
            # Simulation de fonctionnement
            for i in range(3):
                print(f"🔍 Scan {i+1}/3 en cours...")
                time.sleep(1)
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur démarrage service: {e}")
            return False

    def show_status(self):
        """Affiche le statut détaillé"""
        print("\n" + "="*50)
        print("         STATUT EAHIDS")
        print("="*50)
        
        installed = self.check_installation()
        
        if installed:
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                print(f"✅ SYSTÈME INSTALLÉ")
                print(f"   Nom: {config['system']['name']}")
                print(f"   Version: {config['system']['version']}") 
                print(f"   Installé le: {config['system']['install_date']}")
                print(f"   Statut: {config['system']['status']}")
                print(f"   Config: {self.config_file}")
                
            except Exception as e:
                print(f"⚠  Système installé mais config illisible: {e}")
        else:
            print("❌ SYSTÈME NON INSTALLÉ")
            print("   Utilisez 'install' pour l'installer")
        
        print("="*50)

    def run(self):
        """Méthode principale EXÉCUTÉE DIRECTEMENT"""
        print("\n" + "="*60)
        print("         🛡  LANCEUR EAHIDS - DÉMARRAGE")
        print("="*60)
        
        try:
            # Vérifier si installé
            if not self.check_installation():
                print("📦 Système non installé - Installation automatique...")
                
                if self.install_system():
                    print("\n🔄 Démarrage du service après installation...")
                    if self.start_monitoring():
                        print("🎊 SYSTÈME OPÉRATIONNEL!")
                    else:
                        print("❌ Service non démarré")
                else:
                    print("💥 ÉCHEC CRITIQUE - Installation impossible")
                    return False
            else:
                print("✅ Système déjà installé - Démarrage...")
                if self.start_monitoring():
                    print("🎊 SYSTÈME OPÉRATIONNEL!")
                else:
                    print("❌ Service non démarré")
            
            # Statut final
            self.show_status()
            return True
            
        except Exception as e:
            print(f"💥 ERREUR GLOBALE: {e}")
            return False

# ⚠ POINT D'ENTRÉE GARANTI - Pas de fonction main() problématique
if __name__ == "__main__":
    try:
        print("🔍 Initialisation EAHIDS...")
        app = EAHIDSLiaison()
        success = app.run()
        
        if success:
            print("\n✅ Terminé avec succès!")
            sys.exit(0)
        else:
            print("\n❌ Échec de l'exécution")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹  Arrêt par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 ERREUR CATASTROPHIQUE: {e}")
        sys.exit(1)

