import os
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk


class BoutiqueApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Boutique en Ligne - Python & Images")
    self.root.geometry("600x750")
    self.root.config(bg="#f8fafc")

    # Title Banner
    title_label = tk.Label(
        root,
        text="Boutique en Ligne (Application Python)",
        font=("Arial", 15, "bold"),
        bg="#4f46e5",
        fg="white",
        pady=12,
    )
    title_label.pack(fill=tk.X)

    # Produits data w esmi el tswir fel dossier images
    self.products = {
        "Chaussures (120 DT)": {"price": 120, "file": "chaussures.jpg"},
        "Manteau (180 DT)": {"price": 180, "file": "manteau.jpg"},
        "Pantalon (75 DT)": {"price": 75, "file": "pantalon.jpg"},
        "Lunettes (50 DT)": {"price": 50, "file": "lunettes.jpg"},
        "T-Shirt (35 DT)": {"price": 35, "file": "tshirt.jpg"},
        "Maquillage (60 DT)": {"price": 60, "file": "maquillage.jpg"},
    }

    # Inputs Frame
    frame = tk.Frame(root, bg="#f8fafc", pady=10)
    frame.pack()

    # Client Name
    tk.Label(
        frame,
        text="Nom et Prénom:",
        font=("Arial", 11, "bold"),
        bg="#f8fafc",
        fg="#1e293b",
    ).grid(row=0, column=1, sticky="e", padx=5, pady=5)
    self.name_entry = tk.Entry(frame, font=("Arial", 11), width=22)
    self.name_entry.grid(row=0, column=0, padx=5, pady=5)

    # Product Selection Combobox
    tk.Label(
        frame,
        text="Sélectionner Article:",
        font=("Arial", 11, "bold"),
        bg="#f8fafc",
        fg="#1e293b",
    ).grid(row=1, column=1, sticky="e", padx=5, pady=5)

    self.prod_combo = ttk.Combobox(
        frame,
        values=list(self.products.keys()),
        width=20,
        state="readonly",
        font=("Arial", 10),
    )
    self.prod_combo.grid(row=1, column=0, padx=5, pady=5)
    self.prod_combo.current(0)
    self.prod_combo.bind("<<ComboboxSelected>>", self.update_image)

    # Quantity
    tk.Label(
        frame,
        text="Quantité:",
        font=("Arial", 11, "bold"),
        bg="#f8fafc",
        fg="#1e293b",
    ).grid(row=2, column=1, sticky="e", padx=5, pady=5)
    self.qty_entry = tk.Entry(frame, font=("Arial", 11), width=22)
    self.qty_entry.insert(0, "1")
    self.qty_entry.grid(row=2, column=0, padx=5, pady=5)

    # Image Display Frame
    self.img_label = tk.Label(root, bg="#f8fafc", bd=2, relief="groove")
    self.img_label.pack(pady=8)
    self.load_product_image(list(self.products.keys())[0])

    # Add to Cart Button
    order_btn = tk.Button(
        root,
        text="Ajouter au Panier",
        font=("Arial", 11, "bold"),
        bg="#10b981",
        fg="white",
        padx=20,
        pady=6,
        command=self.add_order,
    )
    order_btn.pack(pady=5)

    # Treeview Table
    self.tree = ttk.Treeview(
        root,
        columns=("Client", "Product", "Qty", "Total"),
        show="headings",
        height=6,
    )
    self.tree.heading("Client", text="Client")
    self.tree.heading("Product", text="Article")
    self.tree.heading("Qty", text="Quantité")
    self.tree.heading("Total", text="Total")

    self.tree.column("Client", width=120, anchor="center")
    self.tree.column("Product", width=190, anchor="center")
    self.tree.column("Qty", width=60, anchor="center")
    self.tree.column("Total", width=90, anchor="center")

    self.tree.pack(pady=10)

  def load_product_image(self, product_key):
    filename = self.products[product_key]["file"]
    img_path = os.path.join("images", filename)

    try:
      if os.path.exists(img_path):
        img = Image.open(img_path)
        img = img.resize((130, 130))
        self.current_img = ImageTk.PhotoImage(img)
        self.img_label.config(image=self.current_img, text="")
      else:
        self.img_label.config(
            image="",
            text=f"Tswira '{filename}' mch mawjouda fel dossier 'images'",
            font=("Arial", 9),
            fg="red",
        )
    except Exception:
      self.img_label.config(image="", text="Erreur de chargement d'image")

  def update_image(self, event):
    selected = self.prod_combo.get()
    self.load_product_image(selected)

  def add_order(self):
    client = self.name_entry.get().strip()
    selected_prod = self.prod_combo.get()
    qty_str = self.qty_entry.get().strip()

    if not client or not qty_str:
      messagebox.showerror(
          "Erreur", "Veuillez remplir le nom et la quantité !"
      )
      return

    try:
      qty = int(qty_str)
      if qty <= 0:
        raise ValueError()
    except ValueError:
      messagebox.showerror("Erreur", "La quantité doit être un nombre valide !")
      return

    unit_price = self.products[selected_prod]["price"]
    total_price = unit_price * qty

    self.tree.insert(
        "", tk.END, values=(client, selected_prod, qty, f"{total_price} DT")
    )

    self.name_entry.delete(0, tk.END)
    self.qty_entry.delete(0, tk.END)
    self.qty_entry.insert(0, "1")

    messagebox.showinfo(
        "Succès",
        f"Commande de {client} enregistrée pour un total de {total_price} DT !",
    )


if __name__ == "__main__":
  root = tk.Tk()
  app = BoutiqueApp(root)
  root.mainloop()