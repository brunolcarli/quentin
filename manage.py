import os
import sys
from runner import run

def help_message():
    """Shows help message"""
    sys.stdout.write('Quentin command manager options: \n\n')
    for key, value in interface.items():
        sys.stdout.write(f'\t{key}\n')
        sys.stdout.write(f'\t\t{value["help"]}\n\n')


interface = {
    'test': {
        'runner': lambda: os.system('make test'),
        'help': 'Run unit tests.'
    },
    'run': {
        'runner': run,
        'help': 'Run main service.'
    },
    'help': {
        'runner': help_message,
        'help': 'Shows this message.'
    }
}

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        sys.stdout.write(
            'No parameter was give.\n|-> Use python.manage.py help for more information.'
        )

    command = sys.argv[1]
    if command not in interface.keys():
        sys.stdout.write('Comando não reconhecido!')
    else:
        launch = interface[command].get('runner')
        launch()