from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Hola Flask, que tal? c:"

@app.route('/create-article', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        return f"Articulo creado: {title}, Contenido: {content}"
    return '''
    <form method='POST' action="create-article">
        <label for='title'>Título del artículo:</label><br>
        <input type='text' id='title' name='title'><br><br>

        <label for='content'>Contenido del artículo:</label><br>
        <textarea id='content' name='content'></textarea><br><br>

        <input type='submit' id='title' value='Crear Artículo'>
    </form>
'''

@app.route('/article/<int:article_id>')
def view_article(article_id):
    return f"Estas viendo el articulo numero: {article_id}"

if __name__ == '__main__':
    app.run(debug=True)