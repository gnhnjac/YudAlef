from sys import argv
import hashlib


def hash_pass(p):
    """ returns hashed 256 string """
    m = hashlib.sha256()
    m.update(p.encode())  # in python3 m.update(p.encode())
    return m.hexdigest()


def main():
    pass_db_old = {}
    try:
        # Read original names and passwords to dict
        with open(argv[1], 'r') as f1:

            for line in f1:
                name_pass = line.rstrip().split(':')

                pass_db_old[name_pass[0]] = name_pass[1]
        # Write names and hashed passwords to new file
        with open(argv[2], 'w') as f2:
            for name in pass_db_old:
                f2.write(f"{name}:{hash_pass(pass_db_old[name])}\n")
        pass_db = {}
        # Read names and hashed passwords from new file
        with open(argv[2], 'r') as f2:
            for line in f2:
                name_pass = line.rstrip().split(':')
                pass_db[name_pass[0]] = name_pass[1]

        # Request name and password
        name = input("Please enter name: ")
        passwd = input("Please enter password: ")

        # Check if name and password are valid
        success = False
        for item in pass_db:

            if pass_db[item] == hash_pass(passwd) and item == name:
                success = True

        print("Login success" if success else "Login failed")

    except Exception as e:
        print("Could not open file:", e)


if __name__ == '__main__':
    main()
