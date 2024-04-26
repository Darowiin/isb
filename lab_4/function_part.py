import hashlib
import logging
import json
import os
import time
import multiprocessing as mp
import matplotlib.pyplot as plt

from tqdm import tqdm


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


def luhn_alg(card_numbers: str) -> None:
    """a function that checks the card number using the Luhn algorithm

    Args:
    card_numbers (int): Card number
    """
    try:
        result = int(card_numbers[-1])
        list_numbers = [int(i) for i in (card_numbers[::-1])]
        for i, num in enumerate(list_numbers):
            if i % 2 == 0:
                mul = num*2
                if mul > 9:
                    mul -= 9
                list_numbers[i] = mul
        total_sum = sum(list_numbers)
        rem = total_sum % 10
        check_sum = 10 - rem if rem != 0 else 0
        
        if check_sum == result:
            logging.info("The card data have passed the test for compliance with the Luhn algorithm.")
        else:
            logging.info("The card data didn't pass the test for compliance with the Luhn algorithm.")
    except Exception as ex:
        logging.error(f"An error occurred while executing the luhn algorithm: {ex}\n")
    

def time_measurement(bins: tuple, hash: str, last_numbers: str) -> None:
    """A function for measuring time and drawing a graph depending on the number of processes

    Args:
    bins (tuple): a tuple with the intended BIN
    hash (str): hash value
    last_num (str): the last 4 digits of the number
    """
    try:
        args = []
        for i in range(0, 1000000):
            args.append((i, bins, hash, last_numbers))
            
        times_list = []
        for i in tqdm(range(1, int(mp.cpu_count() * 1.5)), desc="Processes"):
            start = time.time()
            with mp.Pool(processes=i) as p:
                for result in p.starmap(check_hash, args):
                    if result:
                        end = time.time() - start
                        times_list.append(end)
                        p.terminate()
                        break
        fig=plt.figure(figsize=(15, 5))
        plt.plot(
            range(len(times_list)),
            times_list,
            linestyle=":",
            color="black",
            marker="x",
            markersize=10,
        )
        plt.bar(range(len(times_list)), times_list)
        plt.xlabel("Процессы")
        plt.ylabel("Время в секундах")
        plt.title("График зависимости времени от числа процессов")
        plt.show()
    except Exception as ex:
        logging.error(f"An error occurred when measuring time and drawing a graph: {ex}\n")



if __name__ == "__main__":
    with open(os.path.join("lab_4","settings.json"), "r") as settings_file:
        settings = json.load(settings_file)
    result = find_card_data(settings["bins"], settings["hash"], settings["last_numbers"])
    luhn_alg(result)
    time_measurement(settings["bins"], settings["hash"], settings["last_numbers"])