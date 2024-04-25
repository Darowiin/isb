import hashlib
import logging
import json
import multiprocessing as mp

def check_hash(x: int, bins: tuple, hash: str, last_numbers: str) -> tuple:
    x = str(x).zfill(6)
    for bin in bins:
        if hashlib.blake2b(f"{bin}{x}{last_numbers}".encode()).hexdigest() == hash:
            return (bin, x, last_numbers)
    return False

def find_card_data(bins: tuple, hash: str, last_numbers: str) -> str:
    args = []
    for i in range(0, 1000000):
        args.append((i, bins, hash, last_numbers))
        
    with mp.Pool(processes=4) as p:
        for result in p.starmap(check_hash, args):
            if result:
                logging.info(
                    f'Number of card: {result[0]}-{result[1]}-{result[2]}')
                p.terminate()
                return (str(f'{result[0]}{result[1]}{result[2]}'))
    return "Card data not found"
            
if __name__ == "__main__":
    with open("lab_4/settings.json", "r") as settings_file:
        settings = json.load(settings_file)
    result = find_card_data(settings["bins"], settings["hash"], settings["last_numbers"])
    print(result) #4274 0202 3652 0877