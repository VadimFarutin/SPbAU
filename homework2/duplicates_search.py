import sys
import os
import hashlib


def duplicate_search(directory_name):

    def md5(path):
        digest = hashlib.md5()
        with open(path, "rb") as file:
            while True:
                byte = file.read(1)
                if not byte:
                    break
                digest.update(byte)
        return digest.hexdigest()

    def make_hashes(directory_name):
        hash_dict = {}
        for root, _, files in os.walk(directory_name):
            for name in files:
                path = os.path.abspath(os.path.join(root, name))
                if name[0] != '.' and name[0] != '~' and not os.path.islink(path):
                    hash = md5(path)
                    hash_dict[hash] = hash_dict.get(hash, [])
                    hash_dict[hash].append(path)
        return hash_dict

    def print_duplicates(hash_dict):
        for file_list in hash_dict.values():
            if len(file_list) > 1:
                print(":".join(file_list))

    print_duplicates(make_hashes(directory_name))


def main():
    if len(sys.argv) != 2:
        print('usage: ./duplicates_search.py directory_name')
        sys.exit(1)

    directory_name = sys.argv[1]
    duplicate_search(directory_name)

if __name__ == '__main__':
    main()
