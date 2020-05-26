import sys
from emit_parser import create_header_and_emit_manifest, create_body
from lr1_collection import create_collection
from lr1_tables import create_tables
from process_production import process_production, Terminal


# error reporting helper routine
def report_error(error, line_num):
    print("Line " + str(line_num) + ": ")
    print(error)
    exit(1)


# parse the manifest part of the input file
def collect_manifest_code(file, line_num):
    manifest = file.readline()
    line_num += 1

    manifest = manifest.strip()
    manifest_code = ''
    if manifest != "_manifest:":
        report_error("_manifest: label not found!", line_num)

    while True:
        file_pos = file.tell()
        line = file.readline()
        line_num += 1
        if not line or "_tokens:" in line:
            file.seek(file_pos)
            break
        manifest_code += line

    return manifest_code, line_num


# parse the token definitions
def collect_tokens(file, line_num):
    tokens = file.readline().strip()
    line_num += 1
    if tokens != "_tokens:":
        report_error("_tokens: label not found!", line_num)

    token_list = []
    while True:
        file_pos = file.tell()
        line = file.readline()
        line_num += 1
        if not line or "_grammar:" in line:
            file.seek(file_pos)
            break

        token_list.append(line.strip())

    token_list.append('$')

    return token_list, line_num


# parse the productions
def collect_productions(file, line_num, terminals, nonterminals, terminals_list):
    grammar = file.readline().strip()
    line_num += 1
    if grammar != "_grammar:":
        report_error("_grammar: label not found!", line_num)

    current_head = None
    while True:
        file_pos = file.tell()
        line = file.readline()
        line_num += 1
        if not line:
            file.seek(file_pos)
            break

        line = line.strip()
        # blank line
        if line == '':
            continue

        if line.count("::=") == 1:
            [current_head, body] = [a.strip() for a in line.split("::=")]
            process_production(current_head, body, terminals, nonterminals, terminals_list)
        elif line.startswith('|') and line.count('|') == 1 and current_head is not None:
            body = line.strip('|')[1].strip()
            process_production(current_head, body, terminals, nonterminals, terminals_list)
        else:
            report_error("Incorrect production!")


def do_the_magic(manifest_code, terminals, nonterminals, terminals_list):
    collection = create_collection(nonterminals, terminals)

    (action_table, goto_table, productions) = create_tables(collection, nonterminals, terminals, terminals_list)
    create_header_and_emit_manifest(manifest_code, collection, goto_table, action_table, productions)
    create_body(action_table, goto_table, productions)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        report_error("Incorrect number of command line arguments! Should be only the input file name!", 0)

    filename = sys.argv[1]
    if ".mlg" not in filename:
        report_error("Input file name should have .mll extension!", 0)

    with open(filename, 'r') as file:
        line_num = 0

        terminals = {"eps": Terminal("eps"), "$": Terminal("$")}
        nonterminals = dict()

        # collect the manifest code
        (manifest_code, line_num) = collect_manifest_code(file, line_num)

        # collect token definitions
        (terminals_list, line_num) = collect_tokens(file, line_num)

        # process the grammar productions
        collect_productions(file, line_num, terminals, nonterminals, terminals_list)

        # create ACTION and GOTO table and emit parser code
        do_the_magic(manifest_code, terminals, nonterminals, terminals_list)