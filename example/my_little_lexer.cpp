#include <type_traits>
#include "my_little_lexer.h"

// << operator overload for the Token class
std::ostream& operator<<(std::ostream& os, const Token& tok) {
	os << "Token type: " << static_cast<uint16_t>(tok.get_token_type()) << std::endl;
	os << "Lexeme: " << tok.get_lexeme() << std::endl;
	os << "Line: " << tok.get_line() << std::endl;
	if (tok.get_token_type() == TokenType::LAST)
		os << "Last" << std::endl;

	return os;
}

void ws__(std::shared_ptr<Token> token)
{ token->set_token_type(TokenType::WS); token->set_ignore(true); }

void num__(std::shared_ptr<Token> token)
{ token->set_token_type(TokenType::NUM); }

void plus__(std::shared_ptr<Token> token)
{ token->set_token_type(TokenType::PLUS); }

void mult__(std::shared_ptr<Token> token)
{ token->set_token_type(TokenType::MULT); }

void opar__(std::shared_ptr<Token> token)
{ token->set_token_type(TokenType::OPAR); }

void cpar__(std::shared_ptr<Token> token)
{ token->set_token_type(TokenType::CPAR); }

void div__(std::shared_ptr<Token> token)
{ token->set_token_type(TokenType::DIV); }

void sub__(std::shared_ptr<Token> token)
{ token->set_token_type(TokenType::SUB); }

// Whether the provided state is an accepting state.
constexpr bool Lexer::is_accepting_state(States s) {
	return (false
			|| s == States::S1
			|| s == States::S2
			|| s == States::S3
			|| s == States::S4
			|| s == States::S5
			|| s == States::S6
			|| s == States::S7
			|| s == States::S8
			|| s == States::S9
			|| s == States::S10
			|| s == States::S11
			|| s == States::S12
			|| s == States::S13
			|| s == States::S14
			|| s == States::S15
			|| s == States::S16
			|| s == States::S17
			|| s == States::S18
			|| s == States::S19
			|| s == States::S20
			|| s == States::S21
			|| s == States::S22
			|| s == States::S23
			|| s == States::S24
			|| s == States::S25
			|| s == States::S26
			);
}

std::shared_ptr<Token> Lexer::get_next_word() {
	std::shared_ptr<Token> tok;
	while((tok = this->next_word())->is_ignore());
	return tok;
}

std::shared_ptr<Token> Lexer::next_word() {
Init:
	static int16_t line{1};
	std::string lexeme{};
	char c;
	this->state = States::S0;

	while (!this->states_stack.empty())
		this->states_stack.pop();
	this->states_stack.push(States::BAD);

S0:
	this->state = States::S0;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case '+':
		goto S1;
	case '*':
		goto S2;
	case '(':
		goto S3;
	case ')':
		goto S4;
	case '/':
		goto S5;
	case '-':
		goto S6;
	case '9':
		goto S7;
	case '8':
		goto S8;
	case '7':
		goto S9;
	case '6':
		goto S10;
	case '5':
		goto S11;
	case '4':
		goto S12;
	case '3':
		goto S13;
	case '1':
		goto S14;
	case '2':
		goto S15;
	case ' ':
		goto S16;
	case '\n':
		goto S17;
	default:
		this->state = States::SE;
		goto SOut;
	}

S1:
	this->state = States::S1;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	default:
		this->state = States::SE;
		goto SOut;
	}

S2:
	this->state = States::S2;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	default:
		this->state = States::SE;
		goto SOut;
	}

S3:
	this->state = States::S3;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	default:
		this->state = States::SE;
		goto SOut;
	}

S4:
	this->state = States::S4;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	default:
		this->state = States::SE;
		goto SOut;
	}

S5:
	this->state = States::S5;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	default:
		this->state = States::SE;
		goto SOut;
	}

S6:
	this->state = States::S6;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	default:
		this->state = States::SE;
		goto SOut;
	}

S7:
	this->state = States::S7;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case '1':
		goto S18;
	case '2':
		goto S19;
	case '3':
		goto S20;
	case '4':
		goto S21;
	case '5':
		goto S22;
	case '6':
		goto S23;
	case '7':
		goto S24;
	case '8':
		goto S25;
	case '9':
		goto S26;
	default:
		this->state = States::SE;
		goto SOut;
	}

S8:
	this->state = States::S8;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case '1':
		goto S18;
	case '2':
		goto S19;
	case '3':
		goto S20;
	case '4':
		goto S21;
	case '5':
		goto S22;
	case '6':
		goto S23;
	case '7':
		goto S24;
	case '8':
		goto S25;
	case '9':
		goto S26;
	default:
		this->state = States::SE;
		goto SOut;
	}

S9:
	this->state = States::S9;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case '1':
		goto S18;
	case '2':
		goto S19;
	case '3':
		goto S20;
	case '4':
		goto S21;
	case '5':
		goto S22;
	case '6':
		goto S23;
	case '7':
		goto S24;
	case '8':
		goto S25;
	case '9':
		goto S26;
	default:
		this->state = States::SE;
		goto SOut;
	}

S10:
	this->state = States::S10;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case '1':
		goto S18;
	case '2':
		goto S19;
	case '3':
		goto S20;
	case '4':
		goto S21;
	case '5':
		goto S22;
	case '6':
		goto S23;
	case '7':
		goto S24;
	case '8':
		goto S25;
	case '9':
		goto S26;
	default:
		this->state = States::SE;
		goto SOut;
	}

S11:
	this->state = States::S11;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case '1':
		goto S18;
	case '2':
		goto S19;
	case '3':
		goto S20;
	case '4':
		goto S21;
	case '5':
		goto S22;
	case '6':
		goto S23;
	case '7':
		goto S24;
	case '8':
		goto S25;
	case '9':
		goto S26;
	default:
		this->state = States::SE;
		goto SOut;
	}

S12:
	this->state = States::S12;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case '1':
		goto S18;
	case '2':
		goto S19;
	case '3':
		goto S20;
	case '4':
		goto S21;
	case '5':
		goto S22;
	case '6':
		goto S23;
	case '7':
		goto S24;
	case '8':
		goto S25;
	case '9':
		goto S26;
	default:
		this->state = States::SE;
		goto SOut;
	}

S13:
	this->state = States::S13;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case '1':
		goto S18;
	case '2':
		goto S19;
	case '3':
		goto S20;
	case '4':
		goto S21;
	case '5':
		goto S22;
	case '6':
		goto S23;
	case '7':
		goto S24;
	case '8':
		goto S25;
	case '9':
		goto S26;
	default:
		this->state = States::SE;
		goto SOut;
	}

S14:
	this->state = States::S14;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case '1':
		goto S18;
	case '2':
		goto S19;
	case '3':
		goto S20;
	case '4':
		goto S21;
	case '5':
		goto S22;
	case '6':
		goto S23;
	case '7':
		goto S24;
	case '8':
		goto S25;
	case '9':
		goto S26;
	default:
		this->state = States::SE;
		goto SOut;
	}

S15:
	this->state = States::S15;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case '1':
		goto S18;
	case '2':
		goto S19;
	case '3':
		goto S20;
	case '4':
		goto S21;
	case '5':
		goto S22;
	case '6':
		goto S23;
	case '7':
		goto S24;
	case '8':
		goto S25;
	case '9':
		goto S26;
	default:
		this->state = States::SE;
		goto SOut;
	}

S16:
	this->state = States::S16;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case ' ':
		goto S16;
	case '\n':
		goto S17;
	default:
		this->state = States::SE;
		goto SOut;
	}

S17:
	this->state = States::S17;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case ' ':
		goto S16;
	case '\n':
		goto S17;
	default:
		this->state = States::SE;
		goto SOut;
	}

S18:
	this->state = States::S18;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case '1':
		goto S18;
	case '2':
		goto S19;
	case '3':
		goto S20;
	case '4':
		goto S21;
	case '5':
		goto S22;
	case '6':
		goto S23;
	case '7':
		goto S24;
	case '8':
		goto S25;
	case '9':
		goto S26;
	default:
		this->state = States::SE;
		goto SOut;
	}

S19:
	this->state = States::S19;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case '1':
		goto S18;
	case '2':
		goto S19;
	case '3':
		goto S20;
	case '4':
		goto S21;
	case '5':
		goto S22;
	case '6':
		goto S23;
	case '7':
		goto S24;
	case '8':
		goto S25;
	case '9':
		goto S26;
	default:
		this->state = States::SE;
		goto SOut;
	}

S20:
	this->state = States::S20;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case '1':
		goto S18;
	case '2':
		goto S19;
	case '3':
		goto S20;
	case '4':
		goto S21;
	case '5':
		goto S22;
	case '6':
		goto S23;
	case '7':
		goto S24;
	case '8':
		goto S25;
	case '9':
		goto S26;
	default:
		this->state = States::SE;
		goto SOut;
	}

S21:
	this->state = States::S21;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case '1':
		goto S18;
	case '2':
		goto S19;
	case '3':
		goto S20;
	case '4':
		goto S21;
	case '5':
		goto S22;
	case '6':
		goto S23;
	case '7':
		goto S24;
	case '8':
		goto S25;
	case '9':
		goto S26;
	default:
		this->state = States::SE;
		goto SOut;
	}

S22:
	this->state = States::S22;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case '1':
		goto S18;
	case '2':
		goto S19;
	case '3':
		goto S20;
	case '4':
		goto S21;
	case '5':
		goto S22;
	case '6':
		goto S23;
	case '7':
		goto S24;
	case '8':
		goto S25;
	case '9':
		goto S26;
	default:
		this->state = States::SE;
		goto SOut;
	}

S23:
	this->state = States::S23;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case '1':
		goto S18;
	case '2':
		goto S19;
	case '3':
		goto S20;
	case '4':
		goto S21;
	case '5':
		goto S22;
	case '6':
		goto S23;
	case '7':
		goto S24;
	case '8':
		goto S25;
	case '9':
		goto S26;
	default:
		this->state = States::SE;
		goto SOut;
	}

S24:
	this->state = States::S24;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case '1':
		goto S18;
	case '2':
		goto S19;
	case '3':
		goto S20;
	case '4':
		goto S21;
	case '5':
		goto S22;
	case '6':
		goto S23;
	case '7':
		goto S24;
	case '8':
		goto S25;
	case '9':
		goto S26;
	default:
		this->state = States::SE;
		goto SOut;
	}

S25:
	this->state = States::S25;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case '1':
		goto S18;
	case '2':
		goto S19;
	case '3':
		goto S20;
	case '4':
		goto S21;
	case '5':
		goto S22;
	case '6':
		goto S23;
	case '7':
		goto S24;
	case '8':
		goto S25;
	case '9':
		goto S26;
	default:
		this->state = States::SE;
		goto SOut;
	}

S26:
	this->state = States::S26;

	c = this->next_char();
	if (this->is_newline(c))
		line++;

	lexeme.push_back(c);

	if (this->is_accepting_state(this->state))
		while (!this->states_stack.empty())
			this->states_stack.pop();
	this->states_stack.push(this->state);

	switch (c) {
	case '1':
		goto S18;
	case '2':
		goto S19;
	case '3':
		goto S20;
	case '4':
		goto S21;
	case '5':
		goto S22;
	case '6':
		goto S23;
	case '7':
		goto S24;
	case '8':
		goto S25;
	case '9':
		goto S26;
	default:
		this->state = States::SE;
		goto SOut;
	}

SOut:
	while (!this->is_accepting_state(this->state) && this->state != States::BAD) {
		this->state = this->states_stack.top();
		this->states_stack.pop();

		if (this->is_newline(lexeme.back()))
			line--;

		if (!lexeme.empty())
			lexeme.pop_back();
		this->rollback();
	}

	std::shared_ptr<Token> tok{std::make_shared<Token>(lexeme, TokenType::DEFAULT, line, false)};
	if (this->is_accepting_state(this->state)) {
		switch(this->state) {
		case States::S16:
			ws__(tok);
			break;
		case States::S17:
			ws__(tok);
			break;
		case States::S7:
			num__(tok);
			break;
		case States::S8:
			num__(tok);
			break;
		case States::S9:
			num__(tok);
			break;
		case States::S10:
			num__(tok);
			break;
		case States::S11:
			num__(tok);
			break;
		case States::S12:
			num__(tok);
			break;
		case States::S13:
			num__(tok);
			break;
		case States::S14:
			num__(tok);
			break;
		case States::S15:
			num__(tok);
			break;
		case States::S18:
			num__(tok);
			break;
		case States::S19:
			num__(tok);
			break;
		case States::S20:
			num__(tok);
			break;
		case States::S21:
			num__(tok);
			break;
		case States::S22:
			num__(tok);
			break;
		case States::S23:
			num__(tok);
			break;
		case States::S24:
			num__(tok);
			break;
		case States::S25:
			num__(tok);
			break;
		case States::S26:
			num__(tok);
			break;
		case States::S1:
			plus__(tok);
			break;
		case States::S2:
			mult__(tok);
			break;
		case States::S3:
			opar__(tok);
			break;
		case States::S4:
			cpar__(tok);
			break;
		case States::S5:
			div__(tok);
			break;
		case States::S6:
			sub__(tok);
			break;
		}
	}
	else if (c == std::char_traits<char>::eof())
		tok->set_token_type(TokenType::LAST);
	else
		tok->set_token_type(TokenType::ERROR);

	return tok;
}

