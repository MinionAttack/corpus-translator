# -*- coding: utf-8 -*-

from pathlib import Path
from re import search
from typing import Any, Tuple

from torch import device, cuda
from tqdm.asyncio import tqdm
from transformers import MarianTokenizer, MarianMTModel

from modules.constants import CATALAN_MODELS, ENGLISH_MODELS, SPANISH_MODELS, BASQUE_MODELS, NORWEGIAN_MODELS, PUNCTUATION_SYMBOLS


def translate_corpus(input_language: str, output_language: str, input_file: str, output_file: str) -> None:
    print(f"INFO: Translating corpus from {input_language} to {output_language}")

    tokenizer, model = get_translation_tools(input_language, output_language)
    if tokenizer is not None and model is not None:
        process_file(tokenizer, model, input_file, output_file)
    else:
        print(f"ERROR: The combination of the selected languages is not available")


def get_translation_tools(input_language: str, output_language: str) -> Tuple[Any, Any]:
    print(f"INFO: Selecting the model, please wait")

    pattern = f"opus-mt-{input_language}-{output_language}$"
    if input_language == "ca":
        model_name = find_model(pattern, CATALAN_MODELS)
    elif input_language == "en":
        model_name = find_model(pattern, ENGLISH_MODELS)
    elif input_language == "es":
        model_name = find_model(pattern, SPANISH_MODELS)
    elif input_language == "eu":
        model_name = find_model(pattern, BASQUE_MODELS)
    elif input_language == "no":
        model_name = find_model(pattern, NORWEGIAN_MODELS)
    else:
        model_name = None
        print(f"ERROR: Language {input_language} not supported")

    if model_name is not None:
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)

        return tokenizer, model
    else:
        tokenizer = None
        model = None

        return tokenizer, model


def find_model(pattern: str, models) -> Any:
    model_name = None
    for model in models:
        if search(pattern, model) is not None:
            model_name = model
            break

    return model_name


def process_file(tokenizer: MarianTokenizer, model: MarianMTModel, input_file: str, output_file: str) -> None:
    print(f"INFO: Processing the corpus")

    input_data = Path(input_file)
    if input_data.exists() and input_data.is_file() and input_data.suffix == ".conllu":
        output_data = Path(output_file)
        if output_data.is_dir():
            input_name = input_data.name
            output_data = output_data.joinpath(input_name)
            with tqdm(total=input_data.stat().st_size, desc="Translating the FORM and LEMMA parts of sentences") as progress_bar:
                with open(input_data, 'rt', encoding='UTF-8') as original, open(output_data, 'wt', encoding='UTF-8') as translated:
                    for line in original:
                        progress_bar.update(len(line))
                        if not line.startswith("# sent_id =") and not line.startswith("# text ="):
                            if line != "\n":
                                translated_line = translate_columns(tokenizer, model, line)
                                translated.write(translated_line)
                            else:
                                translated.write('\n')
                        else:
                            translated.write(line)
        else:
            print(f"ERROR: The output path is not a directory")
    else:
        print(f"ERROR: The input file is not valid")


def translate_columns(tokenizer: MarianTokenizer, model: MarianMTModel, line: str) -> str:
    line = line.replace("\n", "")
    columns = line.split("\t")
    original_form = columns[1]
    original_lemma = columns[2]
    translated_form = translate_word(tokenizer, model, original_form)
    translated_lemma = translate_word(tokenizer, model, original_lemma)
    columns[1] = translated_form
    columns[2] = translated_lemma
    new_line = '\t'.join(columns) + '\n'

    return new_line


def translate_word(tokenizer: MarianTokenizer, model: MarianMTModel, original: str) -> str:
    execution_device = device('cuda' if cuda.is_available() else 'cpu')
    model.to(execution_device)
    batch = tokenizer([original], return_tensors="pt").to(execution_device)
    generated = model.generate(**batch)
    translation = tokenizer.batch_decode(generated, skip_special_tokens=True)[0]
    fixed = fix_errors(original, translation)

    return fixed


def fix_errors(original: str, translation: str) -> str:

    fixed = translation
    if len(original) == 1 and original in PUNCTUATION_SYMBOLS:
        fixed = translation
    if len(original) == 1 and original in PUNCTUATION_SYMBOLS and len(translation) > len(original) and translation[0] in PUNCTUATION_SYMBOLS:
        if original == translation[0]:
            fixed = translation[0]
        else:
            fixed = original
    if original == "be" and translation.startswith("#"):
        fixed = translation.split("#")[1].strip()
    # We need to use 'fixed' instead of 'translation' so as not to add the removed punctuation symbols again
    if len(original) > 1 and fixed[0] in PUNCTUATION_SYMBOLS and original[0] not in PUNCTUATION_SYMBOLS:
        fixed = fixed[1:]
    # We need to use 'fixed' instead of 'translation' so as not to add the removed punctuation symbols again
    if len(original) > 1 and fixed[-1] in PUNCTUATION_SYMBOLS and original[-1] not in PUNCTUATION_SYMBOLS:
        fixed = fixed[0:-1]
    # We need to use 'fixed' instead of 'translation' so as not to add the removed punctuation symbols again
    if original[0].islower() and fixed[0].isupper():
        fixed = fixed[0].lower() + fixed[1:]
    # We need to use 'fixed' instead of 'translation' so as not to add the removed punctuation symbols again
    if original[0].isupper() and fixed[0].islower():
        fixed = fixed.capitalize()

    return fixed
