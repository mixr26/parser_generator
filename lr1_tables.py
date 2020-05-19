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
def print_goto_table(goto_table, nonterminals_list):
    header = ["   "] + [str(sym) + "  " for sym in nonterminals_list]
    print(*header)

    state = 0
    for row in goto_table:
        r = 'S' + str(state)
        for field in row:
            if field is None:
                r += "  "
            else:
                r += str(field) + " "
        print(*r)
        state += 1


# create ACTION and GOTO tables of the LR(1) parser
def create_tables(collection, start_state, nonterminals, terminals):
    # make lists out of data structures which hold collection of sets of LR(1) items, nonterminal symbols
    # and terminal symbols
    collection_list = list(collection.copy())
    collection_list.remove(start_state)
    collection_list.insert(0, start_state)

    terminals_list = [terminals[sym] for sym in terminals]
    terminals_list.remove(terminals["eps"])

    nonterminals_list = [nonterminals[sym] for sym in nonterminals]
    nonterminals_list.remove(nonterminals["__start"])

    # create empty tables
    action_table = [[None for y in range(len(terminals_list))] for x in range(len(collection_list))]
    goto_table = [[None for y in range(len(nonterminals_list))] for x in range(len(collection_list))]

    # iterate through every LR(1) item of every set of the collection
    for i in range(len(collection_list)):
        for item in collection_list[i]:
            # if dot is not at the end of a production
            if item.dot < len(item.production):
                # the incoming symbol is the one in front of the dot
                sym = item.production[item.dot]
                # compute the GOTO state from this state on the incoming symbol
                goto_state = goto(collection_list[i], sym, terminals)
                if len(goto_state) == 0:
                    continue
                goto_state_index = collection_list.index(goto_state)
                # if the incoming symbol is a terminal, we populate ACTION table
                if sym.is_terminal:
                    sym_index = terminals_list.index(sym)
                    # check whether there is a conflict on the ACTION table entry
                    if action_table[i][sym_index] is None:
                        action_table[i][sym_index] = ('s', goto_state_index)
                    elif action_table[i][sym_index] != ('s', goto_state_index):
                        raise ConflictError("Grammar conflict! Aborting table generation!")
                # if the incoming symbol is a nonterminal, we populate GOTO table
                else:
                    sym_index = nonterminals_list.index(sym)
                    # check whether there is a conflict on the GOTO table entry
                    if goto_table[i][sym_index] is None:
                        goto_table[i][sym_index] = goto_state_index
                    elif goto_table[i][sym_index] != goto_state_index:
                        raise ConflictError("Grammar conflict! Aborting table generation!")
            # if the dot is at the end of a production
            else:
                sym = item.lookahead
                # if the head of the item production is the start symbol, this is an accepting configuration
                if item.nonterminal == nonterminals["__start"] and item.dot == 1 and sym == terminals['$']:
                    action_table[i][terminals_list.index(sym)] = 'a'
                # else check whether we should reduce or if we have a conflict on the ACTION table entry
                elif item.nonterminal != nonterminals["__start"] and action_table[i][terminals_list.index(sym)] is None:
                    action_table[i][terminals_list.index(sym)] = ('r', item.nonterminal, item.production)
                elif item.nonterminal != nonterminals["__start"] and \
                        action_table[i][terminals_list.index(sym)] != ('r', item.nonterminal, item.production):
                    raise ConflictError("Grammar conflict! Aborting table generation!")

    return action_table, goto_table, terminals_list, nonterminals_list,


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
    (collection, start_state) = create_collection(nonterminals, terminals)
    (action_table, goto_table, terminals_list, nonterminals_list) = \
        create_tables(collection, start_state, nonterminals, terminals)
    print_goto_table(goto_table, nonterminals_list)
