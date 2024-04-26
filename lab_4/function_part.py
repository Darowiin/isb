import hashlib
import logging
import json
import os
import multiprocessing as mp


logging.basicConfig(level=logging.INFO)


def check_hash(x: int, bins: tuple, hash: str, last_numbers: str) -> tuple:
    """hash verification function

    Args:
    x (int): the intended digits of the card number
    bins (tuple): a tuple with the intended BIN
    hash (str): hash value
    last_num (str): the last 4 digits of the number

    Returns:
    tuple: in case of a match, a tuple with the BIN, the correct number and the last digits.
    """
    x = str(x).zfill(6)
    for bin in bins:
        if hashlib.blake2b(f"{bin}{x}{last_numbers}".encode()).hexdigest() == hash:
            return (bin, x, last_numbers)
    return None


def find_card_data(bins: tuple, hash: str, last_numbers: str) -> str:
    """bank card data search function

    Args:
    bins (tuple): a tuple with the intended BIN
    hash (str): hash value
    last_num (str): the last 4 digits of the number

    Returns:
    str: card number in the form of a string.
    """
    try:
        args = []
        for i in range(0, 1000000):
            args.append((i, bins, hash, last_numbers))
            
        with mp.Pool(processes=mp.cpu_count()) as p:
            for result in p.starmap(check_hash, args):
                if result:
                    logging.info(f'Number of card: {result[0]}-{result[1]}-{result[2]}')
                    p.terminate()
                    return (str(f'{result[0]}{result[1]}{result[2]}'))
    except Exception as ex:
        logging.error(f"The card data couldn't be found: {ex}\n")
    
            
if __name__ == "__main__":
    with open(os.path.join("lab_4","settings.json"), "r") as settings_file:
        settings = json.load(settings_file)
    result = find_card_data(settings["bins"], settings["hash"], settings["last_numbers"])