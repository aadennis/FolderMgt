import csv
from collections import defaultdict

def load_index(index_file="image_index.csv"):
    results = defaultdict(lambda: defaultdict(list))
    with open(index_file, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            fname = row["Filename"]
            h = row["Hash"]
            results[fname][h].append({
                "path": row["Path"],
                "size": row["Size"],
                "created": row["Created"],
                "modified": row["Modified"]
            })
    return results

def print_results(results, target_name=None):
    for fname, hashes in results.items():
        if target_name and fname.lower() != target_name.lower():
            continue
        print(f"\n=== Filename: {fname} ===")
        for h, files in hashes.items():
            print(f"  Hash: {h}")
            print("  {:<60} {:<12} {:<20} {:<20}".format("Path","Size","Created","Modified"))
            print("  " + "-"*120)
            for f in files:
                print("  {:<60} {:<12} {:<20} {:<20}".format(
                    f['path'], f['size'], f['created'], f['modified']
                ))

if __name__ == "__main__":
    results = load_index("../image_index2.csv")
    # Example: query one file
    print_results(results, target_name="img_0026.jpg")

    