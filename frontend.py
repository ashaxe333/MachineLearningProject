import main

def main_ui():
    print("=" * 30)
    print(" RAM PRICE PREDICTOR v2.0 ")
    print("=" * 30)

    try:
        # Vstupy s defaultními hodnotami
        cap = float(input("Kapacita v GB (povinné): "))
        speed = float(input("Frekvence v MHz (povinné): "))

        gen_in = input("Generace DDR (3/4/5) [Enter pro auto]: ")
        gen = int(gen_in) if gen_in else None

        brand = input("Značka (např. Corsair) [Enter pro neznámou]: ") or "-"

        lat_in = input("Latence CL [Enter pro odhad]: ")
        lat = int(lat_in) if lat_in else None

        volt_in = input("Napětí ve V [Enter pro odhad]: ")
        volt = float(volt_in) if volt_in else None

        # Volání tvé našlapané funkce
        results = main.predict_price(cap, gen, speed, lat, volt, brand, 1)

        print("\n" + "*" * 20)
        print(" VÝSLEDKY PŘEDPOVĚDI ")
        print("*" * 20)

        for r in results:
            print(r)

    except Exception as e:
        print(f"\n CHYBA: {e}")

    print("\n Děkujeme za použití prediktoru!")


if __name__ == "__main__":
    main_ui()