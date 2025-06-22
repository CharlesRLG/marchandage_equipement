import tkinter as tk
from tkinter import ttk

# Données de base
categories = {
    "Armes": {"items": ["Épée", "Dague", "Marteau de guerre"], "has_material": True, "has_quality": True},
    "Armes à distance": {"items": ["Arc", "Arbalète"], "has_material": True, "has_quality": True},
    "Armures": {"items": ["Casque", "Plastron", "Jambières"], "has_material": True, "has_quality": True, "has_type": True},
    "Bijoux": {"items": ["Anneau", "Amulette"], "has_material": True, "has_quality": True},
    "Potions": {"items": ["Potion de soin", "Potion de mana"], "has_material": False, "has_quality": True},
    "Animaux": {"items": ["Cheval", "Chien", "Faucon"], "has_material": False, "has_quality": True},
    "Outils": {"items": ["Marteau de forgeron", "Pelle", "Pioche"], "has_material": True, "has_quality": True}
}

materials = {
    "Bois": {"price_mod": 0.8, "effect": ""},
    "Fer": {"price_mod": 1.0, "effect": ""},
    "Acier": {"price_mod": 1.5, "effect": "Magique"},
    "Argent": {"price_mod": 2.0, "effect": "Intangible"},
    "Mythril": {"price_mod": 3.0, "effect": "Magique & Intangible"}
}

qualities = {
    "Commun": 1.0,
    "Bon": 1.5,
    "Excellent": 2.0,
    "Chef-d'œuvre": 3.0
}

base_prices = {
    "Épée": 100, "Dague": 60, "Marteau de guerre": 120,
    "Arc": 90, "Arbalète": 110,
    "Casque": 50, "Plastron": 150, "Jambières": 100,
    "Anneau": 200, "Amulette": 180,
    "Potion de soin": 50, "Potion de mana": 70,
    "Cheval": 500, "Chien": 150, "Faucon": 300,
    "Marteau de forgeron": 80, "Pelle": 40, "Pioche": 60
}

ca_values = {"Casque": 1, "Plastron": 3, "Jambières": 2}

# Fonctions de conversion

def convert_price_to_text(total_cp):
    po = total_cp // 240
    reste = total_cp % 240
    pa = reste // 12
    pc = reste % 12
    return f"{po} PO, {pa} PA, {pc} PC"

# Application
class RPGShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Magasin de JDR")
        self.root.geometry("800x700")

        self.items = []

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.main_frame)
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.build_interface()

    def build_interface(self):
        self.category_var = tk.StringVar()
        self.item_var = tk.StringVar()
        self.material_var = tk.StringVar()
        self.quality_var = tk.StringVar()
        self.armor_type_var = tk.StringVar()

        tk.Label(self.scrollable_frame, text="Catégorie").pack()
        self.category_menu = ttk.Combobox(self.scrollable_frame, textvariable=self.category_var, values=list(categories.keys()))
        self.category_menu.pack()
        self.category_menu.bind("<<ComboboxSelected>>", self.update_items)

        tk.Label(self.scrollable_frame, text="Objet").pack()
        self.item_menu = ttk.Combobox(self.scrollable_frame, textvariable=self.item_var)
        self.item_menu.pack()

        tk.Label(self.scrollable_frame, text="Matériau").pack()
        self.material_menu = ttk.Combobox(self.scrollable_frame, textvariable=self.material_var, values=list(materials.keys()))
        self.material_menu.pack()

        tk.Label(self.scrollable_frame, text="Qualité").pack()
        self.quality_menu = ttk.Combobox(self.scrollable_frame, textvariable=self.quality_var, values=list(qualities.keys()))
        self.quality_menu.pack()

        self.armor_type_menu = ttk.Combobox(self.scrollable_frame, textvariable=self.armor_type_var, values=["Légère", "Lourde"])
        self.armor_type_menu.pack()

        tk.Button(self.scrollable_frame, text="Ajouter", command=self.add_item).pack()

        self.summary_label = tk.Label(self.scrollable_frame, text="Résumé:")
        self.summary_label.pack()
        self.summary_text = tk.Text(self.scrollable_frame, height=20, width=80)
        self.summary_text.pack()

        self.total_label = tk.Label(self.scrollable_frame, text="Total: 0 PO, 0 PA, 0 PC")
        self.total_label.pack()

    def update_items(self, event):
        cat = self.category_var.get()
        self.item_menu["values"] = categories[cat]["items"]
        if categories[cat].get("has_material"):
            self.material_menu.configure(state="normal")
        else:
            self.material_menu.set("")
            self.material_menu.configure(state="disabled")

        if categories[cat].get("has_type"):
            self.armor_type_menu.configure(state="normal")
        else:
            self.armor_type_menu.set("")
            self.armor_type_menu.configure(state="disabled")

    def add_item(self):
        cat = self.category_var.get()
        item = self.item_var.get()
        mat = self.material_var.get()
        qual = self.quality_var.get()
        armor_type = self.armor_type_var.get()

        if not (cat and item and qual):
            return

        base_price = base_prices.get(item, 100)
        mat_mod = materials[mat]["price_mod"] if mat else 1.0
        qual_mod = qualities[qual]
        total_price = int(base_price * mat_mod * qual_mod * 12)  # en pièces de cuivre

        ca = 0
        bonus = ""
        effet = materials[mat]["effect"] if mat in materials else ""

        if cat == "Armures":
            ca = ca_values.get(item, 0)
            if armor_type == "Lourde":
                ca *= 2
                total_price = int(total_price * 1.5)
        
        if qual == "Chef-d'œuvre":
            if cat == "Armures":
                bonus = "+5 Soc"
            elif cat == "Armes":
                bonus = "+5 CC"
            elif cat == "Armes à distance":
                bonus = "+5 CT"

        entry = f"{item} ({cat}) - {qual}"
        if mat:
            entry += f", {mat}"
        if armor_type:
            entry += f" ({armor_type})"
        if ca:
            entry += f", CA: {ca}"
        if effet:
            entry += f", Effet: {effet}"
        if bonus:
            entry += f", Bonus: {bonus}"

        entry += f" -> {convert_price_to_text(total_price)}"
        self.items.append((entry, total_price))
        self.refresh_summary()

    def refresh_summary(self):
        self.summary_text.delete("1.0", tk.END)
        total_cp = 0
        for idx, (text, price) in enumerate(self.items):
            self.summary_text.insert(tk.END, f"[{idx}] {text}\n")
            total_cp += price
        self.total_label.config(text=f"Total: {convert_price_to_text(total_cp)}")

        # Boutons de suppression
        for widget in self.scrollable_frame.pack_slaves():
            if isinstance(widget, tk.Button) and widget.cget("text").startswith("Supprimer"):
                widget.destroy()

        for idx in range(len(self.items)):
            btn = tk.Button(self.scrollable_frame, text=f"Supprimer {idx}", command=lambda i=idx: self.remove_item(i))
            btn.pack()

    def remove_item(self, index):
        if 0 <= index < len(self.items):
            del self.items[index]
            self.refresh_summary()

root = tk.Tk()
app = RPGShopApp(root)
root.mainloop()