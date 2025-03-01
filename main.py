from __grammar import _grammar
from pprint import pprint


def main():
    # starts = "S"
    # non_ters = ("S", "A", "B", "C", "D")
    # ters = ("b", "c", "d")

    # prods = {
    #     "S": {"Ac", "BBc"},
    #     "B": {"dBb", "dDb", _grammar.EPSILON},
    #     "A": {"BC"},
    #     "C": {"b", "bCd"},
    #     "D": {"bd", "bDd"},
    # }

    # starts = "S"
    # non_ters = ("S", "A")
    # ters = ("a", "b")
    # prods = {"S": {"AS", "b"}, "A": {"SA", "a"}}

    starts = "S"
    non_ters = ("S", "A", "B", "C", "D")
    ters = ("a", "b", "c", "d", "u")
    prods = {
        "S": {"ABCd"},
        "A": {"CDu", _grammar.EPSILON},
        "B": {"bd", "cDd", _grammar.EPSILON},
        "C": {"aA", _grammar.EPSILON},
        "D": {"Dd", _grammar.EPSILON},
    }

    g = _grammar(starts=starts, non_ters=non_ters, ters=ters, prods=prods)
    print("First set:")
    pprint(g.first)
    print("\n\n\n")
    print("Follow set: ")
    pprint(g.follow)


if __name__ == "__main__":
    main()
