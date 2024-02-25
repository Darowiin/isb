import argparse
import logging
from read_write import read_file,write_to_file


logging.basicConfig(level=logging.INFO)


ALPHABET_RU = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def encryption_text(path: str, encryption_path: str, step: int) -> None:
    """
    Encrypts the text from a file using a Caesar cipher with the specified step.

    Args:
        path (str): The path to the input file.
        encryption_path (str): The path to the output file for the encrypted text.
        step (int): The step (shift) to be used in the Caesar cipher.

    Raises:
        IOError: If there is an issue reading the input file or writing to the output file.
    """
    try:
        data = read_file(path)
        result = ""
        for i in data:
            if i == " ":
                result += " "
                continue
            new_idx = (ALPHABET_RU.find(i) + step) % len(ALPHABET_RU)
            result += ALPHABET_RU[new_idx]

        write_to_file(encryption_path, result)
    except Exception as ex:
        logging.error(f"Error during text encryption: {ex}\n")
        
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Caesar Cipher Text Encryption")
    parser.add_argument(
        "--input_file",
        type=str,
        default="lab_1/task_1/original_text.txt",
        help="Path to the input file containing the text to be encrypted."
    )

    parser.add_argument(
        "--output_file",
        type=str,
        default="lab_1/task_1/encryption_text.txt",
        help="Path to the output file where the encrypted text will be saved."
    )

    parser.add_argument(
        "--step",
        type=int,
        default=4,
        help="The step (shift) to be used in the Caesar cipher. Default is 4."
    )

    args = parser.parse_args()

    try:
        encryption_text(args.input_file, args.output_file, args.step)
        logging.info(f"Text successfully encrypted and saved to {args.output_file}")
    except Exception as ex:
        logging.error(f"Error during encryption: {ex}")