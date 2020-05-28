#include <iostream>

#include "my_little_parser.h"

int main() {
    Lexer lex("example.txt");
    Parser parser(lex);

    if (parser.parse()) {
        std::cout << "Successful!" << std::endl;
        std::cout << parser.get_top_value().__0 << std::endl;
    } else
        std::cout << "Failed!" << std::endl;

    return 0;
}