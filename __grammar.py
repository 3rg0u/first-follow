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
        _changed = True  # compute til there's no change in all first-set
        while _changed:
            _idx = 0
            _state = [
                len(self.first[n_ter]) for n_ter in self.prods.keys()
            ]  # track state of all First(X)
            # check each non-ter X & its corresponding prods
            for n_ter, prds in self.prods.items():
                # discard all EPSILON prods
                prds.discard(_grammar.EPSILON)
                # check each prod X -> YZW...
                for rhs in prds:
                    _eps = len(rhs)  # tracking EPSILON-appearances
                    for symbol in rhs:
                        # First(X) = First(X) ∪ {First(Y) - {EPSILON}}
                        self.first[n_ter] |= self.first[symbol] - {_grammar.EPSILON}

                        # if EPSILON not in first(Y), end
                        if _grammar.EPSILON not in self.first[symbol]:
                            break
                        else:
                            _eps -= 1
                    self.first[n_ter] |= (
                        {_grammar.EPSILON} if _eps == 0 else set()
                    )  # _eps = 0 => EPSILON-able
                # update modifications
                _state[_idx] = len(self.first[n_ter]) != _state[_idx]
                _idx += 1
            _changed = True in _state  # True if _state was changed

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
                    for i, sym in enumerate(rhs):
                        if sym in self.non_ters:
                            self.follow[sym] |= self.__inter_first(rhs[i + 1 :])
                else:
                    # case: X -> αB
                    # follow(B) = follow(B) ∪ follow(X)
                    self.follow[rhs[-1]] |= self.follow[n_ter]

                    # the rest, which is follow(α), similar as above
                    # _rest = rhs[:-1]
                    for i, sym in enumerate(rhs):
                        if sym in self.non_ters:
                            _tmp = self.__inter_first(rhs[i + 1 :])
                            if _grammar.EPSILON in _tmp:
                                self.follow[sym] |= self.follow[n_ter]
                                continue
                            self.follow[sym] |= _tmp

    def __inter_first(self, sent):
        first = set()
        _eps = len(sent)
        for sym in sent:
            first |= self.first[sym] - {_grammar.EPSILON}
            if _grammar.EPSILON not in self.first[sym]:
                break
            _eps -= 1
        first |= {_grammar.EPSILON} if _eps == 0 else set()
        return first
