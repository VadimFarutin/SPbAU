import sys
import os
import hashlib


def duplicate_search(directory_name):
    hash_dict = {}

    def md5(path):
        digest = hashlib.md5()
        with open(path, "rb") as file:
            for line in file:
                digest.update(line)
        hash_dict[digest.hexdigest()] = hash_dict.get(digest.hexdigest(), [])
        hash_dict[digest.hexdigest()].append(path.replace(directory_name, "")[1:])

    def make_hashes(directory_name):
        for root, _, files in os.walk(directory_name):
            for name in files:
                if name[0] != '.' and name[0] != '~':
                    md5(os.path.join(root, name))

    def print_duplicates():
        for file_list in hash_dict.values():
            if len(file_list) > 1:
                print(":".join(file_list))

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
