import tkinter as tk
from tkinter import ttk

# Données de base
categories = {
    "Armes": {"items": ["Baton de combat", "Hallebarde", "Pique", "Sarisse", "Cestes", "Couteau", "Dague", "Epée", "Lance", "Marteau bec-de-corbin", "Epée batarde", "Grande hache", "Masse d'arme", "Marteau de guerre", "Pioche", "Espadon", "Fleuret", "Rapière", "Fléau", "Fléau à grain", "Fléau d'armes", "Brise-épée"], "has_material": True, "has_quality": True},
    "Armes à distance": {"items": ["Arc", "Arc court", "Arc long", "Arc elfique", "Arbalète de poing", "Arbalète", "Arbalète lourde", "Pistolet", "Pistolet à répétition", "Arquebuse", "Arquebuse à répétition", "Long fusil"], "has_material": True, "has_quality": True},
    "Armures": {"items": ["Casque", "Plastron", "Jambières", "Gants", "Bouclier", "Grand bouclier", "Bouclier bocle"], "has_material": True, "has_quality": True, "has_type": True},
    "Bijoux": {"items": ["Anneau", "Amulette", "Bracelet"], "has_material": True, "has_quality": True},
    "Potions": {"items": ["Potion de soin", "Poison mineur"], "has_material": False, "has_quality": True},
    "Animaux": {"items": ["Boeuf", "Chat", "Cheval d'attelage", "Chevale de guerre léger", "Cheval de selle", "Chèvre", "Chien de chasse", "Chien de guerre", "Chien domestique", "Chien ratier", "Cochon", "Cochon de lait", "Destrier", "Faucon"], "has_material": False, "has_quality": False},
    "Outils": {"items": ["Marteau de forgeron", "Pelle", "Pioche"], "has_material": True, "has_quality": True}
}

materials = {
    "Bronz ou Chêne": {"price_mod": 0.2, "C_armor_mod": 0.2, "effect": ""},
    "Fer ou Hêtre": {"price_mod": 0.4, "C_armor_mod": 0.4, "effect": ""},
    "Acier ou Frêne": {"price_mod": 1.0, "C_armor_mod": 1.0, "effect": ""},
    "Platine ou Hérable": {"price_mod": 2.0, "C_armor_mod": 1.2, "effect": ""},
    "Argent ou Saule Blanc": {"price_mod": 3.0, "C_armor_mod": 1.5, "effect": "Magique & Intangible"},
    "Mythril ou Bois de Lune": {"price_mod": 6.0, "C_armor_mod": 2.0, "effect": "Magique & Intangible"},
    "Verre ou Bois de Vitréalis": {"price_mod": 10.0, "C_armor_mod": 2.4, "effect": "Magique & Intangible"},
    "Obsidienne ou Bois d'Ebène": {"price_mod": 15.0, "C_armor_mod": 3.0, "effect": "Magique & Intangible"},
    "Ebonite ou Bois de Corbeau": {"price_mod": 20.0, "C_armor_mod": 3.7, "effect": "Magique & Intangible"},
    "Infernal ou Bois du Styx": {"price_mod": 50.0, "C_armor_mod": 4.5, "effect": "Magique & Intangible"},
    "Auréalis ou Bois Céleste": {"price_mod": 100.0, "C_armor_mod": 5.0, "effect": "Magique & Intangible"}
}

qualities = {
    "Médiocre": 0.25,
    "Correcte": 0.5,
    "Assez bonne": 1,
    "Bonne": 1.25,
    "Magnifique": 1.5,
    "Chef d'œuvre": 2.0
}

quality_price_multipliers = {
    "Médiocre": 0.25,
    "Correcte": 0.5,
    "Assez bonne": 1,
    "Bonne": 10,
    "Magnifique": 25,
    "Chef d'œuvre": 1000
}

base_prices = {
    "Baton de combat": 3, "Hallebarde": 40, "Pique": 15, "Sarisse": 18, "Cestes": 3, "Couteau": 8, "Dague": 16, "Epée": 20, "Lance": 20, "Marteau bec-de-corbin": 60, "Epée batarde": 160, "Grande hache": 80, "Masse d'arme": 20, "Marteau de guerre": 60, "Pioche": 9, "Espadon": 200, "Fleuret": 20, "Rapière": 40, "Fléau": 40, "Fléau à grain": 10, "Fléau d'armes": 60, "Brise-épée": 22,
    "Arc": 80, "Arc court": 60, "Arc long": 100, "Arc elfique": 200, "Arbalète de poing": 100, "Arbalète": 120, "Arbalète lourde": 140, "Pistolet": 160, "Pistolet à répétition": 3000, "Arquebuse": 80, "Arquebuse à répétition": 2000, "Long fusil": 10000,
    "Casque": 100, "Plastron": 300, "Jambières": 200, "Gants": 160, "Bouclier": 40, "Grand bouclier": 60, "Bouclier bocle": 12,
    "Anneau": 100, "Amulette": 160, "Bracelet": 140,
    "Potion de soin": 5, "Poison mineur": 3,
    "Boeuf": 1400, "Chat": 80, "Cheval d'attelage": 1200, "Cheval de guerre léger": 17200, "Cheval de selle": 5400,"Chèvre": 60, "Chien de chasse": 80, "Chien de guerre": 400, "Chien domestique": 60, "Chien ratier": 80, "Cochon": 140, "Cochon de lait": 80, "Destrier": 57100, "Faucon": 1100,
    "Marteau de forgeron": 80, "Pelle": 40, "Pioche": 60
}

ca_values = {"Casque": 20, "Plastron": 30, "Jambières": 20, "Gants": 20, "Bouclier": 20, "Grand bouclier": 30, "Bouclier bocle": 10}

def convert_price_to_text(total_cp):
    po = total_cp // 240
    reste = total_cp % 240
    pa = reste // 12
    pc = reste % 12
    return f"{po} PO, {pa} PA, {pc} PC"

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
        mat_CA_mod = materials[mat]["C_armor_mod"] if mat else 1.0
        qual_mod = quality_price_multipliers[qual]
        total_price = int(base_price * mat_mod * qual_mod * 12)

        ca = 0
        bonus = ""
        effet = materials[mat]["effect"] if mat in materials else ""

        if cat == "Armures":
            ca_base = ca_values.get(item, 0)
            ca = ca_base * mat_CA_mod * qualities[qual]
            if armor_type == "Lourde":
                ca *= 1.5
                total_price = int(total_price * 1.5)
            ca = int(ca)

        if qual == "Chef d'œuvre":
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