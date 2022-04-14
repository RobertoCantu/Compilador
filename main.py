# <VARS>
def vars(p):
  '''
  vars          : tipo_simple vars_2
                | tipo_compuesto vars_2
  '''

def vars_2(p):
  '''
  vars_2        : ID vars_3
  '''

def vars_3(p):
  '''
  vars_3        : vars_comma
                | LSQRBRACKET CTEINT RSQRBRACKET vars_semicolon
                | vars_semicolon
  '''

def vars_comma(p):
  '''
  vars_comma      : vars_2
  '''

def vars_semicolon(p):
  '''
  vars_semicolon  : vars
                  | empty
  '''

# <FUNCIONES>
def funciones(p):
  '''
  funciones      : tipo_simple FUNCTION LPAREN param RPAREN LBRACKET vars estatutos RETURN LPAREN expresion RPAREN RBRACKET funciones
                 | VOID FUNCTION LPAREN param RPAREN LBRACKET vars estatutos RBRACKET funciones
                 | empty
  '''

# <EXP>
def exp(p):
  '''
  exp    : t_exp exp_2
  '''

def exp_2(p):
  '''
  exp_2  : OR exp
          | empty
  '''

# <T_EXP>
def t_exp(p):
  '''
  t_exp    : g_exp t_exp_2
  '''

def t_exp_2(p):
  '''
  t_exp_2  : AND t_exp
            | empty
  '''
  

# <G_EXP>
def g_exp(p):
  '''
  g_exp    : m_exp g_exp_2
  '''

def g_exp_2(p):
  '''
  g_exp_2   : GREATER m_exp
            | LESS m_exp
            | NOTEQUAL m_exp
            | EQUAL m_exp
            | empty
  '''

# <M_EXP>
def m_exp(p):
  '''
  m_exp    : t m_exp_2
  '''

def m_exp_2(p):
  '''
  m_exp_2   : PLUS  m_exp
            | MINUS m_exp
            | empty
  '''
# <T>
def t(p):
  '''
  t        : f t_2
  '''

def t(p):
  '''
  t_2       : TIMES t
            | DIVIDE t
            | empty
  '''

# <F>
def f(p):
  '''
  f         : LPAREN exp RPAREN f_2
            | CTEI RPAREN f_2
            | CTEF RPAREN f_2
            | CTESTRING RPAREN f_2
            | variable RPAREN f_2
            | llamada RPAREN f_2
            | ID DOT ID RPAREN f_2
  '''

def f_2(p):
  '''
  f_2      : empty
  '''

# <WRITE>
def write(p):
  '''
  write    : LPAREN write_2
  '''

def write_2(p):
  '''
  write_2   : exp  RPAREN write_3
            | letrero RPAREN write_3
  '''

def write_3(p):
  '''
  write_3  : COMMA write_2
           | empty
  '''


# <LOOP_COND>
def loop_cond(p):
  '''
  loop_cond  : L_1 loop_cond_2
  '''

def loop_cond_2(p):
  '''
  loop_cond_2   : OR loop_cond
                | empty
  '''

# <L_1>
def l_1(p):
  '''
  l_1    : l_2 l_1_2
  '''

def l_1_2(p):
  '''
  l_1_2     : AND l_1
            | empty
  '''

# <L_2>
def l_2(p):
  '''
  l_2    : l_3 l_2_2
  '''

def l_2_2(p):
  '''
  l_2_2     : GREATER l_3
            | LESS l_3
            | NOTEQUAL l_3
            | EQUAL l_3
            | empty
  '''

def l_3(p):
  '''
  l_3       : CTEI empty
            | LPAREN loop_cond RPAREN empty
  '''