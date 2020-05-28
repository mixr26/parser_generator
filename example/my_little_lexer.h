#ifndef __MY_LITTLE_LEXER_H
#define __MY_LITTLE_LEXER_H

#include <string>
#include <fstream>
#include <iostream>
#include <stack>
#include <memory>
#include <functional>
#include <cstdint>

enum class TokenType : uint16_t {
	NUM = 0,
	MULT = 1,
	PLUS = 2,
	DIV = 3,
	SUB = 4,
	OPAR = 5,
	CPAR = 6,
	WS = 7,
	LAST = 8,
	ERROR = 9,
	DEFAULT = 10
};


// Token class, which represents one lexeme of the input file.
class Token {
	TokenType token_type;
	std::string lexeme;
	// Line in input file which contains this lexeme. Currently only used for
	// error reporting.
	int16_t line;
	// Whether this token should be ignored.
	bool ignore;
public:
	Token() = delete;
	Token(std::string lexeme = "", TokenType token_type = TokenType::DEFAULT, int16_t line = 0, bool ignore = false)
 		: lexeme(lexeme), token_type(token_type), line(line), ignore(ignore) {}

	void set_token_type(TokenType token_type) { this->token_type = token_type; }
	void set_ignore(bool ignore) { this->ignore = ignore; }
	void set_lexeme(std::string lexeme) { this->lexeme = lexeme; }

	const std::string& get_lexeme() const { return this->lexeme; }
	TokenType get_token_type() const { return this->token_type; }
	bool is_ignore() const { return this->ignore; }
	int16_t get_line() const { return this->line; }
};

// << operator overload for the Token class
std::ostream& operator<<(std::ostream& os, const Token& tok);

// States of the lexer DFA.
enum class States : uint32_t {
	S0 = 0,
	S1,
	S2,
	S3,
	S4,
	S5,
	S6,
	S7,
	S8,
	S9,
	S10,
	S11,
	S12,
	S13,
	S14,
	S15,
	S16,
	S17,
	S18,
	S19,
	S20,
	S21,
	S22,
	S23,
	S24,
	S25,
	S26,
	SE,
	BAD
};

// Takes a stream of characters from the input file and tokenizes them
// into a stream of lexemes.

class Lexer {
	static uint32_t token_class;
	static bool is_last_token;
	// Input file.
	std::ifstream filestream;
	// Current DFA state.
	States state;
	// A stack of states used for backtracking.
	std::stack<States> states_stack;
	// Return the next character of the input file.
	char next_char() { return static_cast<char>(this->filestream.get()); }
	// Roll back the filestream one character.
	void rollback() { this->filestream.seekg(-1, std::ios_base::cur); }

	// Whether the provided state is an accepting state.
	static constexpr bool is_accepting_state(States);
	// Whether the provided character is newline.
	static constexpr bool is_newline(char c) { return c == 10 || c == 13; }
	// Try to tokenize next word from the input file. This is the heart of the
	// lexer. This method implements a table-driven, direct-coded scanning algorithm
	// described in 'Engineering a Compiler' by Cooper and Torczon (2nd edition, p. 60).
	std::shared_ptr<Token> next_word();
public:
	Lexer() = delete;
	Lexer(const Lexer&) = delete;
	Lexer(Lexer&&) = delete;
	Lexer(const char* input_file) { 
		this->filestream.open(input_file);
		if (!this->filestream.is_open()) {
			std::cout << "Input file not opened correctly!" << std::endl;
			exit(1);
		}
	}
	~Lexer() { this->filestream.close(); }
	Lexer& operator=(Lexer&) = delete;
	Lexer& operator=(Lexer&&) = delete;
	std::shared_ptr<Token> get_next_word();
};

#endif //__MY_LITTLE_LEXER_H