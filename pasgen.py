# This code generates passwords and checks if passwords were leaked by using "have i been pwned" API
import requests
import hashlib
from random import randint, choice
import string


def request_list(request_input):
	# sends a slice of hashed password to API in order to get a list of similar hashes
	url = 'https://api.pwnedpasswords.com/range/' + request_input
	res = requests.get(url)
	if res.status_code != 200:
		raise RuntimeError(f'Error {res.status_code}\nCheck required')
	return res


def main_check(secret):
	# returns the amount of password leaks
	hashed_secret = hashlib.sha1(str(secret).encode('utf-8')).hexdigest().upper()
	api_res = request_list(hashed_secret[:5]).text
	all_hashes = (line.split(':') for line in api_res.splitlines())
	for given_hash, times in all_hashes:
		if given_hash == hashed_secret[5:]:
			return times
	return 0


def symbol_add(symbol_type):
    return choice(symbol_type)


def gen():
	# password generator
	gen_length = randint(9, 12)
	gen_pass = []
	while len(gen_pass) < gen_length:
		gen_pass.append(symbol_add(choice([string.ascii_lowercase, string.ascii_uppercase, string.digits])))
	return ''.join(gen_pass)


while __name__ == '__main__':
	# main loop
	print('For password leak check type in "C" and press "Enter" or for generating new passwords type in "G" and press "Enter"')
	task = input(': ').upper()
	
	while task == 'G':
		t = 3
		while t > 0:
			new_gen = gen()
			check = main_check(new_gen)
			print(new_gen)
			if check:
				continue
			t -= 1
		input_console = input('Press "Enter" to run again or type in "B" and press "Enter" to go back\n')
		if input_console.upper() == 'B':
			break
		else:
			continue

	while task == 'C':
		input_console = input('\nEnter the password you want to check and press "Enter" or type in "B" and press "Enter" to go back\n: ')
		if input_console.upper() == 'B':
			break
		check = main_check(input_console)
		if check:
			print(f'This password was leaked {check} time{"s" if int(check) > 1 else ""}')
		else:
			print('No leaks recorded')
