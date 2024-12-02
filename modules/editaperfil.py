from flask import g, redirect, render_template, request, url_for
from functions.db_usuario import get_user_data, update_password, update_user


def mod_editaperfil(mysql):
    if g.usuario == '':
        return redirect(url_for('login'))
    if request.method == 'POST':
        form = dict(request.form)
        update_user(mysql=mysql, form=form)
        if form['senha2'] != '':
            update_password(mysql=mysql, form=form)
        return redirect(url_for('logout'))
    row = get_user_data(mysql=mysql)
    pagina = {
        'titulo': 'Bloco de Notas - Erro 404',
        'usuario': g.usuario,
        'form': row
    }
    return render_template('editaperfil.html', **pagina)
