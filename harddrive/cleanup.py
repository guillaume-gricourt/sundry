import argparse
import os
import hashlib
import shutil
import sys
from collections import defaultdict


def hash_file(file_path, block_size=65536):
    """Generate the MD5 hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(block_size):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_directory_hash(directory_path):
    """Return a hash representing the contents of a directory."""
    file_hashes = []
    try:
        for root, _, files in os.walk(directory_path):
            for file_name in sorted(files):  # Sorting to ensure consistent hash
                file_path = os.path.join(root, file_name)
                file_hash = hash_file(file_path)
                if file_hash:
                    file_hashes.append((file_name, file_hash))
        file_hashes.sort()  # Sorting to ensure consistent hash across different runs
    except Exception as e:
        print(f"Error processing directory {directory_path}: {e}")
        return None

    directory_hash = hashlib.sha256()
    for file_name, file_hash in file_hashes:
        directory_hash.update(f"{file_name}:{file_hash}".encode())

    return directory_hash.hexdigest()


#############################################################################################
def remove_duplicate_files(root_folder):
    """Find and group duplicate files based on file hash."""
    file_hashes = defaultdict(list)
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                file_hash = hash_file(file_path)
                file_hashes[file_hash].append(file_path)
            except Exception as e:
                print(f"Error hashing file {file_path}: {e}")

    for file_list in file_hashes.values():
        if len(file_list) > 1:
            # Keep the first file and delete the rest
            for file_path in file_list[1:]:
                print(f"Remove duplicated file {file_path}")
                os.remove(file_path)


def delete_specific_directories(root_dir, targets):
    """Recursively search for directories with duplicate contents."""
    directories = []
    # Recursively walk through the root directory
    for dirpath, dirnames, _ in os.walk(root_dir):
        for dirname in dirnames:
            if dirname in targets:
                dir_full_path = os.path.join(dirpath, dirname)
                directories.append(dir_full_path)
    # Find and print duplicates
    if len(directories) > 0:
        print("Duplicate directories found:")
        for directory in directories:
            print(f"Dir to remove: {directory}")
            shutil.rmtree(directory)


def delete_empty_folders(root_folder, to_ignore):
    """Delete empty folders recursively."""
    to_removes = []
    for dirpath, dirnames, _ in os.walk(root_folder, topdown=False):
        if not dirnames and not os.listdir(dirpath):  # Empty folder
            is_ignored = False
            for chunk in dirpath.split(os.sep):
                if chunk in to_ignore:
                    is_ignored = True
                    break
            if is_ignored is False:
                to_removes.append(dirpath)

    for empty_dir in to_removes:
        print(f"Empty dir: {empty_dir}")
        os.rmdir(empty_dir)


def find_duplicate_directories(root_dir, to_ignore):
    """Recursively search for directories with duplicate contents."""
    directory_hashes = defaultdict(list)

    # Recursively walk through the root directory
    for dirpath, dirnames, _ in os.walk(root_dir):
        for dirname in dirnames:
            dir_full_path = os.path.join(dirpath, dirname)
            is_ignored = False
            for chunk in dir_full_path.split(os.sep):
                if chunk in to_ignore:
                    is_ignored = True
                    break
            if is_ignored is False:
                dir_hash = get_directory_hash(dir_full_path)
                if dir_hash:
                    directory_hashes[dir_hash].append(dir_full_path)

    # Find and print duplicates
    duplicates = {k: v for k, v in directory_hashes.items() if len(v) > 1}
    if duplicates:
        print("Duplicate directories found:")
        for hash_key, paths in duplicates.items():
            print(f"\nHash: {hash_key}")
            for path in paths:
                print(f" - {path}")
    else:
        print("No duplicate directories found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-dir", required=True, help="Directory to scan")
    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        print("Directory is not exists")
        sys.exit()

    root_dir = args.input_dir

    print(f"Start cleanup of: {root_dir}")

    ## Clean up directories
    print("\t", "Clean up directories", "-", "start")
    directories_to_remove = [".snakemake", "__pycache__", ".ipynb_checkpoints"]
    delete_specific_directories(root_dir, directories_to_remove)
    print("\t", "Clean up directories", "-", "end")

    ## Delete empty folders
    print("\t", "Remove empty folder", "-", "start")
    directories_to_ignore = [".git"]
    delete_empty_folders(root_dir, directories_to_ignore)
    print("\t", "Remove empty folder", "-", "end")

    ## Duplicate directories
    # print("\t", "Find duplicate dir", "-", "start")
    # directories_to_ignore = [".git"]
    # find_duplicate_directories(root_dir, directories_to_ignore)
    # print("\t", "Find duplicate dir", "-", "end")

    ## Find duplicate files
    # print("\t", "Find duplicate files", "-", "start")
    # remove_duplicate_files(root_dir)
    # print("\t", "Find duplicate files", "-", "end")

    print(f"End cleanup of: {root_dir}")
