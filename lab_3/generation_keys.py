import argparse
import logging
import os


logging.basicConfig(level=logging.INFO)


def symmetric_key_generation(key_path: str, key_len: int) -> None:
    try:
        key = os.urandom(key_len)
        
        with open(f"{key_path[:-4]}_{key_len}.txt", 'wb') as key_file:
            key_file.write(key)
        logging.info(f"Key successfully generated and write to file: {key_path}.")
    except Exception as ex:
        logging.error(f"An error occurred while generating the key: {ex}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="An application for generate symmetric and asymmetric keys.")
    
    parser.add_argument(
        "--len",
        type=int,
        default=256,
        help="Encryption key length."
    )
    parser.add_argument(
        "--path",
        type=str,
        default='lab_3/symmetric_keys/symmetric.txt',
        help="Encryption key path."
    )
    
    args = parser.parse_args()

    symmetric_key_generation(args.path,args.len)