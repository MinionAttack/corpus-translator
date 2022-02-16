# Corpus translator

Table of contents.

1. [Summary](#summary)
2. [How to use](#how-to-use)
3. [Examples](#examples)
4. [Licensing agreement](#licensing-agreement)

## Summary

Tool to translate the lemma and form columns of a corpus file in *CoNLL-U* format from one language to another.

## Project Structure

In this section you can have a quick view of the project structure.

```
.
├── corpus_translator.py
├── LICENSE
├── modules
│   ├── constants.py
│   └── translator.py
├── README.md
├── requirements.txt
└── translations
    ├── multibooked_ca
    │   └── head_final
    │       ├── dev-ca-es.conllu
    │       ├── dev-ca-es.json
    │       ├── train-ca-es.conllu
    │       └── train-ca-es.json
    ├── multibooked_eu
    │   └── head_final
    │       ├── dev-eu-es.conllu
    │       ├── dev-eu-es.json
    │       ├── train-eu-es.conllu
    │       └── train-eu-es.json
    └── norec
        └── head_final
            ├── dev-no-es.conllu
            ├── dev-no-es.json
            ├── train-no-es.conllu
            └── train-no-es.json
```

The `translations` folder contains some translated files used in the cross-lingual subtask
of [SemEval-2022 Shared Task 10: Structured Sentiment Analysis][1]

[1]: https://github.com/jerbarnes/semeval22_structured_sentiment

## How to use

Install the necessary dependencies listed in the `requirements.txt` file.

`$ pip3 install -r requirements.txt`

To run the script, from a terminal in the root directory, type:

`$ ./corpus_translator.py`

This will show the usage:

```
usage: corpus_translator.py [-h] {translate} ...

Tool for translating a corpus file from one language to another.

optional arguments:
  -h, --help   show this help message and exit

Commands:
  {translate}
    translate  Download the specified language, using the language code, from the OSCAR corpus.
```

If you want to know how to use a specific command, for example the *clean* command, type:

`$ ./corpus_translator.py translate --help`

And it will show the help:

```
usage: corpus_translator.py translate [-h] --input_language {ca,en,es,eu,no} --output_language {ca,en,es,eu,no} --input_file INPUT_FILE --output_file OUTPUT_FILE

optional arguments:
  -h, --help            show this help message and exit
  --input_language {ca,en,es,eu,no}
                        Language of the file to be translated.
  --output_language {ca,en,es,eu,no}
                        Language into which to translate the file.
  --input_file INPUT_FILE
                        Path of the CoNLL-U file to be translated.
  --output_file OUTPUT_FILE
                        Path to the folder where to create the translated file.
```

### Note

If you get an error that you do not have permissions to run the script, type:

`$ chmod u+x corpus_translator.py`

Run the script again.

## Examples

### 1. Translate a file

`$ ./corpus_translator.py translate --input_language es --output_language eu --input_file input --output_file output`

- **input**: Path of the *CoNLL-U* file to translate. For example: `path/to/file.conllu`
- **output**: Directory where the translated *CoNLL-U* file shall be created. For example: `path/where/to/save/the/translation/`

## Licensing agreement

MIT License

Copyright (c) 2021 Iago Alonso Alonso

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the
following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.