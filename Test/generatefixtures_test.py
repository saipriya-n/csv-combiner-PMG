import os
import random as r
import csv
import hashlib
import os.path as ospath

DIR = path.abspath(path.dirname(__file__))
FILES = {
	'clothing.csv': ('Blouses', 'Shirts', 'Tanks', 'Cardigans', 'Pants', 'Capris', '"Gingham" Shorts',),
	'accessories.csv': ('Watches', 'Wallets', 'Purses', 'Satchels',),
	'household_cleaners.csv': ('Kitchen Cleaner', 'Bathroom Cleaner',),
}
	
	
def write_file(writer, length_of_file, categories_of_file):
	writer.writerow(['email_hash', 'category'])
	for i in range(length_of_file):
		writer.writerow([
			hashlib.sha256('tech+test{}@pmg.com'.format(i).encode('utf-8')).hexdigest(), r.choice(categories_of_file),
		])
	
def main():
	if (!ospath.exists('./test_fixtures')): 
		os.makedirs('test_fixtures') #if the path does not exist then we will make a new directory with the same name for testing
	
	for file_name, sub_categories in FILES.items():
		with open(ospath.join(DIR, 'test_fixtures', file_name), 'w+', encoding='utf-8') as file_handle:
			write_file(
				csv.writer(file_handle, doublequote=False, escapechar='\\', quoting=csv.QUOTE_ALL)), r.randint(10,100), sub_categories
			)
	with open(ospath.join(DIR, 'test_fixtures', 'empty_file.csv'), 'w', encoding='utf-8') as file_handle:
		pass

if __name__ == '__main__':
    main()

