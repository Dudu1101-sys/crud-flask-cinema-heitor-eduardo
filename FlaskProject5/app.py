from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)


def ligar_banco():
    banco = psycopg2.connect(
        database="Cinema",
        host="localhost",
        user="postgres",
        password="senai",
        port="5432"
    )
    return banco


@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/cadastrar_filmes')
def cadastro():
    return render_template('cadastrar_filmes.html')


@app.route('/cadastrar_sala')
def cadastro_sala():
    return render_template('cadastrar_sala.html')



@app.route('/criar_filmes', methods=['POST'])
def criar():
    titulo = request.form['titulo']
    genero = request.form['genero']
    duracao_min = request.form['duracao_min']
    data_lancamento = request.form['data_lancamento']

    banco = ligar_banco()
    cursor = banco.cursor()

    sql = """
    INSERT INTO filme (titulo, genero, duracao_min, data_lancamento)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (
        titulo,
        genero,
        duracao_min,
        data_lancamento
    ))

    banco.commit()
    cursor.close()
    banco.close()

    return redirect('/exibir_filmes')



@app.route('/criar_sala', methods=['POST'])
def criar_sala():
    nome = request.form['nome']
    tipo = request.form['tipo']
    capacidade = request.form['capacidade']
    preco_ingresso = request.form['preco_ingresso']

    banco = ligar_banco()
    cursor = banco.cursor()

    sql = """
    INSERT INTO sala (nome, tipo, capacidade, preco_ingresso)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (
        nome,
        tipo,
        capacidade,
        preco_ingresso
    ))

    banco.commit()
    cursor.close()
    banco.close()

    return redirect('/exibir_salas')


@app.route('/exibir_filmes')
def exibir():
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute("SELECT * FROM filme")
    lista = cursor.fetchall()

    cursor.close()
    banco.close()

    return render_template('exibir_filmes.html', lista=lista)


@app.route('/exibir_salas')
def exibir_salas():
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute("SELECT * FROM sala")
    lista = cursor.fetchall()

    cursor.close()
    banco.close()

    return render_template('exibir_sala.html', lista=lista)



@app.route('/editar_filme/<int:id_filme>', methods=['GET', 'POST'])
def editar_filme(id_filme):
    banco = ligar_banco()
    cursor = banco.cursor()

    if request.method == 'POST':
        titulo = request.form['titulo']
        genero = request.form['genero']
        duracao_min = request.form['duracao_min']
        data_lancamento = request.form['data_lancamento']

        sql = """
        UPDATE filme
        SET titulo = %s, genero = %s, duracao_min = %s,
            data_lancamento = %s
        WHERE id_filme = %s
        """

        cursor.execute(sql, (
            titulo,
            genero,
            duracao_min,
            data_lancamento,
            id_filme
        ))

        banco.commit()
        cursor.close()
        banco.close()

        return redirect('/exibir_filmes')

    cursor.execute("SELECT * FROM filme WHERE id_filme = %s", (id_filme,))
    filme = cursor.fetchone()

    cursor.close()
    banco.close()

    return render_template('editar_filme.html', filme=filme)


@app.route('/editar_sala/<int:id_sala>', methods=['GET', 'POST'])
def editar_sala(id_sala):
    banco = ligar_banco()
    cursor = banco.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        tipo = request.form['tipo']
        capacidade = request.form['capacidade']
        preco_ingresso = request.form['preco_ingresso']

        sql = """
        UPDATE sala
        SET nome = %s, tipo = %s, capacidade = %s,
            preco_ingresso = %s
        WHERE id_sala = %s
        """

        cursor.execute(sql, (
            nome,
            tipo,
            capacidade,
            preco_ingresso,
            id_sala
        ))

        banco.commit()
        cursor.close()
        banco.close()

        return redirect('/exibir_salas')

    cursor.execute("SELECT * FROM sala WHERE id_sala = %s", (id_sala,))
    sala = cursor.fetchone()

    cursor.close()
    banco.close()

    return render_template('editar_sala.html', sala=sala)


@app.route('/excluir_filme/<int:id_filme>')
def excluir_filme(id_filme):
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute(
        "DELETE FROM filme WHERE id_filme = %s",
        (id_filme,)
    )

    banco.commit()
    cursor.close()
    banco.close()

    return redirect('/exibir_filmes')


@app.route('/excluir_sala/<int:id_sala>')
def excluir_sala(id_sala):
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute(
        "DELETE FROM sala WHERE id_sala = %s",
        (id_sala,)
    )

    banco.commit()
    cursor.close()
    banco.close()

    return redirect('/exibir_salas')


if __name__ == '__main__':
    app.run()
