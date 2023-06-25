# Definição dos tokens
tokens = (
    'IDENTIFICADOR',
    'NUMERO',
    'MAIS',
    'MENOS',
    'MULTIPLICACAO',
    'DIVISAO',
    'LPAREN',
    'RPAREN',
    'PONTOVIRGULA',
)

# Palavras-chave da linguagem C
palavras_chave = [
    'int', 'float', 'char', 'if', 'else', 'for', 'while', 'do', 'return'
]

# Operadores e delimitadores
operadores = ['+', '-', '*', '/']
operadores_logicos = ['==', '!=', '>=', '<=', '&&', '||']
delimitadores = ['(', ')', ';', '{', '}']

# Função para separar o código em tokens
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

# Exemplo de uso
codigo_exemplo = '''
float teste() {
    int a = 10;
    int b = 5;
    int c = a + b;
    return c;
}
'''

resultado = lexer(codigo_exemplo)
print(resultado)





