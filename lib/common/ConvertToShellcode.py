import argparse
from ShellcodeRDI import *

__version__ = '1.0'

def main():
    parser = argparse.ArgumentParser(description='RDI Shellcode Converter', conflict_handler='resolve')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s Version: ' + __version__)
    parser.add_argument('input_dll', help='DLL to convert to shellcode')
    parser.add_argument('-f', '--function-name', dest='function_name', default='SayHello', help='The function to call after DllMain')
    arguments = parser.parse_args()

    input_dll = arguments.input_dll
    output_bin = input_dll.replace('.dll', '.bin')

    print('Creating Shellcode: {}'.format(output_bin))
    dll = open(arguments.input_dll, 'rb').read()

    converted_dll = ConvertToShellcode(dll, functionHash=0x10)
    with open(output_bin, 'wb') as f:
        f.write(converted_dll)

if __name__ == '__main__':
    main()