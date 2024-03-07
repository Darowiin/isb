import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required = True)
group.add_argument('-gen','--generation',help='Запускает режим генерации ключей')
group.add_argument('-enc','--encryption',help='Запускает режим шифрования')
group.add_argument('-dec','--decryption',help='Запускает режим дешифрования')

args = parser.parse_args()
if args.gen:
    print("")
elif args.enc:
    print("")
else:
    print("")