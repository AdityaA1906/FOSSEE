import os

files = ["out_jacobi.txt", "out_seidel.txt", "out_elimination.txt"]
base_dir = r"d:\projects last sem"

for f_name in files:
    path = os.path.join(base_dir, f_name)
    print(f"\n{'#'*40}")
    print(f"OUTPUT: {f_name}")
    print(f"{'#'*40}")
    try:
        # PowerShell > redirection creates UTF-16 LE files
        with open(path, 'r', encoding='utf-16') as f:
            content = f.read()
            print(content)
    except Exception as e:
        print(f"Error reading with utf-16: {e}")
        try:
             with open(path, 'r', encoding='utf-8', errors='replace') as f:
                print(f.read())
        except Exception as e2:
            print(f"Error reading with utf-8: {e2}")
