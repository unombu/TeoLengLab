import os
from AFND_e import AFND_e
from AFND_eBuilder import cargar_afnd_desde_json, afnde_to_json
from regex_to_afnde import regex_to_afnde
from is_entry_valid import is_entry_valid

if __name__ == "__main__":
    archivos = sorted(os.listdir("entradas"), key=lambda x: int(x.split('.')[0]))
    total = len(archivos)
    aprobados = 0

    for archivo in archivos:
        i = archivo.split('.')[0]
        with open(os.path.join("entradas", archivo)) as f:
            expr = f.read().strip()

        print(f"\n===============================")
        print(f"Test {i}: expresión = {expr}")

        entrada_valida = is_entry_valid(expr)

        salida_esperada_path = f"salidas_esperadas/{i}.json"
        salida_generada_path = f"salidas/{i}.json"

        try:
            with open(salida_esperada_path, 'r', encoding='utf-8') as expected_file:
                contenido = expected_file.read().strip()
                if contenido == "Entrada no valida":
                    salida_esperada_valida = False
                else:
                    salida_esperada_valida = True
        except FileNotFoundError:
            print("❌ No se encontró la salida esperada.")
            continue

        if not entrada_valida:
            print("🔎 Entrada determinada como NO válida")

            with open(salida_generada_path, 'w', encoding='utf-8') as f:
                f.write("Entrada no valida")

            if not salida_esperada_valida:
                print("✅ Resultado: OK (coincide con la salida esperada: entrada no válida)")
                aprobados += 1
            else:
                print("❌ ERROR: la entrada fue rechazada pero se esperaba un AFND válido")
        else:
            print("🔎 Entrada determinada como VÁLIDA")

            if not salida_esperada_valida:
                print("❌ ERROR: la entrada fue aceptada pero se esperaba 'Entrada no válida'")
            else:
                generado = regex_to_afnde(expr)
                afnde_to_json(generado, salida_generada_path)
                esperado = cargar_afnd_desde_json(salida_esperada_path)
                ok = AFND_e.son_isomorfos(generado, esperado)
                if generado is not None:
                    print("\nAFND generado:")
                    generado.mostrar()
                else:
                    print("\nEl AFND no fue generado")
                print("\nResultado:", "✅ OK" if ok else "❌ ERROR")
                if ok:
                    aprobados += 1

    print("\n===============================" )
    print(f"Resumen: {aprobados} / {total} tests pasados")
