import argparse
import os

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
	


def main():
	input_name = "input.csv"
	output_name = generate_output_name(input_name)
	process(input_name, output_name)


if __name__ == "__main__":
	main()	