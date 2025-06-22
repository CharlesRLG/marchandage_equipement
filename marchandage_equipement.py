import tkinter as tk
from tkinter import ttk

# Prix de base pour chaque item
prix_base_armes = {"Épée": 50, "Dague": 30, "Marteau de guerre": 70}
prix_base_armures = {"Casque": 40, "Plastron": 100, "Jambières": 60}
prix_base_bijoux = {"Amulette": 25, "Anneau": 20, "Bracelet": 30}

# Modificateurs de matériaux
materiaux = {
    "Bronze": {"prix": 1.0, "bonus_CA": 0, "magie": False, "intangibles": False},
    "Fer": {"prix": 1.2, "bonus_CA": 1, "magie": False, "intangibles": False},
    "Acier": {"prix": 1.5, "bonus_CA": 2, "magie": True, "intangibles": False},
    "Mithril": {"prix": 2.5, "bonus_CA": 3, "magie": True, "intangibles": True},
}

# Modificateurs de qualité
qualites = {
    "Standard": {"prix": 1.0, "bonus_CA": 0},
    "Maître": {"prix": 1.5, "bonus_CA": 1},
    "Chef-d'œuvre": {"prix": 2.0, "bonus_CA": 2},
}

# Conversion monétaire
def convertir_en_pieces(pc_total):
    po = pc_total // 240
    reste = pc_total % 240
    pa = reste // 12
    pc = reste % 12
    return f"{po} PO, {pa} PA, {pc} PC"

class ItemSelection:
    def __init__(self, parent, item_type, liste_items, prix_base_dict, remove_callback):
        self.frame = ttk.Frame(parent)
        self.frame.pack(pady=2, fill="x")

        self.item_type = item_type
        self.remove_callback = remove_callback
        self.prix_base_dict = prix_base_dict

        self.selected_item = tk.StringVar()
        self.selected_mat = tk.StringVar()
        self.selected_qual = tk.StringVar()
        self.armure_type = tk.StringVar()

        ttk.Combobox(self.frame, textvariable=self.selected_item, values=list(prix_base_dict.keys()), state="readonly", width=15).pack(side="left")
        ttk.Combobox(self.frame, textvariable=self.selected_mat, values=list(materiaux.keys()), state="readonly", width=10).pack(side="left", padx=2)
        ttk.Combobox(self.frame, textvariable=self.selected_qual, values=list(qualites.keys()), state="readonly", width=15).pack(side="left", padx=2)

        if item_type == "Armure":
            ttk.Combobox(self.frame, textvariable=self.armure_type, values=["Légère", "Lourde"], state="readonly", width=10).pack(side="left", padx=2)

        ttk.Button(self.frame, text="❌", width=3, command=self.remove).pack(side="right", padx=5)

    def remove(self):
        self.frame.destroy()
        self.remove_callback(self)

    def get_resume(self):
        if not (self.selected_item.get() and self.selected_mat.get() and self.selected_qual.get()):
            return "", 0, 0

        nom = self.selected_item.get()
        mat = self.selected_mat.get()
        qual = self.selected_qual.get()
        prix_base = self.prix_base_dict.get(nom, 10)

        prix_pc = int(prix_base * materiaux[mat]["prix"] * qualites[qual]["prix"] * 12)  # en PC (12 = 1 PA)
        ca = 0
        effets = []

        if self.item_type == "Armure":
            ca = 5 + materiaux[mat]["bonus_CA"] + qualites[qual]["bonus_CA"]
            if self.armure_type.get() == "Lourde":
                ca *= 2
                prix_pc *= 2
            if materiaux[mat]["magie"]:
                effets.append("Protège des dégâts magiques")
        elif self.item_type == "Arme":
            if materiaux[mat]["intangibles"]:
                effets.append("Peut toucher les créatures intangibles")

        resume = f"{self.item_type}: {nom} ({mat}, {qual}) - Prix: {convertir_en_pieces(prix_pc)}"
        if self.item_type == "Armure":
            resume += f", CA: {ca}"
        if effets:
            resume += f" | Effets: {', '.join(effets)}"

        return resume, prix_pc, ca

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Achat d'Équipement - Jeu de Rôle")
        self.geometry("950x700")

        scroll_frame = ttk.Frame(self)
        scroll_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(scroll_frame)
        self.scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Sections
        self.arm_frame = ttk.LabelFrame(self.scrollable_frame, text="Armes")
        self.arm_frame.pack(fill="x", padx=10, pady=5)
        self.armor_frame = ttk.LabelFrame(self.scrollable_frame, text="Armures")
        self.armor_frame.pack(fill="x", padx=10, pady=5)
        self.bijoux_frame = ttk.LabelFrame(self.scrollable_frame, text="Bijoux")
        self.bijoux_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(self.arm_frame, text="Ajouter une arme", command=self.add_arme).pack(anchor="w", padx=5, pady=2)
        ttk.Button(self.armor_frame, text="Ajouter une armure", command=self.add_armure).pack(anchor="w", padx=5, pady=2)
        ttk.Button(self.bijoux_frame, text="Ajouter un bijou", command=self.add_bijou).pack(anchor="w", padx=5, pady=2)

        self.armes = []
        self.armures = []
        self.bijoux = []

        self.add_arme()
        self.add_armure()
        self.add_bijou()

        self.resume_frame = ttk.LabelFrame(self, text="Résumé et Total")
        self.resume_frame.pack(fill="both", expand=False, padx=10, pady=10)

        ttk.Button(self, text="Mettre à jour le résumé", command=self.update_resume).pack(pady=5)
        self.text = tk.Text(self.resume_frame, height=12)
        self.text.pack(fill="both", expand=True)

    def add_arme(self):
        item = ItemSelection(self.arm_frame, "Arme", prix_base_armes.keys(), prix_base_armes, self.remove_arme)
        self.armes.append(item)

    def add_armure(self):
        item = ItemSelection(self.armor_frame, "Armure", prix_base_armures.keys(), prix_base_armures, self.remove_armure)
        self.armures.append(item)

    def add_bijou(self):
        item = ItemSelection(self.bijoux_frame, "Bijou", prix_base_bijoux.keys(), prix_base_bijoux, self.remove_bijou)
        self.bijoux.append(item)

    def remove_arme(self, item):
        if item in self.armes:
            self.armes.remove(item)

    def remove_armure(self, item):
        if item in self.armures:
            self.armures.remove(item)

    def remove_bijou(self, item):
        if item in self.bijoux:
            self.bijoux.remove(item)

    def update_resume(self):
        self.text.delete(1.0, tk.END)
        total_pc = 0
        ca_total = 0

        for item_list in [self.armes, self.armures, self.bijoux]:
            for item in item_list:
                resume, prix_pc, ca = item.get_resume()
                if resume:
                    self.text.insert(tk.END, resume + "\n")
                    total_pc += prix_pc
                    ca_total += ca

        self.text.insert(tk.END, f"\nTotal: {convertir_en_pieces(total_pc)}\n")
        if ca_total > 0:
            self.text.insert(tk.END, f"CA Totale: {ca_total}\n")

if __name__ == "__main__":
    app = Application()
    app.mainloop()