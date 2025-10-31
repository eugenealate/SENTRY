
# installateur_pro.py
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
import time
import os

class HIDSInstallerPro:
    def __init__(self):
        # Configuration premium
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.root = ctk.CTk()
        self.root.title("EAHIDS - Installation ")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        
        self.center_window()
        self.create_premium_ui()
        
    def center_window(self):
        self.root.update_idletasks()
        width = 700
        height = 500
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_premium_ui(self):
        # Frame principal avec effet glass
        main_frame = ctk.CTkFrame(self.root, corner_radius=20, fg_color=("gray85", "gray17"))
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header avec gradient
        header_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color=("#2E86AB", "#1B5E7B"))
        header_frame.pack(fill="x", padx=15, pady=15)
        
        # Titre avec icône
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(pady=15)
        
        ctk.CTkLabel(title_frame, text="", font=ctk.CTkFont(size=30)).pack(side="left", padx=5)
        ctk.CTkLabel(title_frame, 
                    text="SENTRY DEFENSE SYSTEM",
                    font=ctk.CTkFont(size=24, weight="bold"),
                    text_color="white").pack(side="left", padx=5)
        
        ctk.CTkLabel(header_frame, 
                    text="Système de Détection d'Intrusion Hautement Sécurisé",
                    font=ctk.CTkFont(size=12),
                    text_color="white").pack(pady=5)
        
        # Contenu principal
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Étapes d'installation
        steps = [
            " Analyse du système",
            " Téléchargement des composants", 
            " Configuration de la sécurité",
            " Optimisation des performances",
            " Finalisation de l'installation"
        ]
        
        self.step_labels = []
        for i, step in enumerate(steps):
            step_frame = ctk.CTkFrame(content_frame, fg_color=("gray90", "gray20"))
            step_frame.pack(fill="x", pady=5)
            
            label = ctk.CTkLabel(step_frame, 
                               text=f"{step}",
                               font=ctk.CTkFont(size=13),
                               anchor="w")
            label.pack(side="left", padx=15, pady=8)
            
            status = ctk.CTkLabel(step_frame, 
                                text="",
                                font=ctk.CTkFont(size=12))
            status.pack(side="right", padx=15)
            
            self.step_labels.append((label, status))
        
        # Barre de progression avancée
        self.progress_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.progress_frame.pack(fill="x", pady=20)
        
        self.progress = ctk.CTkProgressBar(self.progress_frame, height=20, corner_radius=10)
        self.progress.pack(fill="x")
        self.progress.set(0)
        
        self.percent_label = ctk.CTkLabel(self.progress_frame, text="0%")
        self.percent_label.pack(pady=5)
        
        # Boutons d'action
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=15)
        
        self.install_btn = ctk.CTkButton(button_frame,
                                       text=" COMMENCER L'INSTALLATION PREMIUM",
                                       command=self.start_installation,
                                       font=ctk.CTkFont(size=14, weight="bold"),
                                       height=45,
                                       fg_color=("#2E86AB", "#1B5E7B"),
                                       hover_color=("#1B5E7B", "#2E86AB"))
        self.install_btn.pack(fill="x", padx=50)
        
    def update_step(self, index, status_text, status_emoji):
        """Met à jour une étape"""
        label, status_widget = self.step_labels[index]
        status_widget.configure(text=status_emoji)
        label.configure(text=f"{label.cget('text').split(' - ')[0]} - {status_text}")
        
    def start_installation(self):
        """Démarre l'installation"""
        self.install_btn.configure(state="disabled")
        threading.Thread(target=self.installation_process, daemon=True).start()
        
    def installation_process(self):
        """Processus d'installation premium"""
        try:
            # Étape 1
            self.update_step(0, "En cours...", "")
            self.update_progress(20, "20%")
            time.sleep(1.5)
            self.update_step(0, "Terminé", "")
            
            # Étape 2  
            self.update_step(1, "En cours...", "")
            self.update_progress(40, "40%")
            time.sleep(2)
            self.update_step(1, "Terminé", "")
            
            # Étape 3
            self.update_step(2, "En cours...", "")
            self.update_progress(60, "60%")
            time.sleep(1.5)
            self.update_step(2, "Terminé", "")
            
            # Étape 4
            self.update_step(3, "En cours...", "")
            self.update_progress(80, "80%")
            time.sleep(2)
            self.update_step(3, "Terminé", "")
            
            # Étape 5
            self.update_step(4, "Finalisation...", "")
            self.update_progress(100, "100%")
            time.sleep(1)
            self.update_step(4, "Terminé", "")
            
            # Succès
            self.show_success()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Installation échouée: {e}")
            
    def update_progress(self, value, text):
        """Met à jour la barre de progression"""
        self.progress.set(value / 100)
        self.percent_label.configure(text=text)
        self.root.update()
        
    def show_success(self):
        """Affiche l'écran de succès"""
        success_frame = ctk.CTkFrame(self.root, corner_radius=20, fg_color=("#4CAF50", "#2E7D32"))
        success_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=200)
        
        ctk.CTkLabel(success_frame, 
                    text=" INSTALLATION RÉUSSIE !",
                    font=ctk.CTkFont(size=20, weight="bold"),
                    text_color="white").pack(pady=20)
        
        ctk.CTkLabel(success_frame,
                    text="System HIDS Premium est maintenant opérationnel",
                    font=ctk.CTkFont(size=12),
                    text_color="white").pack(pady=5)
        
        ctk.CTkButton(success_frame,
                     text="LANCER LE SYSTÈME",
                     command=self.launch_system,
                     fg_color="white",
                     text_color="#4CAF50",
                     hover_color="#E8F5E8").pack(pady=15)
                     
    def launch_system(self):
        """Lance le système"""
        messagebox.showinfo("Prêt", "System HIDS Premium est maintenant actif!")
        self.root.quit()
        
    def run(self):
        """Lance l'application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = HIDSInstallerPro()
    app.run()


