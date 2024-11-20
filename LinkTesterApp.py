import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import requests
import pandas as pd
import threading
import validators
import os
import sys
import tempfile
import subprocess
from packaging import version

__version__ = "1.0.5"

class LinkTesterApp:
    def __init__(self, master):
        self.master = master
        master.title("Testeur de Liens")
        master.geometry("900x600")
        master.resizable(False, False)

        # Zone de texte pour les liens
        self.label = tk.Label(master, text="Collez vos liens ci-dessous (un par ligne) :")
        self.label.pack(pady=10)

        self.text = tk.Text(master, height=10, width=110)
        self.text.pack(pady=5)

        # Bouton pour tester les liens
        self.test_button = tk.Button(master, text="Tester les Liens", command=self.test_links)
        self.test_button.pack(pady=10)

        # Zone pour afficher les résultats avec Treeview
        self.result_label = tk.Label(master, text="Résultats :")
        self.result_label.pack()

        # Configuration du Treeview avec trois colonnes
        self.tree = ttk.Treeview(master, columns=("Lien", "Statut", "Commentaire"), show='headings')
        self.tree.heading("Lien", text="Lien")
        self.tree.heading("Statut", text="Statut")
        self.tree.heading("Commentaire", text="Commentaire")

        # Configuration des colonnes
        self.tree.column("Lien", width=400, anchor='w')
        self.tree.column("Statut", width=150, anchor='center')
        self.tree.column("Commentaire", width=300, anchor='w')

        # Ajout d'une barre de défilement verticale
        self.scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side='right', fill='y')
        self.tree.pack(pady=5, fill='both', expand=True)

        # Boutons pour exporter et copier
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

        self.export_button = tk.Button(self.button_frame, text="Exporter en Excel", command=self.export_to_excel, state='disabled')
        self.export_button.pack(side=tk.LEFT, padx=10)

        self.copy_button = tk.Button(self.button_frame, text="Copier les Résultats", command=self.copy_results, state='disabled')
        self.copy_button.pack(side=tk.LEFT, padx=10)

        # Stocker les résultats
        self.results = []

        # Menu pour mises à jour
        self.menu = tk.Menu(master)
        master.config(menu=self.menu)
        self.update_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Mise à jour", menu=self.update_menu)
        self.update_menu.add_command(label="Vérifier les mises à jour", command=self.check_for_updates)

    def test_links(self):
        links = self.text.get("1.0", tk.END).strip().splitlines()
        if not links:
            messagebox.showwarning("Avertissement", "Veuillez coller au moins un lien.")
            return

        # Désactiver les boutons pendant le test
        self.test_button.config(state='disabled')
        self.export_button.config(state='disabled')
        self.copy_button.config(state='disabled')

        # Effacer les résultats précédents
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.results = []

        # Utiliser un thread pour ne pas bloquer l'interface
        threading.Thread(target=self.process_links, args=(links,)).start()

    def process_links(self, links):
        self.results = []
        # Effacer les résultats en cours
        self.tree.delete(*self.tree.get_children())

        for link in links:
            link = link.strip()
            if not link:
                continue  # Ignorer les lignes vides
            if not validators.url(link):
                statut = "Non Fonctionne"
                commentaire = "URL invalide"
            else:
                statut, commentaire = self.check_link(link)
            self.results.append({'Lien': link, 'Statut': statut, 'Commentaire': commentaire})
            self.update_result_tree(link, statut, commentaire)

        # Réactiver le bouton de test
        self.test_button.config(state='normal')

        # Activer les boutons d'export et de copie si des résultats sont présents
        if self.results:
            self.export_button.config(state='normal')
            self.copy_button.config(state='normal')

        messagebox.showinfo("Terminé", "Le test des liens est terminé.")

    def check_link(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                          'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Chrome/58.0.3029.110 Safari/537.3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Referer': 'https://www.google.com/'  # Ajout d'un referer
        }
        session = requests.Session()
        try:
            response = session.get(url, headers=headers, allow_redirects=True, timeout=10, stream=True)
            if response.status_code == 200:
                return "Fonctionne", "OK"
            elif response.status_code == 403:
                return "Non Fonctionne", "Erreur 403 - Accès refusé"
            else:
                return "Non Fonctionne", f"Erreur {response.status_code}"
        except requests.exceptions.Timeout:
            return "Non Fonctionne", "Délai d'attente dépassé"
        except requests.exceptions.ConnectionError:
            return "Non Fonctionne", "Erreur de connexion"
        except requests.exceptions.InvalidURL:
            return "Non Fonctionne", "URL invalide"
        except requests.exceptions.RequestException as e:
            return "Non Fonctionne", str(e)

    def update_result_tree(self, link, statut, commentaire):
        try:
            self.tree.insert("", "end", values=(link, statut, commentaire))
        except IndexError as e:
            print(f"Erreur d'insertion pour {link}: {e}")

    def export_to_excel(self):
        if not self.results:
            messagebox.showwarning("Avertissement", "Il n'y a pas de résultats à exporter.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if file_path:
            df = pd.DataFrame(self.results)
            try:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Succès", f"Résultats exportés vers {file_path}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Échec de l'exportation : {e}")

    def copy_results(self):
        if not self.results:
            messagebox.showwarning("Avertissement", "Il n'y a pas de résultats à copier.")
            return

        result_str = "\n".join([f"{item['Lien']} : {item['Statut']} ({item['Commentaire']})" for item in self.results])
        self.master.clipboard_clear()
        self.master.clipboard_append(result_str)
        messagebox.showinfo("Succès", "Résultats copiés dans le presse-papiers.")

    def check_for_updates(self):
        repo_owner = "Fababidu43"  # Remplacez par votre nom d'utilisateur GitHub
        repo_name = "LinkTesterApp"  # Remplacez par le nom de votre repository
        latest_release = get_latest_release(repo_owner, repo_name)
        if latest_release:
            latest_version = latest_release['tag_name']
            download_url = None
            for asset in latest_release['assets']:
                if asset['name'].endswith('.exe'):  # Suppose votre installer est .exe
                    download_url = asset['browser_download_url']
                    break
            if not download_url:
                messagebox.showerror("Erreur", "Impossible de trouver l'installer de mise à jour.")
                return
            if is_newer_version(__version__, latest_version):
                if messagebox.showyesno("Mise à jour disponible", f"Une nouvelle version {latest_version} est disponible. Voulez-vous la télécharger et l'installer ?"):
                    download_and_run_installer(download_url)
            else:
                messagebox.showinfo("Aucune mise à jour", "Vous avez déjà la dernière version.")
        else:
            messagebox.showerror("Erreur", "Impossible de vérifier les mises à jour.")

def get_latest_release(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def is_newer_version(current_version, latest_version):
    return version.parse(latest_version) > version.parse(current_version)

def download_and_run_installer(download_url):
    local_filename = os.path.join(tempfile.gettempdir(), "update_installer.exe")
    try:
        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du téléchargement de la mise à jour : {e}")
        return

    # Exécuter l'installateur
    try:
        subprocess.Popen([local_filename], shell=True)
        sys.exit()
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'exécution de l'installateur : {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LinkTesterApp(root)
    root.mainloop()
