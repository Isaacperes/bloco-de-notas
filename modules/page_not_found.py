from flask import g, render_template


def mod_page_not_found():
    pagina = {
        'titulo': 'Bloco de Notas - Erro 404',
        'usuario': g.usuario,
    }
    return render_template('404.html', **pagina), 404
