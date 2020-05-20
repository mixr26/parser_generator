from lr1_collection import print_collection, create_collection, goto
from process_production import process_production, Terminal


# this implements the computation of ACTION and GOTO tables of an LR(1) parser as described in [1]
#
# [1] The Dragon Book, 2nd Ed, p. 265


# throw this if error is encountered during LR(1) tables generation
class ConflictError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


# helper function which prints GOTO table
def print_goto_table(goto_table):
    header = ["   "] + goto_table[0]
    print(*header)

    state = 0
    for row in goto_table[1:len(goto_table)]:
        r = 'S' + str(state)
        for field in row:
            if field is None:
                r += ' '
            else:
                r += str(field)
        print(*r)
        state += 1


# create ACTION and GOTO tables of the LR(1) parser
def create_tables(collection, nonterminals, terminals):
    # create empty tables
    action_header = []
    for terminal in terminals:
        if terminal != "eps":
            action_header.append(terminal)

    action_table = [[None for y in range(len(terminals) - 1)] for x in range(len(collection))]
    action_table.insert(0, action_header)

    goto_header = []
    for nonterminal in nonterminals:
        if nonterminal != "__start":
            goto_header.append(nonterminal)

    goto_table = [[None for y in range(len(nonterminals) - 1)] for x in range(len(collection))]
    goto_table.insert(0, goto_header)

    # iterate through every LR(1) item of every set of the collection
    for i in range(len(collection)):
        for item in collection[i]:
            # if dot is not at the end of a production
            if item.dot < len(item.production):
                # the incoming symbol is the one in front of the dot
                sym = item.production[item.dot]
                # compute the GOTO state from this state on the incoming symbol
                goto_state = goto(collection[i], sym, terminals)
                if len(goto_state) == 0:
                    continue
                goto_state_index = collection.index(goto_state)
                # if the incoming symbol is a terminal, we populate ACTION table
                if sym.is_terminal:
                    sym_index = action_table[0].index(sym.name)
                    # check whether there is a conflict on the ACTION table entry
                    if action_table[i + 1][sym_index] is None:
                        action_table[i + 1][sym_index] = ('s', goto_state_index)
                    elif action_table[i + 1][sym_index] != ('s', goto_state_index):
                        raise ConflictError("Grammar conflict! Aborting table generation!")
                # if the incoming symbol is a nonterminal, we populate GOTO table
                else:
                    sym_index = goto_table[0].index(sym.name)
                    # check whether there is a conflict on the GOTO table entry
                    if goto_table[i + 1][sym_index] is None:
                        goto_table[i + 1][sym_index] = goto_state_index
                    elif goto_table[i + 1][sym_index] != goto_state_index:
                        raise ConflictError("Grammar conflict! Aborting table generation!")
            # if the dot is at the end of a production we add a reduce field
            else:
                sym = item.lookahead
                sym_index = action_table[0].index(sym.name)
                # if the head of the item production is the start symbol, this is an accepting configuration
                if item.nonterminal == nonterminals["__start"] and item.dot == 1 and sym == terminals['$']:
                    action_table[i + 1][sym_index] = 'a'
                # else check whether we should reduce or if we have a conflict on the ACTION table entry
                elif item.nonterminal != nonterminals["__start"] and action_table[i + 1][sym_index] is None:
                    action_table[i + 1][sym_index] = ('r', item.nonterminal, item.production)
                elif item.nonterminal != nonterminals["__start"] and \
                        action_table[i + 1][sym_index] != ('r', item.nonterminal, item.production):
                    raise ConflictError("Grammar conflict! Aborting table generation!")

    return action_table, goto_table


if __name__ == "__main__":
    terminals = {"eps": Terminal("eps"), "$": Terminal("$")}
    nonterminals = dict()
    process_production("s", "c c", terminals, nonterminals)
    process_production("c", "C c", terminals, nonterminals)
    process_production("c", "D", terminals, nonterminals)
    # for sym in [nonterminals[key] for key in nonterminals]:
    #    print_productions(sym)
    # item = Item(nonterminals["__start"], nonterminals["__start"].productions[0], 0, terminals['$'])
    # items = {item}
    # items = closure(items, terminals)
    # items = goto(items, nonterminals['c'], terminals)
    collection = create_collection(nonterminals, terminals)
    (action_table, goto_table) = create_tables(collection, nonterminals, terminals)
    print_goto_table(goto_table)
