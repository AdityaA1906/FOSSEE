import os

files = ["1_out.txt", "2_out.txt", "3_out.txt", "4_out.txt", "5_out.txt", "6_out.txt"]
output_file = "all_outputs.txt"

with open(output_file, 'w', encoding='utf-8') as outfile:
    for f in files:
        outfile.write(f"\n{'='*20} Output of {f} {'='*20}\n")
        if os.path.exists(f):
            try:
                # PowerShell > redirection often produces UTF-16LE
                with open(f, 'r', encoding='utf-16') as infile:
                    outfile.write(infile.read())
            except Exception as e:
                try:
                    # Fallback to default/utf-8
                    with open(f, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                except Exception as e2:
                    outfile.write(f"Error reading {f}: {e2}\n")
        else:
            outfile.write(f"File {f} not found.\n")
    outfile.write("\n" + "="*50 + "\n")

print(f"Consolidated outputs to {output_file}")
