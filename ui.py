import tkinter as tk
from tkinter import messagebox, ttk
from main import predict_price


def run_ui():
    """
    Creates and render UI
    """
    root = tk.Tk()
    root.title("RAM Price Predictor")
    root.geometry("650x700")

    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(main_frame, text="RAM Price Predictor", font=("Arial", 16, "bold")).pack(pady=10)

    brands = [
        "ADATA", "A-Tech", "Acclamator", "Adamanta", "Ballistix", "Corsair",
        "Crucial", "Dell", "G.SKILL", "GIGASTONE", "HP", "Kingston", "Lenovo",
        "Micron", "NEMIX", "OWC", "PNY", "Patriot", "Patriot Memory", "PUSKILL",
        "QNAP", "SK Hynix", "Samsung", "TEAMGROUP", "Timetec", "XPG", "Other", "Unknown"
    ]

    def on_submit():
        try:
            c = float(entry_cap.get())
            s = float(entry_speed.get())

            g = int(combo_gen.get()) if combo_gen.get() else None
            b = combo_brand.get() if combo_brand.get() else "Unknown"
            l = float(entry_lat.get()) if entry_lat.get().strip() else None
            v = float(entry_volt.get()) if entry_volt.get().strip() else None

            k = var_kit.get()
            f = var_server.get()

            results = predict_price(c, g, s, l, v, b, k, f)

            text_result.config(state=tk.NORMAL)
            text_result.delete(1.0, tk.END)
            if results:
                for res in results:
                    text_result.insert(tk.END, res + "\n")
            text_result.config(state=tk.DISABLED)

        except ValueError:
            messagebox.showerror("Input Error", "Capacity & Frequency are REQUIRED and must be numbers")
        except Exception as e:
            messagebox.showerror("Unknown Error", str(e))

    #Entry pole
    fields = [
        ("*Capacity (GB):", "entry_cap"),
        ("*Frequency (MHz):", "entry_speed"),
        ("Latency (CL) - optional:", "entry_lat"),
        ("Voltage (V) - optional:", "entry_volt"),
    ]

    entries = {}
    for label_text, var_name in fields:
        frame = ttk.Frame(main_frame)
        frame.pack(fill=tk.X, pady=5)
        ttk.Label(frame, text=label_text, width=25).pack(side=tk.LEFT)
        entry = ttk.Entry(frame)
        entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        entries[var_name] = entry

    #Brand
    brand_frame = ttk.Frame(main_frame)
    brand_frame.pack(fill=tk.X, pady=5)
    ttk.Label(brand_frame, text="Brand:", width=25).pack(side=tk.LEFT)
    combo_brand = ttk.Combobox(brand_frame, values=brands)
    combo_brand.set("Unknown")  # Výchozí hodnota
    combo_brand.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    #Gen
    gen_frame = ttk.Frame(main_frame)
    gen_frame.pack(fill=tk.X, pady=5)
    ttk.Label(gen_frame, text="Generation DDR:", width=25).pack(side=tk.LEFT)
    combo_gen = ttk.Combobox(gen_frame, values=["3", "4", "5"])
    combo_gen.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    #Checkboxy
    check_frame = ttk.Frame(main_frame)
    check_frame.pack(pady=10)

    var_kit = tk.BooleanVar(value=True)
    ttk.Checkbutton(check_frame, text="Jedná se o Kit (sadu)?", variable=var_kit).pack(side=tk.LEFT, padx=10)

    var_server = tk.BooleanVar(value=False)
    ttk.Checkbutton(check_frame, text="Server RAM (ECC)?", variable=var_server).pack(side=tk.LEFT, padx=10)

    #Přiřazení proměnných
    entry_cap = entries["entry_cap"]
    entry_speed = entries["entry_speed"]
    entry_lat = entries["entry_lat"]
    entry_volt = entries["entry_volt"]

    btn_predict = ttk.Button(main_frame, text="PREDICT PRICE", command=on_submit)
    btn_predict.pack(pady=20, fill=tk.X)

    ttk.Label(main_frame, text="Results:").pack(anchor=tk.W)
    text_result = tk.Text(main_frame, height=8, state=tk.DISABLED, bg="#f0f0f0")
    text_result.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


if __name__ == "__main__":
    run_ui()