import sys
import hashlib


def hash_passwd(passwd):
	"""return hashed 256 string"""
	m = hashlib.sha256()
	m.update(passwd.encode())
	return m.hexdigest()


# checks if the input name resolves in the same password hashcode
def login(passwd_dict):
	name = input("Please enter name:")
	passwd = input("Please enter password:")
	if passwd_dict[name] == hash_passwd(passwd):
		print("Login success")
	else:
		print("Login failed")


def main():
	# check the amount of args
	if len(sys.argv) < 2:
		print("Not enough arguments!")
		sys.exit()

	try:
		# Read original names and passwords into a dict
		with open(sys.argv[1], 'r') as org_file:
			separate_dict = {}
			for line in org_file:
				separate_lst = line.split(":")
				if len(separate_lst) > 1:
					separate_dict[separate_lst[0].strip()] = separate_lst[1].strip()
		# write to the second file the names and their hashed passwords
		with open(sys.argv[2], "w") as hash_file:
			for name in separate_dict:
				hash_file.write(f"{name}:{hash_passwd(separate_dict[name])}\n")
		# make a dictionary out of the written names and passwords from the second file
		hash_passwd_dict = {}
		with open(sys.argv[2], "r") as hash_file:
			for line in hash_file:
				separate_file2 = line.split(":")
				if len(separate_file2) > 1:
					hash_passwd_dict[separate_file2[0].strip()] = separate_file2[1].strip()
		login(hash_passwd_dict)
	except Exception as e:
		print("An error has accrued while opening file ", e)


if __name__ == '__main__':
	main()
