class _grammar:
    """
    @static variables
    """

    EPSILON = "_epsilon"
    ENDMARK = "$"

    def __init__(
        self,
        starts: tuple = None,
        non_ters: tuple = None,
        ters: tuple = None,
        prods: dict = None,
    ):
        """
        params:
        - starts: a tuple of non-terminal symbols which are used as starting point
        - non_ters: a tuple of non-terminal symbols of grammar
        - ters: a tuple of terminal symbols of grammar
        - prods: a list of productions of grammar
        example:
        - starts: {'S'}
        - non_ters: {'A', 'B', 'C'}
        - ters: {'c', 'd', 'e'}
        - prods:{
                'A': {'BC', _grammar.EPSILON},
                'B': {'Cd'},
                'C': {'e', _grammar.EPSILON}
                }
        """
        self.starts = starts
        self.non_ters = non_ters
        self.ters = ters
        self.prods = prods
        self.__first()
        self.__follow()

    def __first(self):
        """
        compute Fist set for all grammar symbols X
        """

        # if X is a terminal symbol, then first(X) = {X}
        self.first = {ter: {ter} for ter in self.ters}

        # if X -> EPSILON is a production, then add EPSILON to first(X)
        for n_ter in self.non_ters:
            self.first[n_ter] = (
                {_grammar.EPSILON} if _grammar.EPSILON in self.prods[n_ter] else set()
            )

        # case: X -> Y1Y2Y3...Yn
        _is_changed = True  # compute til there's no change in all first-set
        while _is_changed:
            _is_changed = False
            # check each non-ter X & its corresponding prods
            for n_ter, prds in self.prods.items():
                _len_state = len(self.first[n_ter])  # track num-of-elms of first(X)
                # remove EPSILON if it's a production
                prds.discard(_grammar.EPSILON)
                # check each prod X -> YZW...
                for rhs in prds:
                    _eps_cnt = len(rhs)  # track EPSILON-appearances
                    for symbol in rhs:
                        # First(X) = First(X) ∪ {First(Y) - {EPSILON}}
                        self.first[n_ter] |= self.first[symbol] - {_grammar.EPSILON}
                        if _grammar.EPSILON not in self.first[symbol]:
                            break
                        _eps_cnt -= 1
                        # X ->* EPSILON, add EPSILON to First(X)
                    self.first[n_ter] |= {_grammar.EPSILON} if _eps_cnt == 0 else set()
                _is_changed = _len_state != len(
                    self.first[n_ter]
                )  # whether First(X) is modified

    def __follow(self):
        """
        compute Follow set for all non-terminal symbols X
        """
        self.follow = dict()

        # if X in starts, Follow(X).add($), else {}
        for n_ter in self.non_ters:
            self.follow[n_ter] = (
                set() if n_ter not in self.starts else {_grammar.ENDMARK}
            )

        for n_ter, prds in self.prods.items():
            prds.discard(_grammar.EPSILON)  # discard all EPSILON-able prod
            for rhs in prds:
                # case: X -> αBβ, where β is in form of γa
                # => first(β) cannot include EPSILON
                # => follow(B) = follow(B) ∪ first(β)
                if rhs[-1] in self.ters:
                    for i, symbol in enumerate(rhs):
                        if symbol in self.non_ters:
                            self.follow[symbol] |= self.__inter_first(rhs[i + 1 :])
                else:
                    # case: X -> αB
                    # follow(B) = follow(B) ∪ follow(X)
                    self.follow[rhs[-1]] |= self.follow[n_ter]

                    # the rest, which is follow(α), similar as above
                    _rest = rhs[:-1]
                    for i, symbol in enumerate(_rest):
                        if symbol in self.non_ters:
                            _tmp = self.__inter_first(_rest[i + 1 :])
                            if _grammar.EPSILON in _tmp:
                                self.follow[symbol] |= self.follow[n_ter]
                                continue
                            self.follow[symbol] |= _tmp

    def __inter_first(self, sent):
        first = set()
        _eps_cnt = len(sent)
        for symbol in sent:
            first |= self.first[symbol] - {_grammar.EPSILON}
            if _grammar.EPSILON not in self.first[symbol]:
                break
            _eps_cnt -= 1
        first |= {_grammar.EPSILON} if _eps_cnt == 0 else set()
        return first
