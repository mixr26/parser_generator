_manifest:
_tokens:
	NUM
	MULT
	PLUS
	DIV
	SUB
	OPAR
	CPAR
	WS
_defines:
	whitespace     %{ |\n}%
    digit          %{[1-9]}%
    number         %{{digit}{digit}*}%
_patterns:
	ws             %{{whitespace}*}%                #{ token->set_token_type(WS); token->set_ignore(true); }#
    num            %{{number}}%                     #{ token->set_token_type(NUM); }#
    plus 		   %{+}%							#{ token->set_token_type(PLUS); }#
    mult 		   %{\*}%							#{ token->set_token_type(MULT); }#
    opar 		   %{\(}%							#{ token->set_token_type(OPAR); }#
    cpar 		   %{\)}%							#{ token->set_token_type(CPAR); }#
    div 		   %{/}%							#{ token->set_token_type(DIV); }#
	sub 		   %{\-}%							#{ token->set_token_type(SUB); }#