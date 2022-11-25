import argparse
import os


def main():
    parser = argparse.ArgumentParser(description="Think of a number and I'll find it out")
    parser.add_argument("number", nargs="?", type=int, help="Your number if I didn't find it out")
    args = parser.parse_args()
    guess_number(args.number)


def guess_number(number):
  if number is None:
      print(42)
  else:
      clear_screen()
      print("Just what I said: {}".format(number))


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


main()