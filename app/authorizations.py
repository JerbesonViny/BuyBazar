from flask import request, session

"""
ATENÇÃO: Colocamos as autorizações somente como demonstrativo para a condição de,
se caso adotassemos, utilizar esse arquivo dentro das rotas para liberar
as permissões de usuário e administrador da aplicação. Portanto, deixamos esse
arquivo como complemento da aplicação desenvolvida.
"""

"""
0 - Não cadastrado.
1 - Administrador
2 - Usuário
"""

authorizations = {
  'comprar-produto/': {1: 0, 2: 1},
  'cadastrar-produtos/': {1: 1, 2: 0},
  'atualizar-produto/': {1: 1, 2: 0},
  'deletar-produto/': {1: 1, 2: 0},
  'tirar-vendido/': {1: 1, 2: 0},
  'declarar-vendido/': {1: 1, 2: 0},
  'minhas-compras/': {1: 0, 2: 1},
  'reportar-erro/': {1: 1, 2: 1},
  'resultados/': {1: 1, 2: 1}
}

def check():
  method = request.path[1:]

  try:
    perfil = session['logado'][4]
  except:
    return 0
  
  return authorizations[method][perfil]