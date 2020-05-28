# final stage of the parser generator
# generates a pair of .h and .cpp files that represent the specified parser
# since we generate c++ code, grammar symbols and the lexer itself are represented by the eponymous classes
# the core of the generated parser is an LR(1) parsing algorithm, described in [1]
#
# [1] The Dragon Book, 2nd Ed, p. 251


# open the header file and emit necessary class and enum declarations (eg. GrammarSymbol class, ParserStates enum, etc.)
# also emit manifest code, which is provided by the user in the first part of the input file
def create_header_and_emit_manifest(manifest, types, collection, goto_table, action_table, productions):
    with open("my_little_parser.h", 'w') as header:
        # emit header guards and includes
        header.writelines([
            "#ifndef __MY_LITTLE_PARSER_H\n"
            "#define __MY_LITTLE_PARSER_H\n\n"
            "#include <stack>\n"
            "#include <cstring>\n"
            "#include <fstream>\n"
            "#include <list>\n"
            "#include <memory>\n\n"
            "#include \"my_little_lexer.h\"\n\n"
        ])

        # emit manifest code
        header.writelines(manifest)
        header.write("\n\n")

        # emit types union
        header.write("union types {\n")
        # write the terminals lexeme field
        header.write("\tchar* lexeme;\n")
        i = 0
        for type in types:
            header.write("\t" + type + " __" + str(i) + ";\n")
            i += 1
        header.write("};\n\n")

        # emit an enum representing LR(0) automaton states
        header.writelines([
            "// States of the LR(0) automaton\n"
            "enum class ParserStates : uint16_t {\n"
            "\tS0 = 0,\n"
        ])
        for i in range(1, len(collection)):
            header.write("\tS" + str(i) + ",\n")
        header.writelines([
            "\tSE\n"
            "};\n\n"
        ])

        # emit an enum representing nonterminal symbols
        header.writelines([
            "// Enumeration of used nonterminal symbols.\n"
            "enum class Nonterminals : uint8_t {\n"
        ])
        header.write("\t" + goto_table[0][0] + " = 0,\n")
        for nonterminal in goto_table[0][1:len(goto_table[0])]:
            header.write("\t" + nonterminal + ",\n")
        header.write("};\n\n")

        # emit the Parser class
        header.writelines([
            "// Take a stream of tokens from the lexer and check for syntactic correctness\n"
            "// while building a parse tree.\n"
            "class Parser {\n"
            "\t// Stack of LR(0) automaton states.\n"
            "\tstd::stack<ParserStates> states_stack;\n"
            "\t// Current input token.\n"
            "\tstd::shared_ptr<Token> current_input;\n"
            "\t// A stack of nonterminal values, used in the user defined code.\n"
            "\tstd::stack<union types> sym_stack;\n"
            "\t// Lexer which is used for providing the tokens.\n"
            "\tLexer& lexer;\n\n"
            "\tusing ActionTableEntry = std::pair<char, uint8_t>;\n"
            "\tusing FunctionType = void (*)(std::stack<union types>&);\n"
            "\tusing Production = std::tuple<Nonterminals, int, FunctionType>;\n\n"
            "\t// ACTION table.\n"
            "\tstatic ActionTableEntry action_table[" + str(len(collection)) + "][" + str(len(action_table[0])) + "];\n"
            "\t// GOTO table.\n"
            "\tstatic ParserStates goto_table[" + str(len(collection)) + "][" + str(len(goto_table[0])) + "];\n"
            "\t// Table of productions.\n"
            "\tstatic Production productions[" + str(len(productions)) + "];\n"
            "public:\n"
            "\tParser() = delete;\n"
            "\tParser(const Parser&) = delete;\n"
            "\tParser(Parser&&) = delete;\n"
            "\tParser(Lexer& lexer) : lexer(lexer) {}\n"
            "\t~Parser() = default;\n"
            "\tParser& operator=(Parser&) = delete;\n"
            "\tParser& operator=(Parser&&) = delete;\n"
            "\t// Check for syntactic correctness and build a parse tree. This is the\n"
            "\t// heart of the parser. This method implements LR(1) parsing algorithm\n"
            "\t// described in the 'Dragon Book' (2nd edition, p. 241).\n"
            "\tbool parse();\n"
            "\t// Return the value of the start symbol. Should be called after the successful call to parse();\n"
            "\tunion types get_top_value() { return this->sym_stack.top(); }\n"
            "};\n\n"
        ])

        header.write("#endif // __MY_LITTLE_PARSER_H")


# emit user defined code
def emit_code(productions, body):
    i = 0
    head = productions[0][0]
    # for each production of a nonterminal, extract the code from the nonterminal object
    for production in productions:
        if production[0] != head:
            head = production[0]
            i = 0
        code = head.code[i]

        # if this is a nontrivial production and there is no user provided code, let it be
        if code == '' and len(production[1]) > 1:
            i += 1
            continue

        body.writelines([
            "void " + head.name + "__" + str(i) + "(std::stack<union types>& sym_stack) {\n"
                                                  "\tunion types param__head;\n"
        ])

        # prepare the parameters
        param_num = len(production[1]) - 1
        for sym in production[1]:
            body.writelines([
                "\tunion types param__" + str(param_num) + "{sym_stack.top()};\n"
                                                           "\tsym_stack.pop();\n"
            ])
            param_num -= 1
        body.write("\n")

        # replace the placeholder parameters with the real ones
        code = code.replace("$$", "param__head.__" + str(head.type))
        for j in range(len(production[1])):
            param = "param__" + str(j) + '.'
            sym = production[1][j]
            if sym.is_terminal:
                param += "lexeme"
            else:
                param += "__" + str(sym.type)

            code = code.replace('$' + str(j), param)

        # write the code itself
        if code != '':
            code = "\t" + code + "\n\n"
            body.write(code)
        # if this is a trivial production and there is no user provided code, emit the default expression
        else:
            body.write("\tparam__head = param__0;\n\n")

        # free the memory which holds the lexeme of popped terminals
        param_num = len(production[1]) - 1
        for sym in production[1]:
            if sym.is_terminal:
                body.write("\tdelete[](param__" + str(param_num) + ".lexeme);\n")
            param_num -= 1
        body.write("\n")

        # push the result onto the stack
        body.writelines([
            "\tsym_stack.push(param__head);\n"
            "}\n\n"
        ])

        i += 1


# open the source file and emit class method definitions
def create_body(action_table, goto_table, productions):
    with open("my_little_parser.cpp", 'w') as body:
        # emit includes
        body.write("#include \"my_little_parser.h\"\n\n")

        emit_code(productions, body)

        # emit action table
        body.writelines([
            "// ACTION table.\n"
            "Parser::ActionTableEntry Parser::action_table[][" + str(len(action_table[0])) + "] = {\n"
        ])
        for row in action_table[1:len(action_table)]:
            line = "\t{"
            for field in row:
                if field is None:
                    line += "Parser::ActionTableEntry('e', 0), "
                elif field == 'a':
                    line += "Parser::ActionTableEntry('a', 0), "
                else:
                    line += "Parser::ActionTableEntry(\'" + field[0] + "\', " + str(field[1]) + "), "
            line += "},\n"
            body.write(line)
        body.write("};\n\n")

        # emit GOTO table
        body.writelines([
            "// GOTO table.\n"
            "ParserStates Parser::goto_table[][" + str(len(goto_table[0])) + "] = {\n"
        ])
        for row in goto_table[1:len(goto_table)]:
            line = "\t{"
            for field in row:
                if field is None:
                    line += "ParserStates::SE, "
                else:
                    line += "ParserStates::S" + str(field) + ", "
            line += "},\n"
            body.write(line)
        body.write("};\n\n")

        # emit productions table
        body.writelines([
            "// Table of productions.\n"
            "Parser::Production Parser::productions[] = {\n"
        ])
        i = 0
        head = productions[0][0]
        for production in productions:
            line = "\tstd::make_tuple(Nonterminals::" + production[0].name + ", " \
                   + str(len(production[1])) + ", "

            if production[0] != head:
                head = production[0]
                i = 0
            code = head.code[i]

            if code == '' and len(production[1]) > 1:
                line += "nullptr), \n"
            else:
                line += head.name + "__" + str(i) + "), \n"
            body.write(line)

            i += 1

        body.write("};\n\n")

        # emit the parser body
        body.writelines([
            "bool Parser::parse() {\n"
            "\t// Get the first token from the lexer and initialize the states stack,\n"
            "\t// as well as the parse tree.\n"
            "\tthis->current_input = this->lexer.get_next_word();\n"
            "\tthis->states_stack.push(ParserStates::S0);\n\n"
            "\twhile (true) {\n"
            "\t\tTokenType token_type{this->current_input->get_token_type()};\n"
            "\t\tActionTableEntry action = this->action_table[static_cast<uint8_t>(this->states_stack.top())]\n"
            "\t\t\t\t\t\t\t\t\t\t\t\t\t[static_cast<uint16_t>(token_type)];\n\n"
            "\t\t// Shift action.\n"
            "\t\tif (action.first == 's') {\n"
            "\t\t\t// Push the token lexeme to the symbol stack.\n"
            "\t\t\tunion types term;\n"
            "\t\t\tterm.lexeme = new char[this->current_input->get_lexeme().size() + 1];\n"
            "\t\t\tstrcpy(term.lexeme, this->current_input->get_lexeme().c_str());\n"
            "\t\t\tthis->sym_stack.push(term);\n\n"
            "\t\t\t// Get the next input symbol and add it to the parse tree frontier.\n"
            "\t\t\tthis->current_input = this->lexer.get_next_word();\n"
            "\t\t\tthis->states_stack.push(static_cast<ParserStates>(action.second));\n"
            "\t\t// Reduce action.\n"
            "\t\t} else if (action.first == 'r') {\n"
            "\t\t\tProduction prod{this->productions[action.second]};\n\n"
            "\t\t\t// Pop the states off the stack. \n"
            "\t\t\tfor (uint8_t i = 0; i < std::get<1>(prod); i++) {\n"
            "\t\t\t\tthis->states_stack.pop();\n"
            "\t\t\t}\n"
            "\t\t\tthis->states_stack.push(this->goto_table[static_cast<uint8_t>(this->states_stack.top())]\n"
            "\t\t\t\t\t\t\t\t\t\t\t\t\t[static_cast<uint8_t>(std::get<0>(prod))]);\n"
            "\t\t\t// Call the user defined code.\n"
            "\t\t\tif (std::get<2>(prod) != nullptr) {\n"
            "\t\t\t\tFunctionType func{std::get<2>(prod)};\n"
            "\t\t\t\tfunc(this->sym_stack);\n"
            "\t\t\t}\n"
            "\t\t// Accept action. This ends the parsing process successfully.\n"
            "\t\t} else if (action.first == 'a') {\n"
            "\t\t\treturn true;\n"
            "\t\t// Error action. This ends the parsing process unsuccessfully.\n"
            "\t\t} else {\n"
            "\t\t\treturn false;\n"
            "\t\t}\n"
            "\t}\n"
            "}\n"
        ])
