from flask import g, redirect, render_template, request, url_for
from functions.db_anotacao import create_anotação


def mod_novo(mysql):

    # Se o usuário não está logado redireciona para a página de login
    if g.usuario == '':
        return redirect(url_for('login'))

    # Variável que ativa a mensagem de sucesso no HTML
    sucesso = False

    # Se o formulário foi enviado
    if request.method == 'POST':

        # Obtém os dados preenchidos na forma de dicionário
        form = dict(request.form)

        # Teste de mesa (comente depois dos testes)
        # Verifica se os dados do formulário chegaram ao back-end
        # print('\n\n\n FORM:', form, '\n\n\n')

        # Grava os dados no banco de dados
        if create_anotação(mysql=mysql, form=form):
            sucesso = True

    # Dados, variáveis e valores a serem passados para o template HTML
    pagina = {
        'titulo': 'Bloco de Notas - Novo Treco',
        'usuario': g.usuario,
        'sucesso': sucesso,
    }

    # Renderiza o template HTML, passaod valores para ele
    return render_template('novo.html', **pagina)
