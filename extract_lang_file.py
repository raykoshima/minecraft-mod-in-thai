import os
import zipfile
import argparse

def extract_lang_files(folder: str, skip_th: bool):
    if not os.path.isdir(folder):
        print("❌ Invalid folder path. Exiting...")
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "assets")
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(folder):
        if filename.endswith(".jar"):
            jar_path = os.path.join(folder, filename)
            print(f"🔍 Checking {jar_path}...")

            with zipfile.ZipFile(jar_path, 'r') as jar:
                for file in jar.namelist():
                    if file.startswith("assets/") and "/lang/en_us.json" in file:
                        folder_name = file.split('/')[1]
                        subfolder_path = os.path.join(output_dir, folder_name, "lang")
                        os.makedirs(subfolder_path, exist_ok=True)

                        output_path = os.path.join(subfolder_path, "en_us.json")
                        if os.path.exists(output_path):
                            print(f"⏭️ Skipped {output_path} (already exists)")
                            break

                        with jar.open(file) as source, open(output_path, "wb") as target:
                            target.write(source.read())
                        
                        print(f"✅ Extracted {file} -> {output_path}")
                        break
                else:
                    print("⚠️ No en_us.json found in this JAR.")

                if not skip_th:
                    for file in jar.namelist():
                        if file.startswith("assets/") and "/lang/th_th.json" in file:
                            folder_name = file.split('/')[1]
                            subfolder_path = os.path.join(output_dir, folder_name, "lang")
                            os.makedirs(subfolder_path, exist_ok=True)

                            output_path = os.path.join(subfolder_path, "th_th.json")
                            if os.path.exists(output_path):
                                print(f"⏭️ Skipped {output_path} (already exists)")
                                break

                            with jar.open(file) as source, open(output_path, "wb") as target:
                                target.write(source.read())
                            
                            print(f"✅ Extracted {file} -> {output_path}")
                            break
                    else:
                        print("⚠️ No th_th.json found in this JAR.")

    print("🎉 Extraction complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract en_us.json (and optionally th_th.json) from JAR files.")
    parser.add_argument("folder", help="Full folder path containing .jar files")
    parser.add_argument("--no-th", action="store_true", help="Skip extracting th_th.json")
    args = parser.parse_args()

    extract_lang_files(args.folder, args.no_th)
