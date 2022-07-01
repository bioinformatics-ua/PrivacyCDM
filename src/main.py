import argparse
import configparser
import utils

def help(show=False):
    parser = argparse.ArgumentParser(description="")
    configs = parser.add_argument_group('Privacy-preserving meets OMOP CDM', 'This tool aims to measure the privacy levels in released data from OMOP CDM structure')
    #configs.add_argument('-s', '--settings', dest='settings', \
    #                    type=str, default="settings.ini", \
    #                    help='The system settings file (default: settings.ini)')    
    configs.add_argument('-rf', '--read-fields', default=False, action='store_true', \
                         help='When active, it reads the OMOP CDM CSV file with all fields and print them (default: False)')


    if show:
        parser.print_help()
    return parser.parse_args()

def readSettings(settingsFile):
    configuration = configparser.ConfigParser()
    configuration.read(settingsFile)
    if not configuration:
        raise Exception("The settings file was not found!")
    return configuration


def main():
    args = help()
    settings = readSettings(args.settings)

    if args.read_fields:
        utils.readFields()

if __name__ == "__main__":
    main()