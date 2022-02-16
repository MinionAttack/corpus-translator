#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser, Namespace

from modules.translator import translate_corpus


def main() -> None:
    parser = ArgumentParser(description='Tool for translating a corpus file from one language to another.')
    subparsers = parser.add_subparsers(title='Commands', dest='command')

    # Translate
    subparser = subparsers.add_parser('translate', help='Download the specified language, using the language code, from the OSCAR corpus.')
    subparser.add_argument('--input_language', type=str, choices=['ca', 'en', 'es', 'eu', 'no'], required=True, help="Language of the file "
                                                                                                                     "to be translated.")
    subparser.add_argument('--output_language', type=str, choices=['ca', 'en', 'es', 'eu', 'no'], required=True, help="Language into which "
                                                                                                                      "to translate the "
                                                                                                                      "file.")
    subparser.add_argument('--input_file', type=str, required=True, help="Path of the CoNLL-U file to be translated.")
    subparser.add_argument('--output_file', type=str, required=True, help="Path to the folder where to create the translated file.")

    arguments = parser.parse_args()
    if arguments.command:
        process_arguments(arguments)
    else:
        parser.print_help()


def process_arguments(arguments: Namespace) -> None:
    print("INFO: Processing arguments")

    command = arguments.command
    if command == "translate":
        input_language = arguments.input_language
        output_language = arguments.output_language
        input_file = arguments.input_file
        output_file = arguments.output_file
        translate_corpus(input_language, output_language, input_file, output_file)
    else:
        print(f"Error: Command {command} is not recognised")


if __name__ == "__main__":
    main()
