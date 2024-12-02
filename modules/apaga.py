

from flask import g, redirect, url_for

from functions.db_anotacao import delete_anotação


def mod_apaga(mysql, id):

    # Se o usuário não está logado redireciona para a página de login
    if g.usuario == '':
        return redirect(url_for('login'))

    # Apaga registro
    delete_anotação(mysql=mysql, id=id)

    # Retorna para a lista de items
    return redirect(url_for('home', a='apagado'))
