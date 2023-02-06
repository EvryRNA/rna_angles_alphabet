import argparse


def return_hello(name: str):
    """
    Print the name in the terminal
    """
    assert type(name) == str
    print(f"Hello {name}")


def function_a():
    """
    Return None
    :return:
    """
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", dest="name", type=str, help="Name to print in the terminal")
    args = parser.parse_args()
    return_hello(**vars(args))
