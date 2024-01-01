import os
from configparser import ConfigParser

current_dir = os.path.dirname(os.path.abspath(__file__))
database_ini_path = os.path.join(current_dir, 'database.ini')


def config(filename=database_ini_path, section='postgresql'):
    # Print the current working directory
    print("Current Working Directory:", os.getcwd())

    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} is not found in the {1} file.'.format(section, filename))

    return db