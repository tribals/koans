import sys


def main():
    path = sys.argv[1]
    text = read_file_reliably(path)
    print(text)


def read_file_reliably(path):
    try:
        read_file(path)
    except FileNotFoundError as e:
        raise DomainError from e


def read_file(path):
    with open(path) as f:
        return f.read()


class DomainError(Exception):
    pass


if __name__ == '__main__':
    main()
