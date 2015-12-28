import argparse
import os
import sys

def generate_output_name(input_name):
	fname, ext = os.path.splitext(input_name)
	return '%s.output%s' % (fname, ext)

def process_line(line):
	parts = line.strip().split(';')
	try:
		amount = float(parts[-1].replace(',','.'))
	except ValueError:
		return None

	date = parts[1].replace('.','/')
	
	credit_amount = 0
	debit_amount = 0
	if amount < 0:
		debit_amount = -amount
	else:
		credit_amount = amount

	description = ' '.join(p for p in parts[3:6]).strip()
	
	return '%s;%s;%s;%f;%f\n' % (date, parts[0], description, credit_amount, debit_amount)

def process(input_name, output_name):
	assert os.path.isfile(input_name)

	with open(input_name) as f:
		in_lines = f.readlines()

	out_lines = []

	for l in in_lines:
		out_line = process_line(l)
		if not out_line:
			continue
		out_lines.append(out_line)

	with open(output_name,'w') as f:
		print("Writing %s" % output_name)
		f.writelines(out_lines)
	

def parse_args():
	parser = argparse.ArgumentParser(description='Convert an Amazon Credit Card CSV file for importing into GNUCash')
	parser.add_argument('input_name', help='The name of the input CSV file.')
	parser.add_argument('-o', required=False, default=None, help='The name of the output filename')
	parser.add_argument('-f', action='store_true', help='Overwrite the output file if it exists')

	return parser.parse_args()

def main():
	args = parse_args()

	input_name = args.input_name
	if args.o:
		output_name = args.o
	else:
		output_name = generate_output_name(input_name)

	if os.path.isfile(output_name):
		print "The output file %s already exists" % output_name
		if not args.f:
			print "exiting"
			sys.exit(1)
		else:
			print "Overwriting due to -f flag!"

	process(input_name, output_name)


if __name__ == "__main__":
	main()	