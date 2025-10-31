# interface_pro.py
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import psutil
import time
from datetime import datetime
import threading

class HIDSInterfacePro:
    def __init__(self):
        # Configuration 
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.root = ctk.CTk()
        self.root.title("System HIDS - Tableau de Bord Premium")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)
        
        self.surveillance_active = True
        self.setup_premium_interface()
        self.start_monitoring()
        
    def setup_premium_interface(self):
        """Configure l'interface premium"""
        # Configuration de la grille
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.root, corner_radius=0)
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Sidebar
        self.create_sidebar(main_frame)
        
        # Content area
        self.content_frame = ctk.CTkFrame(main_frame, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=2)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Dashboard par défaut
        self.show_dashboard()
        
    def create_sidebar(self, parent):
        """Crée la sidebar premium"""
        sidebar = ctk.CTkFrame(parent, corner_radius=0, fg_color=("gray90", "gray17"))
        sidebar.grid(row=0, column=0, sticky="nsew", padx=2)
        
        # Logo
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.pack(pady=20)
        
        ctk.CTkLabel(logo_frame, text="🛡", font=ctk.CTkFont(size=35)).pack()
        ctk.CTkLabel(logo_frame, 
                    text="HIDS\nSECURITY", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=("#2E86AB", "#2E86AB"),
                    justify="center").pack()
        
        # Menu
        menu_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        menu_frame.pack(fill="x", pady=20)
        
        menu_items = [
            ("📊 Tableau de Bord", "dashboard"),
            ("🚨 Alertes", "alertes"),
            ("⚙ Paramètres", "parametres"),
            ("📈 Performances", "performances"),
            ("🔒 Sécurité", "securite")
        ]
        
        self.menu_buttons = {}
        for text, key in menu_items:
            btn = ctk.CTkButton(menu_frame,
                              text=text,
                              command=lambda k=key: self.show_section(k),
                              anchor="w",
                              fg_color="transparent",
                              hover_color=("gray80", "gray25"))
            btn.pack(fill="x", padx=10, pady=5)
            self.menu_buttons[key] = btn
        
        # Statut système
        status_frame = ctk.CTkFrame(sidebar, fg_color=("#4CAF50", "#2E7D32"), corner_radius=10)
        status_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(status_frame, 
                    text="🟢 SYSTÈME ACTIF",
                    text_color="white",
                    font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        ctk.CTkLabel(status_frame,
                    text="Toutes les protections sont activées",
                    text_color="white",
                    font=ctk.CTkFont(size=10)).pack(pady=5)
        
    def show_section(self, section):
        """Affiche une section"""
        for btn in self.menu_buttons.values():
            btn.configure(fg_color="transparent")
        
        self.menu_buttons[section].configure(fg_color=("gray75", "gray30"))
        
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        if section == "dashboard":
            self.show_dashboard()
        elif section == "alertes":
            self.show_alertes()
        elif section == "parametres":
            self.show_parametres()
            
    def show_dashboard(self):
        """Affiche le tableau de bord"""
        # Header
        header = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(header,
                    text=" TABLEAU DE BORD PRINCIPAL",
                    font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w")
        
        ctk.CTkLabel(header,
                    text="Surveillance en temps réel de votre système",
                    font=ctk.CTkFont(size=12),
                    text_color="gray").pack(anchor="w")
        
        # Métriques en temps réel
        metrics_frame = ctk.CTkFrame(self.content_frame, corner_radius=15)
        metrics_frame.pack(fill="x", padx=20, pady=10)
        
        # Grille 2x2 pour les métriques
        for i in range(2):
            metrics_frame.grid_columnconfigure(i, weight=1)
        
        self.cpu_metric = self.create_metric_card(metrics_frame, "💻 CPU", "0%", 0, 0)
        self.ram_metric = self.create_metric_card(metrics_frame, "🧠 MÉMOIRE", "0%", 0, 1)
        self.disk_metric = self.create_metric_card(metrics_frame, "💾 DISQUE", "0%", 1, 0)
        self.network_metric = self.create_metric_card(metrics_frame, "🌐 RÉSEAU", "0 KB/s", 1, 1)
        
        # Alertes récentes
        alert_frame = ctk.CTkFrame(self.content_frame, corner_radius=15)
        alert_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(alert_frame,
                    text="🚨 ALERTES RÉCENTES",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=20, pady=15)
        
        # Tableau d'alertes
        columns = ('Heure', 'Type', 'Gravité', 'Description')
        self.alert_tree = ttk.Treeview(alert_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.alert_tree.heading(col, text=col)
            self.alert_tree.column(col, width=120)
        
        self.alert_tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Données d'exemple
        sample_alerts = [
            ("10:23:15", "CPU", "Moyenne", "Utilisation CPU à 85%"),
            ("10:20:45", "Mémoire", "Faible", "Utilisation mémoire à 78%"),
            ("10:15:30", "Sécurité", "Critique", "Processus suspect détecté")
        ]
        
        for alert in sample_alerts:
            self.alert_tree.insert('', 'end', values=alert)
            
    def create_metric_card(self, parent, title, value, row, col):
        """Crée une carte de métrique"""
        card = ctk.CTkFrame(parent, corner_radius=10)
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14)).pack(pady=(15, 5))
        
        value_label = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=24, weight="bold"))
        value_label.pack(pady=5)
        
        progress = ctk.CTkProgressBar(card, height=8, corner_radius=4)
        progress.pack(fill="x", padx=15, pady=10)
        progress.set(0)
        
        return {"value": value_label, "progress": progress}
    
    def show_alertes(self):
        """Affiche la page des alertes"""
        content = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(content,
                    text="🚨 GESTION DES ALERTES",
                    font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=10)
        
        ctk.CTkLabel(content,
                    text="Historique complet des incidents de sécurité",
                    font=ctk.CTkFont(size=12),
                    text_color="gray").pack(anchor="w", pady=5)
                    
    def show_parametres(self):
        """Affiche la page des paramètres"""
        content = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(content,
                    text="⚙ PARAMÈTRES AVANCÉS",
                    font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=10)
        
    def start_monitoring(self):
        """Démarre la surveillance"""
        def monitor():
            while self.surveillance_active:
                try:
                    # CPU
                    cpu_percent = psutil.cpu_percent()
                    self.cpu_metric["value"].configure(text=f"{cpu_percent:.1f}%")
                    self.cpu_metric["progress"].set(cpu_percent / 100)
                    
                    # Mémoire
                    memory = psutil.virtual_memory()
                    self.ram_metric["value"].configure(text=f"{memory.percent:.1f}%")
                    self.ram_metric["progress"].set(memory.percent / 100)
                    
                    # Disque
                    disk = psutil.disk_usage('/')
                    disk_percent = (disk.used / disk.total) * 100
                    self.disk_metric["value"].configure(text=f"{disk_percent:.1f}%")
                    self.disk_metric["progress"].set(disk_percent / 100)
                    
                    time.sleep(2)
                except:
                    pass
                    
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
        
    def run(self):
        """Lance l'application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = HIDSInterfacePro()
    app.run()

