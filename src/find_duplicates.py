import os
import hashlib
import datetime
import csv
from collections import defaultdict

def file_hash(path, algo="sha256", chunk_size=8192):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()

def human_size(num_bytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num_bytes < 1024.0:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} PB"

def scan_drives(drives, extensions=None, target_name=None):
    if extensions is None:
        extensions = [".jpg"]
    extensions = [ext.lower() for ext in extensions]

    results = defaultdict(lambda: defaultdict(list))
    for drive in drives:
        for root, dirs, files in os.walk(drive):
            for fname in files:
                if target_name and fname.lower() == target_name.lower():
                    match = True
                else:
                    match = any(fname.lower().endswith(ext) for ext in extensions)

                if match:
                    full_path = os.path.join(root, fname)
                    try:
                        stat = os.stat(full_path)
                        created = datetime.datetime.fromtimestamp(stat.st_ctime)
                        modified = datetime.datetime.fromtimestamp(stat.st_mtime)
                        size = stat.st_size
                        h = file_hash(full_path)
                        results[fname][h].append({
                            "path": full_path,
                            "created": created,
                            "modified": modified,
                            "size": size
                        })
                    except Exception as e:
                        print(f"Error reading {full_path}: {e}")
    return results

def print_results(results):
    for fname, hashes in results.items():
        print(f"\n=== Filename: {fname} ===")
        for h, files in hashes.items():
            print(f"  Hash: {h}")
            print("  {:<60} {:<12} {:<20} {:<20}".format("Path", "Size", "Created", "Modified"))
            print("  " + "-"*120)
            for f in files:
                print("  {:<60} {:<12} {:<20} {:<20}".format(
                    f['path'],
                    human_size(f['size']),
                    f['created'].strftime("%Y-%m-%d %H:%M:%S"),
                    f['modified'].strftime("%Y-%m-%d %H:%M:%S")
                ))

def write_csv(results, output_file):
    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "Hash", "Path", "Size", "Created", "Modified"])
        for fname, hashes in results.items():
            for h, files in hashes.items():
                for f in files:
                    writer.writerow([
                        fname,
                        h,
                        f['path'],
                        human_size(f['size']),
                        f['created'].strftime("%Y-%m-%d %H:%M:%S"),
                        f['modified'].strftime("%Y-%m-%d %H:%M:%S")
                    ])

# Example usage:
drives = ["D:\\", "E:\\"]

# Case 1: General scan
# results = scan_drives(drives, extensions=[".jpg", ".jpeg", ".png"])
# print_results(results)
# timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# write_csv(results, f"duplicates_report_{timestamp}.csv")

# Case 2: Single filename scan
target = "img_7075.png"
results_specific = scan_drives(drives, target_name=target)
print_results(results_specific)
base, _ = os.path.splitext(target)
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_name = f"{base}_report_{timestamp}.csv"
write_csv(results_specific, csv_name)

