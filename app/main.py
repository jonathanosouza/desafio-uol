from flask import request, jsonify
import subprocess
from flask import Flask, request, jsonify
import os
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../data')
ALLOWED_FILENAME = re.compile(r'^[A-Za-z0-9_-]+$')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = '/app/data'


@app.route('/upload', methods=['PUT'])
def upload_arquivos():
    if 'file' not in request.files:
        return jsonify({'error': 'Arquivo não enviado'}), 400

    file = request.files['file']
    filename = file.filename

    name_no_ext = os.path.splitext(filename)[0]

    if not ALLOWED_FILENAME.match(name_no_ext):
        return jsonify({'error': 'Nome de arquivo inválido'}), 400

    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_exists = os.path.exists(path)
    file.save(path)

    return jsonify({'filename': filename}), 204 if file_exists else 201


@app.route('/arquivos', methods=['GET'])
def listar_arquivos():
    try:
        arquivos = os.listdir(app.config['UPLOAD_FOLDER'])
        arquivos.sort()

        pages = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        ini = (pages - 1) * size
        fim = ini + size

        return jsonify({
            "pages": pages,
            "size": size,
            "total": len(arquivos),
            "arquivos": arquivos[ini:fim]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/size', methods=['GET'])
def get_usuario_por_tamanho():
    nome_arquivo = request.args.get('nome_arquivo')
    size = request.args.get('size')

    if not nome_arquivo:
        return jsonify({'error': 'Parâmetro "nome_arquivo" é obrigatório'}), 400

    if size and size != '-min':
        return jsonify({'error': 'Parâmetro "size" inválido. Use "-min" ou não informe.'}), 400

    script_bash = 'app/bash/max-min-size.sh'
    arquivo_path = f'data/{nome_arquivo}'

    if not os.path.exists(arquivo_path):
        return jsonify({'error': 'Arquivo não encontrado'}), 404

    try:
        cmd = ['bash', script_bash, arquivo_path]
        if size:
            cmd.append(size)

        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )

        linha = result.stdout.strip()
        partes = linha.split()

        if len(partes) >= 5 and partes[3] == "size":
            return jsonify({
                "username": partes[0],
                "folder": partes[1],
                "numberMessages": int(partes[2]),
                "size": int(partes[4])
            })

        return jsonify({'error': 'Formato inesperado na saída'}), 500

    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.stderr}), 500


@app.route('/usuarios_ordenados', methods=['GET'])
def get_usuarios_ordenados():
    nome_arquivo = request.args.get('nome_arquivo')
    orderby = request.args.get('orderby')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    if not nome_arquivo:
        return jsonify({'error': 'Parâmetro "nome_arquivo" é obrigatório'}), 400

    if orderby and orderby != '-desc':
        return jsonify({'error': 'Parâmetro "orderby" inválido. Use "-desc" ou não informe.'}), 400

    script_path = 'app/bash/order-by-username.sh'
    arquivo_path = f'data/{nome_arquivo}'

    if not os.path.exists(arquivo_path):
        return jsonify({'error': 'Arquivo não encontrado'}), 404

    try:
        ini = (page - 1) * limit
        cmd = ['bash', script_path, arquivo_path,
               orderby or '', str(ini), str(limit)]

        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )

        linhas = result.stdout.strip().split('\n')
        resultado = []

        for linha in linhas:
            partes = linha.strip().split()
            if len(partes) >= 5 and partes[3] == "size":
                resultado.append({
                    "username": partes[0],
                    "folder": partes[1],
                    "numberMessages": int(partes[2]),
                    "size": int(partes[4])
                })

        return jsonify(resultado)

    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.stderr}), 500


@app.route('/usuarios_por_mensagens', methods=['GET'])
def get_usuarios_por_mensagens():
    nome_arquivo = request.args.get('nome_arquivo')
    min_param = request.args.get('min')
    max_param = request.args.get('max')

    min_msgs = int(min_param) if min_param else None
    max_msgs = int(max_param) if max_param else None
    username_param = request.args.get('username', '').lower()

    if username_param:
        offset = 0
        limit = 10000
    else:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        offset = (page - 1) * limit

    if not nome_arquivo:
        return jsonify({'error': 'Parâmetro "nome_arquivo" é obrigatório'}), 400

    arquivo_path = f'data/{nome_arquivo}'
    script_path = 'app/bash/between-msgs.sh'

    if not os.path.exists(arquivo_path):
        return jsonify({'error': 'Arquivo não encontrado'}), 404

    try:
        cmd = ['bash', script_path, arquivo_path,
               str(min_msgs or 0), str(max_msgs or 99999999),
               str(offset), str(limit)]

        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )

        linhas = result.stdout.strip().split('\n')
        usuarios_filtrados = []

        for linha in linhas:
            partes = linha.strip().split()

            if len(partes) >= 5 and partes[3].lower() == "size":
                email = partes[0]
                folder = partes[1].lower()
                number_messages = int(partes[2])
                size = int(partes[4])

                if folder == "inbox":
                    if (min_msgs is None or number_messages >= min_msgs) and \
                       (max_msgs is None or number_messages <= max_msgs):
                        if not username_param or username_param in email.lower():
                            usuarios_filtrados.append({
                                "username": email,
                                "folder": folder,
                                "numberMessages": number_messages,
                                "size": size
                            })

        return jsonify(usuarios_filtrados)

    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.stderr}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
