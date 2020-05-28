from process_production import Nonterminal
from first_follow import first_syms


# this creates a collection of sets of LR(1) items as described by the algorithms in [1]
#
# [1] The Dragon Book, 2nd Ed, p. 261


# represents one LR(1) item
# LR(1) is defined by a production of a nonterminal, position of the dot, and lookahead symbol
class Item:
    def __init__(self, nonterminal, production, dot, lookahead):
        self.nonterminal = nonterminal
        self.production = production
        self.dot = dot
        self.lookahead = lookahead

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.nonterminal == other.nonterminal \
               and self.production == other.production \
               and self.dot == other.dot \
               and self.lookahead == other.lookahead

    def __str__(self):
        ret = '[' + str(self.nonterminal) + " -> "
        for i in range(0, len(self.production)):
            if i == self.dot:
                ret += "* "
            ret += str(self.production[i]) + ' '
        if self.dot == len(self.production):
            ret += "* "
        ret += ", " + str(self.lookahead) + ']'

        return ret


# augment the described grammar by adding a 'false' starting symbol and its production which derives the original
# starting symbol
def augment_grammar(nonterminals):
    start_sym = None
    # find the original starting symbol
    for sym in nonterminals:
        if nonterminals[sym].is_start:
            start_sym = nonterminals[sym]
            break

    start_sym.is_start = False
    new_start_sym = Nonterminal("__start", True, None)
    new_start_sym.productions.append([start_sym])
    nonterminals["__start"] = new_start_sym


# implement the CLOSURE function
def closure(items, terminals):
    has_unprocessed_items = True
    new_items = set()
    # loop until there are no new items
    while has_unprocessed_items:
        has_unprocessed_items = False
        for item in items:
            # dot is not at the end of the production and dot is in front of a nonterminal
            if item.dot < len(item.production) and not item.production[item.dot].is_terminal:
                # for all productions of the said nonterminal...
                for production in item.production[item.dot].productions:
                    # compute FIRST set of the rest of the production, combined with the lookahead symbol
                    for sym in first_syms(item.production[item.dot + 1:len(item.production)]
                                          + [item.lookahead], terminals):
                        # we only want terminals
                        if sym.is_terminal:
                            set_size = len(new_items)
                            new_items.add(Item(item.production[item.dot], production, 0, sym))
                            # check whether the item was actually added to the set
                            if len(new_items) != set_size:
                                has_unprocessed_items = True
        items |= new_items

    return items


# implement the GOTO function
def goto(items, symbol, terminals):
    j = set()
    for item in items:
        # dot is not at the end of the production and dot is in front of a nonterminal
        if item.dot < len(item.production) and item.production[item.dot] == symbol:
            j.add(Item(item.nonterminal, item.production, item.dot + 1, item.lookahead))

    return closure(j, terminals)


# create a collection of sets of LR(1) items
def create_collection(nonterminals, terminals):
    augment_grammar(nonterminals)
    # starting state is a closure of [__start -> * old_start , $] item
    # use frozenset because we need immutable sets if we want to hash them
    start_state = frozenset(closure({Item(nonterminals["__start"], nonterminals["__start"].productions[0], 0,
                                          terminals['$'])},
                                    terminals))
    collection = {start_state}
    has_new_items = True
    new_items = set()
    # loop until there are no new items
    while has_new_items:
        has_new_items = False
        # compute GOTO sets for current items set and all grammar symbols (both terminals and nonterminals)
        # and add them to the collection
        for item_set in collection:
            for sym in nonterminals:
                goto_set = goto(item_set, nonterminals[sym], terminals)
                if len(goto_set) > 0:
                    new_items_size = len(new_items)
                    new_items.add(frozenset(goto_set))
                    # check whether the set was actually added
                    if len(new_items) != new_items_size:
                        has_new_items = True
            for sym in terminals:
                goto_set = goto(item_set, terminals[sym], terminals)
                if len(goto_set) > 0:
                    new_items_size = len(new_items)
                    new_items.add(frozenset(goto_set))
                    # check whether the set was actually added
                    if len(new_items) != new_items_size:
                        has_new_items = True
        collection |= new_items

    #
    collection = list(collection)
    collection.remove(start_state)
    collection.insert(0, start_state)

    return collection


# helper function which prints the whole collection
def print_collection(collection):
    i = 0
    for item_set in collection:
        print("State " + str(i))
        for item in item_set:
            print(item)
        print()
        i += 1
