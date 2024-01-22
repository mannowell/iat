from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)

# Crie uma conexão com o banco de dados
conexao = sqlite3.connect("animal.db")

# Crie um cursor para executar comandos no banco de dados
cursor = conexao.cursor()

# Receba os dados do formulário HTML
nome = request.form["nome"]
especie = request.form["especie"]
custo = request.form["marca"]
duracao_estoque = request.form["duracao_estoque"]

# Valide os dados recebidos
if nome is None or nome == "":
    return "O nome do alimento é obrigatório."
if especie is None or especie == "":
    return "A espécie do alimento é obrigatória."
if not isinstance(custo, int):
    return "O custo deve ser um número inteiro."
if not isinstance(duracao_estoque, int):
    return "A duração do estoque deve ser um número inteiro."

# Insira os dados na tabela do SQLite
cursor.execute("INSERT INTO animal (nome, especie, custo, duracao_estoque) VALUES (?, ?, ?, ?)", (nome, especie, custo, duracao_estoque))

# Confirme as alterações no banco de dados
conexao.commit()

# Feche a conexão com o banco de dados
conexao.close()

# Redirecione o usuário para a página principal
return redirect("/")

@app.route('/')
def index():
    connection = sqlite3.connect('alimento.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Alimento')
    alimento = cursor.fetchall()

    connection.close()

    return render_template('index.html', alimentos=alimentos)

@app.route('/adicionar_produto', methods=['GET', 'POST'])
def adicionar_produto():
    if request.method == 'POST':
        # Obter dados do formulário
        nome = request.form.get('nome', '')
        descricao = request.form.get('descricao', '')
        preco = float(request.form.get('preco', 0.0))
        estoque = int(request.form.get('estoque', 0))

        connection = sqlite3.connect('alimento.db')
        cursor = connection.cursor()

        cursor.execute('INSERT INTO Alimentos (Nome, Descrição, Preço, Estoque) VALUES (?, ?, ?, ?)',
                       (nome, descricao, preco, estoque))


        # Commit e fechar a conexão
        connection.commit()
        connection.close()

        # Adiciona uma mensagem de sucesso
        flash('Produto adicionado com sucesso!', 'success')

        # Redirecionar de volta para a página principal
        return redirect(url_for('index'))

    connection = sqlite3.connect('alimento.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Produtos')
    produtos = cursor.fetchall()
    connection.close()

    # Se o método for GET, renderiza a página adicionar_produto.html
    return render_template('adicionar_produto.html', produtos=produtos)

if __name__ == '__main__':
    app.run(debug=True)
