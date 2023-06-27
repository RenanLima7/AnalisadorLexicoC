import random

# Definição dos tokens
tokens = (
    'PALAVRA_CHAVE',
    'IDENTIFICADOR',
    'NUMERO',
    'OPERADOR',
    'DELIMITADOR',
    'ATRIBUICAO',
)


# Operadores e delimitadores
operadores = ['+', '-', '*', '/']
operadores_logicos = ['==', '!=', '>=', '<=', '&&', '||']
delimitadores = ['(', ')', ';', '{', '}']

# Palavras-chave da linguagem C
palavras_chave = [
    'int', 'float', 'char', 'if', 'else', 'for', 'while', 'do', 'return'
]

def lexer(codigo):
    codigo = codigo.replace('\n', ' ')  # Remover quebras de linha
    tokens = []
    i = 0

    while i < len(codigo):
        if codigo[i].isspace():
            i += 1
            continue
        elif codigo[i] in operadores:
            tokens.append(('OPERADOR', codigo[i]))
            i += 1
        elif codigo[i] in operadores_logicos:
            tokens.append(('OPERADOR LOGICO', codigo[i]))
            i += 1
        elif codigo[i] == '=':
            tokens.append(('ATRIBUICAO', codigo[i]))
            i += 1
        elif codigo[i] in delimitadores:
            tokens.append(('DELIMITADOR', codigo[i]))
            i += 1
        elif codigo[i].isdigit():
            numero = ''
            while i < len(codigo) and codigo[i].isdigit():
                numero += codigo[i]
                i += 1
            tokens.append(('NUMERO', int(numero)))
        elif codigo[i].isalpha() or codigo[i] == '_':
            identificador = ''
            while i < len(codigo) and (codigo[i].isalnum() or codigo[i] == '_'):
                identificador += codigo[i]
                i += 1
            if identificador in palavras_chave:
                tokens.append(('PALAVRA_CHAVE', identificador))
            else:
                tokens.append(('IDENTIFICADOR', identificador))
        else:
            print("Caractere inválido: '%s'" % codigo[i])
            i += 1

    return tokens

# Função para analisar a sintaxe
def parser(tokens):
    i = 0

    def expressao():
        nonlocal i
        valor = termo()
        while i < len(tokens) and tokens[i][0] in ['MAIS', 'MENOS']:
            if tokens[i][0] == 'MAIS':
                i += 1
                valor += termo()
            else:
                i += 1
                valor -= termo()
        return valor

    def termo():
        nonlocal i
        valor = fator()
        while i < len(tokens) and tokens[i][0] in ['MULTIPLICACAO', 'DIVISAO']:
            if tokens[i][0] == 'MULTIPLICACAO':
                i += 1
                valor *= fator()
            else:
                i += 1
                valor /= fator()
        return valor

    def fator():
        nonlocal i
        if tokens[i][0] == 'NUMERO':
            valor = tokens[i][1]
            i += 1
            return valor
        elif tokens[i][0] == 'LPAREN':
            i += 1
            valor = expressao()
            if i < len(tokens) and tokens[i][0] == 'RPAREN':
                i += 1
                return valor
            else:
                print("Erro de sintaxe: ')' esperado")


# Gramática BNF
gramatica_bnf = {
    "<programa>": ["<declaracoes>"],
    "<declaracoes>": ["<declaracao> <declaracoes>", "<declaracao>"],
    "<declaracao>": ["<tipo> <identificador> <atribuicao> <expressao> <DELIMITADOR>"],
    "<tipo>": ["PALAVRA_CHAVE"],
    "<identificador>": ["IDENTIFICADOR"],
    "<atribuicao>": ["ATRIBUICAO <expressao>", ""],
    "<expressao>": ["<termo> <expressao_restante>"],
    "<expressao_restante>": ["<operador> <termo> <expressao_restante>", ""],
    "<termo>": ["<fator> <termo_restante>"],
    "<termo_restante>": ["<operador> <fator> <termo_restante>", ""],
    "<fator>": ["IDENTIFICADOR", "NUMERO", "( <expressao> )"],
    "<operador>": ["OPERADOR"],
    "<DELIMITADOR>": ["DELIMITADOR"]
}

# Função para gerar a derivação da gramática BNF
def gerar_derivacao(nao_terminal):
    if nao_terminal not in gramatica_bnf:
        return nao_terminal

    producoes = gramatica_bnf[nao_terminal]
    producao_escolhida = random.choice(producoes)
    derivacao = ''
    for simbolo in producao_escolhida.split():
        if simbolo.startswith("<"):
            derivacao += gerar_derivacao(simbolo) + ' '
        else:
            derivacao += simbolo + ' '
    return derivacao.strip()

def visualizarTokens(tokens):
    for token in tokens:
        print(token, " \n")

# Exemplo de uso
codigo_exemplo = '''
int main() {
    int a = 10;
    int b = 5;
    int c = a + b;
    return c
}
'''

resultado = lexer(codigo_exemplo)
visualizarTokens(resultado)

# Geração da derivação da gramática BNF
derivacao = gerar_derivacao("<programa>")
print("Derivação da gramática BNF:")
for linha in derivacao.split("<"):
    print("<" + linha.strip())
