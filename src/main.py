import argparse
import configparser
from pprint import pprint
from utils import *
from attributes import *

def help(show=False):
	parser = argparse.ArgumentParser(description="")
	configs = parser.add_argument_group('Core features', 'This tool aims to measure the privacy levels in released data from the OMOP CDM structure')
	#configs.add_argument('-s', '--settings', dest='settings', \
	#					type=str, default="settings.ini", \
	#					help='The system settings file (default: settings.ini)')	
	aux_methods = parser.add_argument_group('Auxiliary methods', 'Methods useful during the development of this tool that may not be necessary for the last version.')
	aux_methods.add_argument('-rf', '--read-fields', default=False, action='store_true', \
						 help='When active, it reads the OMOP CDM CSV file with all fields and print them (default: False)')
	aux_methods.add_argument('-sa', '--show-attributes', default=False, action='store_true', \
						 help='When active, it reads and prints the attributes defined hardcoded in file attibutes.py (default: False)')

	aux_methods.add_argument('-la', '--latex-attributes', default=False, action='store_true', \
						 help='When active, it reads and prints the attributes in a format easy to insert in the latex document (default: False)')
	aux_methods.add_argument('-la-k', '--latex-attributes-key', default=False, action='store_true', \
						 help='When active, it reads and prints the key attributes in a format easy to insert in the latex document (default: False)')
	aux_methods.add_argument('-la-q', '--latex-attributes-quasi-identifier', default=False, action='store_true', \
						 help='When active, it reads and prints the quasi-identifier attributes in a format easy to insert in the latex document (default: False)')
	aux_methods.add_argument('-la-s', '--latex-attributes-sensitive', default=False, action='store_true', \
						 help='When active, it reads and prints the sensitive attributes in a format easy to insert in the latex document (default: False)')

	if show:
		parser.print_help()
	return parser.parse_args()

def readSettings(settingsFile):
	configuration = configparser.ConfigParser()
	configuration.read(settingsFile)
	if not configuration:
		raise Exception("The settings file was not found!")
	return configuration

def coreMethods(args):
	pass

def auxMethods(args):	
	if args.read_fields:
		readFields()

	if args.show_attributes:
		pprint(processAttributes(keyAttributes))
		pprint(processAttributes(sensitiveAttributes))
		pprint(processAttributes(quasiIdentifiers))

	if args.latex_attributes:
		print(attibutesToLatexTable(processAttributes(keyAttributes)))
		print(attibutesToLatexTable(processAttributes(sensitiveAttributes)))
		print(attibutesToLatexTable(processAttributes(quasiIdentifiers)))

	if args.latex_attributes_key:
		print(attibutesToLatexTable(processAttributes(keyAttributes)))

	if args.latex_attributes_quasi_identifier:
		print(attibutesToLatexTable(processAttributes(sensitiveAttributes)))
		
	if args.latex_attributes_sensitive:
		print(attibutesToLatexTable(processAttributes(quasiIdentifiers)))
		

def main():
	args = help()
	#settings = readSettings(args.settings)
	coreMethods(args)
	auxMethods(args)

if __name__ == "__main__":
	main()