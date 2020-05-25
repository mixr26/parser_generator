# final stage of the parser generator
# generates a pair of .h and .cpp files that represent the specified parser
# since we generate c++ code, grammar symbols and the lexer itself are represented by the eponymous classes
# the core of the generated parser is an LR(1) parsing algorithm, described in [1]
#
# [1] The Dragon Book, 2nd Ed, p. 251

# open the header file and emit necessary class and enum declarations (eg. GrammarSymbol class, ParserStates enum, etc.)
# also emit manifest code, which is provided by the user in the first part of the input file
def create_header_and_emit_manifest(manifest, collection, goto_table, action_table, productions):
    with open("my_little_parser.h", 'w') as header:
        # emit header guards and includes
        header.writelines([
            "#ifndef __MY_LITTLE_PARSER_H\n"
            "#define __MY_LITTLE_PARSER_H\n\n"
            "#include <stack>\n"
            "#include <fstream>\n"
            "#include <list>\n"
            "#include <memory>\n\n"
            "#include \"my_little_lexer.h\"\n\n"
        ])

        # emit manifest code
        header.writelines(manifest)

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

        # emit the GrammarSymbol class
        header.writelines([
            "// Represents one grammar symbol.\n"
            "class GrammarSymbol {\n"
            "public:\n"
            "\tvirtual bool is_terminal() = 0;\n"
            "};\n\n"
        ])

        # emit the Nonterminal class
        header.writelines([
            "// Represents one nonterminal symbol.\n"
            "class Nonterminal : public GrammarSymbol {\n"
            "public:\n"
            "\tusing Children = std::list<std::shared_ptr<GrammarSymbol>>;\n"
            "private:\n"
            "\tNonterminals type;\n"
            "\t// During construction of a parse tree, this holds the children of the\n"
            "\t// nonterminal node.\n"
            "\tChildren production;\n"
            "public:\n"
            "\tNonterminal(Nonterminals type) : type(type) {}\n\n"
            "\tbool is_terminal() { return false; }\n"
            "\tNonterminals get_type() { return this->type; }\n"
            "\tChildren& get_production() { return this->production; }\n"
            "};\n\n"
        ])

        # emit the Terminal class
        header.writelines([
            "// Represents one terminal symbol.\n"
            "class Terminal : public GrammarSymbol {\n"
            "\tTokenType type;\n"
            "public:\n"
            "\tTerminal(TokenType type) : type(type) {}\n\n"
            "\tbool is_terminal() { return true; }\n"
            "\tTokenType get_type() { return this->type; }\n"
            "};\n\n"
        ])

        # emit the Parser class
        header.writelines([
            "// Take a stream of tokens from the lexer and check for syntactic correctness\n"
            "// while building a parse tree.\n"
            "class Parser {\n"
            "\t// Holds the frontier of the parse tree. At the end of the parse, it should\n"
            "\t// contain just the root of the parse tree.\n"
            "\tstd::stack<std::shared_ptr<GrammarSymbol>> parse_tree;\n"
            "\t// Stack of LR(0) automaton states.\n"
            "\tstd::stack<ParserStates> states_stack;\n"
            "\t// Current input token.\n"
            "\tstd::shared_ptr<Token> current_input;\n"
            "\t// Lexer which is used for providing the tokens.\n"
            "\tLexer& lexer;\n\n"
            "\tusing ActionTableEntry = std::pair<char, uint8_t>;\n"
            "\tusing Production = std::pair<Nonterminals, int>;\n\n"
            "\t// ACTION table.\n"
            "\tstatic ActionTableEntry action_table[" + str(len(collection)) + "][" + str(len(action_table[0])) + "];\n"
                                                                                                                  "\t// GOTO table.\n"
                                                                                                                  "\tstatic ParserStates goto_table[" + str(
                len(collection)) + "][" + str(len(goto_table[0])) + "];\n"
                                                                    "\t// Table of productions.\n"
                                                                    "\tstatic Production productions[" + str(
                len(productions)) + "];\n"
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
                                    "};\n\n"
        ])

        header.write("#endif // __MY_LITTLE_PARSER_H")


# open the source file and emit class method definitions
def create_body(action_table, goto_table, productions):
    with open("my_little_parser.cpp", 'w') as body:
        # emit includes
        body.write("#include \"my_little_parser.h\"\n\n")

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
        for production in productions:
            body.write("\tParser::Production(Nonterminals::" + production[0].name + ", "
                       + str(len(production[1])) + "),\n")
        body.write("};\n\n")

        # emit the parser body
        body.writelines([
            "bool Parser::parse() {\n"
            "\t// Get the first token from the lexer and initialize the states stack,\n"
            "\t// as well as the parse tree.\n"
            "\tthis->current_input = this->lexer.get_next_word();\n"
            "\tthis->states_stack.push(ParserStates::S0);\n"
            "\tif (this->current_input->get_token_type() != TokenType::LAST)\n"
            "\t\tthis->parse_tree.push(std::make_shared<Terminal>(this->current_input->get_token_type()));\n\n"
            "\twhile (true) {\n"
            "\t\tTokenType token_type = this->current_input->get_token_type();\n"
            "\t\tActionTableEntry action = this->action_table[static_cast<uint8_t>(this->states_stack.top())]\n"
            "\t\t\t\t\t\t\t\t\t\t\t\t\t[static_cast<uint16_t>(token_type)];\n\n"
            "\t\t// Shift action.\n"
            "\t\tif (action.first == 's') {\n"
            "\t\t\t// Get the next input symbol and add it to the parse tree frontier.\n"
            "\t\t\tthis->current_input = this->lexer.get_next_word();\n"
            "\t\t\tthis->states_stack.push(static_cast<ParserStates>(action.second));\n"
            "\t\t\tif (this->current_input->get_token_type() != TokenType::LAST)\n"
            "\t\t\t\tthis->parse_tree.push(std::make_shared<Terminal>(this->current_input->get_token_type()));\n"
            "\t\t// Reduce action.\n"
            "\t\t} else if (action.first == 'r') {\n"
            "\t\t\tProduction prod = this->productions[action.second];\n\n"
            "\t\t\t// Create a new nonterminal symbol and populate its list of children\n"
            "\t\t\t// with the predefined number of parse tree frontier symbols.\n"
            "\t\t\tstd::shared_ptr<Nonterminal> head = std::make_shared<Nonterminal>(prod.first);\n"
            "\t\t\tNonterminal::Children& prod_list = head->get_production();\n"
            "\t\t\tfor (uint8_t i = 0; i < prod.second; i++) {\n"
            "\t\t\t\tthis->states_stack.pop();\n"
            "\t\t\t\tprod_list.push_front(this->parse_tree.top());\n"
            "\t\t\t\tthis->parse_tree.pop();\n"
            "\t\t\t}\n"
            "\t\t\tthis->parse_tree.push(head);\n\n"
            "\t\t\tthis->states_stack.push(this->goto_table[static_cast<uint8_t>(this->states_stack.top())]\n"
            "\t\t\t\t\t\t\t\t\t\t\t\t\t[static_cast<uint8_t>(prod.first)]);\n"
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
