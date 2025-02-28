### Description

A simple implementation for computing $First$ and $Follow$ of a given grammar $G$ using Python.

### How to use

Inside the `main.py` script, init an instance of `_grammar`, passing these params `[starts, non_ters, ters, prods]`, where:

- `starts`: set of start symbols of grammar.
- `non_ters`: set of non-terminal symbols.
- `ters`: set of terminal symbols.
- `prods`: set of grammar's productions.
- Use the constant variable `_grammar.EPSILON`, `_grammar.ENDMARK` for $\epsilon$ and $ \$ $, respectively.

Here is an example:

```python
starts = ('S', 'A')
non_ters = ('S', 'A', 'B', 'C')
ters = ('a', 'b', 'c', 'd', 'e')
prods = {
    'S': {'ABC'}, # S -> ABC
    'A': {'BC', 'Cd'} # A -> BC | Cd
    'B': {'CC', _grammar.EPSILON}, # B -> CC | epsilon
    'C': {'d', 'e'} # C -> d | e
}

# init grammar
g = _grammar(starts=starts, non_ters=non_ters, ters=ters, prods=prods)

first = g.first # get First set
follow = g.follow # get Follow set
```
