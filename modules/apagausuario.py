from flask import g, make_response, redirect, url_for
from functions.db_anotacao import delete_anotação
from functions.db_usuario import delete_user


def mod_apagausuario(mysql):
    if g.usuario == '':
        return redirect(url_for('login'))
    delete_user(mysql)
    delete_anotação(mysql)
    resposta = make_response(redirect(url_for('login')))
    resposta.set_cookie(
        key='usuario',
        value='',
        max_age=0
    )
    return resposta
