from process_production import process_production, Terminal


# this implements FIRST and FOLLOW sets computation
# algorithms in use can be found in [1]
#
# [1] The Dragon Book, 2nd Ed, p. 221


# error while computing FIRST/FOLLOW sets
class FirstFollowError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


# given a string of symbols, computes the FIRST set of the string
def first_syms(symbols, terminals):
    seen_eps = True
    for symbol in symbols:
        if not seen_eps:
            break

        tmp_set = first(symbol, terminals)
        if terminals["eps"] in tmp_set:
            tmp_set.remove(terminals["eps"])
        else:
            seen_eps = False

    # if there is an epsilon in FIRST set of every symbol, add epsilon to the FIRST set of the string
    if seen_eps:
        tmp_set.add(terminals["eps"])

    return tmp_set


# helper function which iterates over productions for a nonterminal symbol
def first(symbol, terminals):
    if symbol.is_terminal:
        return {symbol}

    sym_set = set()
    for production in symbol.productions:
        # if this is an empty production, add the epsilon terminal to the FIRST set
        if production[0].name == "eps":
            sym_set.add(terminals["eps"])
            continue

        sym_set |= first_syms(production, terminals)

    return sym_set


# given a nonterminal symbol, compute its FOLLOW set
def follow(symbol, terminals, nonterminals):
    sym_set = set()

    if symbol.is_terminal:
        raise FirstFollowError("FOLLOW sets can be calculated for nonterminal symbols only!")

    if symbol.is_start:
        sym_set.add(terminals['$'])

    for nonterminal in nonterminals:
        for production in nonterminals[nonterminal].productions:
            for i in range(0, len(production)):
                # symbol is in a middle of a production
                if production[i] == symbol and i < len(production) - 1:
                    # compute FIRST set of the rest of the production
                    first_set = first_syms(production[i + 1:len(production)], terminals)
                    # rest of the production can produce epsilon
                    if terminals['eps'] in first_set:
                        first_set.remove(terminals['eps'])
                        if nonterminals[nonterminal] != symbol:
                            sym_set |= follow(nonterminals[nonterminal], terminals, nonterminals)
                    sym_set |= first_set
                # symbol is at the end of a production
                elif production[i] == symbol and i == len(production) - 1:
                    if nonterminals[nonterminal] != symbol:
                        sym_set |= follow(nonterminals[nonterminal], terminals, nonterminals)

    return sym_set


if __name__ == "__main__":
    terminals = {"eps": Terminal("eps"), "$": Terminal("$")}
    nonterminals = dict()
    process_production("e", "t eprim", terminals, nonterminals)
    process_production("eprim", "PLUS t eprim", terminals, nonterminals)
    process_production("eprim", "Eps", terminals, nonterminals)
    process_production("t", "f tprim", terminals, nonterminals)
    process_production("tprim", "MULT f tprim", terminals, nonterminals)
    process_production("tprim", "Eps", terminals, nonterminals)
    process_production("f", "OPAR e CPAR", terminals, nonterminals)
    process_production("f", "ID", terminals, nonterminals)
    #print_productions(nonterminals['a'])
    #print_productions(nonterminals['b'])

    #first_set = first_syms([nonterminals['tprim']], terminals)
    #for sym in first_set:
    #    print(sym)
    follow_set = follow(nonterminals['f'], terminals, nonterminals)
    for sym in follow_set:
        print(sym)
