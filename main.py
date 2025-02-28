from __grammar import _grammar
from pprint import pprint


def main():
    non_ters = ("S", "A", "B", "C", "D")
    ters = ("a", "b", "c", "d", "u")

    prods = {
        "S": {
            "ABCd",
        },
        "A": {"CDu", _grammar.EPSILON},
        "B": {"bd", "cDd", _grammar.EPSILON},
        "C": {"aA", _grammar.EPSILON},
        "D": {"Dd", _grammar.EPSILON},
    }

    g = _grammar(starts=("S"), non_ters=non_ters, ters=ters, prods=prods)
    print("First set:")
    pprint(g.first)
    print("\n\n\n")
    print("Follow set: ")
    pprint(g.follow)


if __name__ == "__main__":
    main()
