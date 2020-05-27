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
        if not line or "_types:" in line:
            file.seek(file_pos)
            break
        manifest_code += line

    return manifest_code, line_num


# collect the union of user defined types
def collect_types(file, line_num):
    types = file.readline()
    line_num += 1

    types = types.strip()
    if types != "_types:":
        report_error("_types: label not found!", line_num)

    types_collection = []
    while True:
        file_pos = file.tell()
        line = file.readline().strip()
        line_num += 1
        i = 0
        if not line or "_tokens:" in line:
            file.seek(file_pos)
            break
        types_collection.append(line)

    return types_collection, line_num


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


# extract the value type of the nonterminal
def extract_type(line, line_num, types):
    if line.count("%{") > 1:
        report_error("Ill-formed production", line_num)
    elif line.count("%{") == 0:
        return -1, line
    ocparr_index = line.index("%{")

    if line.count("}%") > 1:
        report_error("Ill-formed production", line_num)
    ccparr_index = line.index("}%")

    if ccparr_index < ocparr_index:
        report_error("Ill-formed production!", line_num)

    if ocparr_index > line.index("::="):
        report_error("Ill-formed production!", line_num)

    type = line[ocparr_index + 2:ccparr_index].strip()
    if types.count(type) == 0:
        report_error("Unspecified type!", line_num)

    line = line[ccparr_index + 2:len(line)]

    return types.index(type), line


# extract the user defined code which should be executed when the reduction is done
def extract_code(line, line_num):
    if line.count("#{") > 1:
        report_error("Ill-formed production", line_num)
    elif line.count("#{") == 0:
        return '', line
    ocparr_index = line.index("#{")

    if line.count("}#") > 1:
        report_error("Ill-formed production", line_num)
    ccparr_index = line.index("}#")

    if ccparr_index < ocparr_index:
        report_error("Ill-formed production!", line_num)

    if ocparr_index < line.index("::="):
        report_error("Ill-formed production!", line_num)

    code = line[ocparr_index + 2:ccparr_index].strip()
    line = line[0:ocparr_index]

    return code, line


# parse the productions
def collect_productions(file, line_num, types, terminals, nonterminals, terminals_list):
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
            (type, line) = extract_type(line, line_num, types)
            (code, line) = extract_code(line, line_num)
            [current_head, body] = [a.strip() for a in line.split("::=")]
            process_production(current_head, body, type, code, terminals, nonterminals, terminals_list)
        elif line.startswith('|') and line.count('|') == 1 and line.count("%{") == 0 and current_head is not None:
            (code, line) = extract_code(line, line_num)
            body = line.strip('|')[1].strip()
            process_production(current_head, body, None, code, terminals, nonterminals, terminals_list)
        else:
            report_error("Ill-formed production!", line_num)


def do_the_magic(manifest_code, types, terminals, nonterminals, terminals_list):
    collection = create_collection(nonterminals, terminals)

    (action_table, goto_table, productions) = create_tables(collection, nonterminals, terminals, terminals_list)
    create_header_and_emit_manifest(manifest_code, types, collection, goto_table, action_table, productions)
    create_body(action_table, goto_table, productions)


if __name__ == "__main__":
    #if len(sys.argv) != 2:
    #    report_error("Incorrect number of command line arguments! Should be only the input file name!", 0)

    filename = "example2.mlg"
    if ".mlg" not in filename:
        report_error("Input file name should have .mll extension!", 0)

    with open(filename, 'r') as file:
        line_num = 0

        terminals = {"eps": Terminal("eps"), "$": Terminal("$")}
        nonterminals = dict()

        # collect the manifest code
        (manifest_code, line_num) = collect_manifest_code(file, line_num)

        # collect the types union
        (types, line_num) = collect_types(file, line_num)

        # collect token definitions
        (terminals_list, line_num) = collect_tokens(file, line_num)

        # process the grammar productions
        collect_productions(file, line_num, types, terminals, nonterminals, terminals_list)

        # create ACTION and GOTO table and emit parser code
        do_the_magic(manifest_code, types, terminals, nonterminals, terminals_list)