# process productions from the input file and populate dictionaries of terminal and nonterminal grammar symbols
# to save memory, each terminal/nonterminal object is created only once, meaning that each production is a list of
# references to grammar symbols


# represents one grammar symbol
class GrammarSymbol:
    def __init__(self, is_terminal, name):
        self.is_terminal = is_terminal
        self.name = name

    def __str__(self):
        return self.name


# represents one terminal grammar symbol (token)
class Terminal(GrammarSymbol):
    def __init__(self, name):
        super(Terminal, self).__init__(True, name)


# represents one nonterminal grammar symbol
class Nonterminal(GrammarSymbol):
    def __init__(self, name, is_start, type):
        self.is_start = is_start
        self.productions = []
        self.code = []
        self.type = type
        super(Nonterminal, self).__init__(False, name)


# throw this if error is encountered during production parsing
class ParseError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


# print all productions of a nonterminal symbol
def print_productions(nonterminal):
    if nonterminal.is_terminal:
        raise ParseError("Terminals do not have productions!")

    for prod in nonterminal.productions:
        print(nonterminal.name + " -> ", end = '')
        for sym in prod:
            print(str(sym) + " ", end = '')
        print()


# process one production of the input file
# every new terminal/nonterminal encountered is added to its respective dictionary
def process_production(head, body, type, code, terminals, nonterminals, terminals_list):
    if not head.islower():
        raise ParseError("Production head is not a nonterminal!")

    if head not in nonterminals.keys():
        start = False
        # first encountered terminal is the starting symbol
        if len(nonterminals.keys()) == 0:
            start = True
        nonterminals[head] = Nonterminal(head, start, type)

    production = []
    for sym in body.split():
        # epsilon productions have only one symbol in their bodies
        if sym == "Eps" and len(body.split()) == 1:
            production.append(terminals["eps"])
        # names of nonterminals should be lowercase
        elif sym.islower():
            if sym not in nonterminals.keys():
                nonterminals[sym] = Nonterminal(sym, False, type)
            production.append(nonterminals[sym])
        # names of terminals should be uppercase
        elif sym.isupper():
            if sym not in terminals_list:
                raise ParseError("Terminal " + sym + " was not defined in the _tokens section!")
            if sym not in terminals.keys():
                terminals[sym] = Terminal(sym)
            production.append(terminals[sym])
        else:
            raise ParseError("Unexpected symbol " + sym + " in the production stream!")
    nonterminals[head].productions.append(production)
    nonterminals[head].code.append(code)
