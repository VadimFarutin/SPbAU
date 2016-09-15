import sys
import os
import hashlib


def duplicate_search(directory_name):
    hash_dict = {}

    def make_hashes(directory_name):
        for entry in os.scandir(directory_name):
            if entry.is_dir():
                make_hashes(entry.path)
            elif entry.name[0] != '.' and entry.name[0] != '~':
                file = open(entry.path, "rb")
                digest = hashlib.md5()
                digest.update(file.read())
                hash_dict[digest.hexdigest()] = hash_dict.get(digest.hexdigest(), []) + [entry.path]
                file.close()

    def print_duplicates():
        for file_list in hash_dict.values():
            if len(file_list) > 1:
                duplicates = ""
                for file in file_list:
                    duplicates += file.replace(directory_name, "")[1:] + ":"
                print(duplicates[:-1] + "\n")

    make_hashes(directory_name)
    print_duplicates()


def main():
    if len(sys.argv) != 2:
        print('usage: ./duplicates_search.py directory_name')
        sys.exit(1)

    directory_name = sys.argv[1]
    duplicate_search(directory_name)

if __name__ == '__main__':
    main()
