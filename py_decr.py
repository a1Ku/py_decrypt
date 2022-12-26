import zlib
import sys
import re
import os
import shutil
import gnupg


old_path = "/home/alku/cripta/22_dfc697a5/"
files_path = "/home/alku/cripta/BBSO_01_19/files/"
etc_path = "/home/alku/cripta/BBSO_01_19/etc/"

gpg = gnupg.GPG()


def init_dir():
	print("---Create dirr---")
	os.mkdir(files_path)
	os.mkdir(etc_path)


def init_files():
	print("---Init files---")
	for root, dirs, files in os.walk(old_path):
		for fname in files:
			if re.search(r"\bfile", fname):
				shutil.copyfile(old_path + fname, files_path + fname)
			else:
				shutil.copyfile(old_path + fname, etc_path + fname)


def crc_check():
	print("---Check crc32---")
	for root, dirs, files in os.walk(files_path):
		for fname in files:
			with open(files_path + fname, "rb") as fp:
				file = fp.read()
				crc32 = hex(zlib.crc32(file) & 0xffffffff)[2:]
				while len(crc32) < 8:
					crc32 = "0" + crc32
				if fname[-13:][:-5] != crc32:
					os.remove(files_path + fname)


def decrypt_files():
	print("---Check passphrase---")
	for root, dirs, files in os.walk(files_path):
		for fname in files:
			with open(files_path + fname, "rb") as fp:
				file = fp.read()
				ps_phrase = file[-1*int(fname[0]):].hex()
				os.truncate(files_path + fname, len(file) - int(fname[0]))
			new_file = gpg.decrypt(file, passphrase=ps_phrase)
			os.remove(files_path + fname)
			if re.search(r"SALT", str(new_file)):
				with open(files_path + fname, "w") as fp:
					fp.write(str(new_file))


def sign_check():
	print("---Check sign---")
	for root, dirs, files in os.walk(files_path):
		for fname in files:
			with open(files_path + fname, "rb") as fp:
				file = fp.read()
			pt = str(file).split("#")[1]
			pt = str(pt).split()[0]
			with open(etc_path + "chunk_" + pt + ".sig", "rb") as fp:
				ver = gpg.verify_file(fp, files_path + fname)
			if re.search(r"bad", str(ver.status)):
				os.remove(files_path + fname)


def create_key():
	print("---Create key---")
	chunk_1, chunk_2, chunk_3, chunk_4, chunk_5 = "", "", "", "", ""
	for root, dirs, files in os.walk(files_path):
		for fname in files:
			with open(files_path + fname, "rb") as fp:
				file = fp.read()
			pt = str(file).split("#")[1]
			pt = str(pt).split()[0]
			chunk = str(file).split("->")[2]
			chunk = str(chunk).split()[0]
			if pt == "1": chunk_1 = chunk
			if pt == "2": chunk_2 = chunk
			if pt == "3": chunk_3 = chunk
			if pt == "4": chunk_4 = chunk
		key = chunk_1 + chunk_2 + chunk_3 + chunk_4
		print("KEY: " + key)
		with open(etc_path + "target.txt.gpg", "rb") as fp:
			n_file = fp.read()
			os.system("echo " + key + " | gpg -d --batch --yes --passphrase-fd 0 " + etc_path + "target.txt.gpg")


if __name__ == "__main__":
	init_dir()
	init_files()
	crc_check()
	decrypt_files()
	sign_check()
	create_key()
