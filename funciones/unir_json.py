import json
import argparse

def merge_json_files(input_files, output_file):
    merged_data = {}
    duplicate_keys = {}

    for file_path in input_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    print(f"El archivo {file_path} no contiene un JSON tipo diccionario.")
                    continue

                for key in data:
                    if key in merged_data:
                        if key not in duplicate_keys:
                            duplicate_keys[key] = []
                        duplicate_keys[key].append(file_path)
                    merged_data[key] = data[key]

        except Exception as e:
            print(f"Error procesando {file_path}: {e}")

    # Guardar el archivo final
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)

    print(f"\nArchivos unidos correctamente en: {output_file}")

    if duplicate_keys:
        print("\nClaves duplicadas encontradas (se sobrescribió la anterior):")
        for key, files in duplicate_keys.items():
            print(f"  - '{key}' apareció también en: {', '.join(files)}")
    else:
        print("No se encontraron claves duplicadas.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unir archivos JSON específicos y reportar claves duplicadas")
    parser.add_argument("input_files", nargs="+", help="Lista de archivos JSON (pueden ser rutas completas)")
    parser.add_argument("-o", "--output", required=True, help="Ruta del archivo JSON de salida")
    args = parser.parse_args()

    merge_json_files(args.input_files, args.output)