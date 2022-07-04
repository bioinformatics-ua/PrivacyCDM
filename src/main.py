import argparse
import configparser
from pprint import pprint
from utils import *
from attributes import *
from core import PluginEngine
import config

def help(show=False):
	parser = argparse.ArgumentParser(description="")
	core = parser.add_argument_group('Core features', 'This tool aims to measure the privacy levels in released data from the OMOP CDM structure')	
	core.add_argument('-ka', '--k-anonymity', default=False, action='store_true', \
						 help='It loads the k-anonymity plugin into the core (default: False)')
	core.add_argument('-k', '--k-value', dest='k_value', type=int, default=10, \
						help='The value of K (defaul: 10')	
	core.add_argument('-ld', '--l-diversity', default=False, action='store_true', \
						 help='It loads the l-diversity plugin into the core (default: False)')
	core.add_argument('-l', '--l-value', dest='l_value', type=int, default=5, \
						help='The value of L (defaul: 5')	
	core.add_argument('-dl', '--data-location', dest='data_location', type=str, default="", \
						help='The location of the dataset to be armonised')			
	core.add_argument('-el', '--export-location', dest='export_location', type=str, default="../results/", \
						help='The location to write the armonised dataset (defaul: ../results/')					 
	############################################
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


def coreMethods(args):
	if args.k_anonymity or args.l_diversity:
		if len(args.data_location) == 0:
			print("Error: The location of dataset was not defined!")
			help(True)
			exit(0)
			
		options = {
			"plugins": dict(),
			"directory": config.pluginsPath,
			"dataLocation": args.data_location,
			"delimiter": ",",
			"exportLocation": args.export_location
		}
		if args.k_anonymity:
			options["plugins"]["k-Anonymity"] = True
			config.k_anonymity = args.k_value
		if args.l_diversity:
			options["plugins"]["l-Diversity"] = True
			config.l_diversity = args.l_value
		PluginEngine(options=options).start()


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
	coreMethods(args)
	auxMethods(args)

if __name__ == "__main__":
	main()