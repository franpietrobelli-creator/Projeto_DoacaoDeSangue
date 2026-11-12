from flask import Flask, request, jsonify
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Abre o arquivo JSON
def carregar(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar(arquivo, dados):
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# Percorre uma lista e retorna o item cujo campo 'id' seja igual ao id informado
# Retorna None caso não encontre
def buscar_por_id(lista, id):
    for item in lista:
        if item.get('id') == id:
            return item
    return None

# Rota GET para buscar um hospital específico pelo id
# Exemplo: localhost/hospitais/1
@app.get('/hospitais/<int:id>')
def get_hospital_por_id(id):
    hospitais = carregar('hospitais.json')

    # Usa a função utilitária para encontrar o hospital pelo id
    hospital = buscar_por_id(hospitais, id)

    if hospital:
        return jsonify(hospital), 200
    return jsonify({"mensagem": "Hospital não encontrado"}), 404

# API - Conexão
# Metodos:
# GET - Busca Informação
# POST - Salva a Informação
# PUT - Atualiza a Informação
# DELETE - Remove a Informação

@app.route('/hospitais', methods=['POST'])
def criar_hospitais():
    # Pega os dados enviados pelo Postman em formato JSON
    dados = request.json

    if not dados.get('ocupacao'):
        return jsonify({"mensagem": "Campo ocupacao é obrigatorio"}), 400
    if not isinstance(dados.get('ocupacao'), int):
        return jsonify({"mensagem": "Campo ocupacao deve ser um número inteiro"}), 422

    if not dados.get('capacidade'):
        return jsonify({"mensagem": "Campo capacidade é obrigatorio"}), 400
    if not isinstance(dados.get('capacidade'), int):
        return jsonify({"mensagem": "Campo capacidade deve ser um número inteiro"}), 422

    # Valida se o campo nome foi enviado
    if not dados.get('nome'):
        return jsonify({"mensagem": "Campo nome é obrigatorio"}), 400

    # Valida se o campo estoque_bolsas foi enviado
    if not dados.get('estoque_bolsas'):
        return jsonify({"mensagem": "Campo estoque_bolsas é obrigatorio"}), 400

    # Percorre cada bolsa dentro de estoque_bolsas e valida se o campo tipo foi enviado
    for bolsa in dados.get('estoque_bolsas', []):
        if not bolsa.get('tipo'):
            return jsonify({"mensagem": "Campo tipo é obrigatorio em todas as bolsas"}), 400

    for bolsa in dados.get('estoque_bolsas', []):
        if not bolsa.get("fator_RH"):
            return jsonify({"mensagem": "Campo fator_RH é obrigatorio em todas as bolsas"}), 400
        if not isinstance(bolsa.get("fator_RH"), bool):
            return jsonify({"mensagem": "Campo fator_RH está inválido"}), 422

    # Carrega a lista atual de hospitais do arquivo
    hospitais = carregar('hospitais.json')

    # Gera um novo id automaticamente pegando o maior id existente e somando 1
    novo_id = max((h.get('id', 0) for h in hospitais), default=0) + 1
    dados['id'] = novo_id

    # Adiciona o novo hospital na lista e salva no arquivo
    hospitais.append(dados)
    salvar('hospitais.json', hospitais)

    return jsonify({"mensagem": "Hospital cadastrado com sucesso!"}), 201

# Rota para obter a lista de hospitais com as informações detalhadas:
# - Nome do hospital
# - Capacidade de leitos
# - Ocupação de leitos atual
# - Estoque de Bolsas para cada tipo sanguíneo
# - Fator RH
# - Tipo Sanguíneo
# - Quantidade
@app.route('/hospitais', methods=['GET'])
def get_hospitais():
    return jsonify(carregar('hospitais.json')), 200

@app.put('/hospitais/<int:id>')
def atualizar_hospitais(id):
    hospitais = carregar('hospitais.json')
    dados = request.json

    for hospital in hospitais:
        if hospital.get('id') == id:
            dados['id'] = id  
            hospital.update(dados)
            salvar('hospitais.json', hospitais)
            return jsonify(hospital), 200

    
    return jsonify({"mensagem": "Não encontrado"}), 404

@app.delete('/hospitais/<int:id>')
def deletar_hospitais(id):
    hospitais = carregar('hospitais.json')

    for hospital in hospitais:
        if hospital.get('id') == id:
            hospitais.remove(hospital)
            salvar('hospitais.json', hospitais)
            return jsonify({"mensagem": "Hospital deletado com sucesso!"}), 200

    return jsonify({"mensagem": "Não encontrado"}), 404

# Rota GET para buscar um paciente específico pelo id
# Exemplo: localhost/pacientes/1
@app.get('/pacientes/<int:id>')
def get_paciente_por_id(id):
    pacientes = carregar('pacientes.json')

    # Usa a função utilitária para encontrar o paciente pelo id
    paciente = buscar_por_id(pacientes, id)

    if paciente:
        return jsonify(paciente), 200
    return jsonify({"mensagem": "Paciente não encontrado"}), 404

# Rota POST para cadastrar um novo paciente
#  - nome: Obrigatório
#  - cpf: Obrigatório
#  - telefone: Obrigatório
#  - sexo: Obrigatório
#  - idade: Obrigatório
#  - endereco: Obrigatório
@app.route('/pacientes', methods=['POST'])
def criar_pacientes():
    dados = request.json

    # Acessa o primeiro objeto dentro da lista 'cadastro'
    cadastro = dados.get('cadastro', [{}])[0]

    if not cadastro.get('nome'):
        return jsonify({"mensagem": "Campo nome é obrigatorio"}), 400

    if not cadastro.get('CPF'):
        return jsonify({"mensagem": "Campo cpf é obrigatorio"}), 400

    if not cadastro.get('telefone'):
        return jsonify({"mensagem": "Campo telefone é obrigatorio"}), 400

    if not cadastro.get('sexo'):
        return jsonify({"mensagem": "Campo sexo é obrigatorio"}), 400
    
    # Valida se o sexo informado é um dos valores permitidos
    sexo_validos = ['masculino', 'feminino', 'outro']
    if cadastro.get('sexo') not in sexo_validos:
        return jsonify({"mensagem": "Campo sexo está inválido"}), 422

    if not cadastro.get('idade'):
        return jsonify({"mensagem": "Campo idade é obrigatorio"}), 400
    if not isinstance(cadastro.get('idade'), int):
        return jsonify({"mensagem": "Campo idade deve ser um número inteiro"}), 422

    if not cadastro.get('endereco'):
        return jsonify({"mensagem": "Campo endereco é obrigatorio"}), 400

    # Carrega a lista atual de pacientes do arquivo
    pacientes = carregar('pacientes.json')

    # Gera um novo id automaticamente pegando o maior id existente e somando 1
    novo_id = max((p.get('id', 0) for p in pacientes), default=0) + 1
    dados['id'] = novo_id

    # Adiciona o novo paciente na lista e salva no arquivo
    pacientes.append(dados)
    salvar('pacientes.json', pacientes)

    return jsonify({"mensagem": "Paciente cadastrado com sucesso!"}), 201

# Rota para obter a lista de pacientes com as informações:
# Cadastro:
# - Nome do paciente
# - CPF
# - Telefone
# - Sexo
# - Idade
# - Endereço
# Informações Médicas:
# - Peso
# - Altura
# - Tipo Sanguíneo
# - Fator RH
# - Data do internamento
@app.route('/pacientes', methods=['GET'])
def get_pacientes():
    # 'r' = Leitura   encoding="utf-8" = Interpreta acentos corretamente
    return jsonify(carregar('pacientes.json')), 200

@app.put('/pacientes/<int:id>')
def atualizar_paciente(id):
    pacientes = carregar('pacientes.json')
    dados = request.json


    for paciente in pacientes:
        if paciente.get('id') == id:
            dados['id'] = id  
            paciente.update(dados)
            salvar('pacientes.json', pacientes)
            return jsonify(paciente), 200

    
    return jsonify({"mensagem": "Não encontrado"}), 404

@app.delete('/pacientes/<int:id>')
def deletar_paciente(id):
    pacientes = carregar('pacientes.json')

    for paciente in pacientes:
        if paciente.get('id') == id:
            pacientes.remove(paciente)
            salvar('pacientes.json', pacientes)
            return jsonify({"mensagem": "Paciente deletado com sucesso!"}), 200

    return jsonify({"mensagem": "Não encontrado"}), 404


# Rota GET para buscar uma bolsa específica pelo id
# Exemplo: localhost/bolsas/1
@app.get('/bolsas/<int:id>')
def get_bolsa_por_id(id):
    bolsas = carregar('bolsas.json')

    # Usa a função utilitária para encontrar a bolsa pelo id
    bolsa = buscar_por_id(bolsas, id)

    if bolsa:
        return jsonify(bolsa), 200
    return jsonify({"mensagem": "Bolsa não encontrada"}), 404

@app.route('/bolsas', methods=['GET'])
def get_bolsas():
    # Carrega todas as bolsas do arquivo
    bolsas = carregar('bolsas.json')

    # Pega os filtros opcionais enviados na URL
    # Exemplo: localhost/bolsas?tipo=A&urgencia=alta
    tipo = request.args.get('tipo')
    urgencia = request.args.get('urgencia')

    resultado = []

    # Percorre as bolsas e filtra conforme os parâmetros informados
    # Se o filtro não foi enviado, ignora a condição e inclui a bolsa
    for bolsa in bolsas:
        if tipo and bolsa.get('tipo') != tipo:
            continue
        if urgencia and bolsa.get('urgencia') != urgencia:
            continue
        resultado.append(bolsa)

    return jsonify(resultado), 200

@app.route('/bolsas', methods=['POST'])
def criar_bolsas():
    dados = request.json

    # Acessa o primeiro objeto dentro da lista 'cadastro'
    cadastro = dados.get('cadastro', [{}])[0]

    if not cadastro.get('tipo_sanguineo'):
        return jsonify({"mensagem": "Campo tipo_sanguineo é obrigatorio"}), 400

    if not cadastro.get('fator_rh'):
        return jsonify({"mensagem": "Campo fator_rh é obrigatorio"}), 400
    if not isinstance(cadastro.get('fator_rh'), bool):
        return jsonify({"mensagem": "Campo fator_rh está inválido"}), 422

    if not cadastro.get('quantidade'):
        return jsonify({"mensagem": "Campo quantidade é obrigatorio"}), 400
    if not isinstance(cadastro.get('quantidade'), int):
        return jsonify({"mensagem": "Campo quantidade deve ser um número inteiro"}), 422

    # Carrega a lista atual de bolsas do arquivo
    bolsas = carregar('bolsas.json')

    # Gera um novo id automaticamente pegando o maior id existente e somando 1
    novo_id = max((b.get('id', 0) for b in bolsas), default=0) + 1
    dados['id'] = novo_id

    # Adiciona a nova bolsa na lista e salva no arquivo
    bolsas.append(dados)
    salvar('bolsas.json', bolsas)

    return jsonify({"mensagem": "Bolsa cadastrada com sucesso!"}), 201

# Rota PUT para atualizar uma bolsa existente pelo id
# Recebe os novos dados no body e sobrescreve os campos da bolsa encontrada
# Retorna 200 se atualizado, 404 se não encontrado
@app.put('/bolsas/<int:id>')
def atualizar(id):
    
    bolsas = carregar('bolsas.json')
    dados = request.json

    for bolsa in bolsas:
        if bolsa.get('id') == id:
            dados['id'] = id  
            bolsa.update(dados)
            salvar('bolsas.json', bolsas)
            return jsonify(bolsa), 200

    
    return jsonify({"mensagem": "Não encontrado"}), 404

# Rota DELETE para remover uma bolsa pelo id
# Retorna 200 se deletado, 404 se não encontrado
@app.delete('/bolsas/<int:id>')
def deletar(id):
    
    bolsas = carregar('bolsas.json')

    for bolsa in bolsas:
        if bolsa.get('id') == id:
            bolsas.remove(bolsa)
            salvar('bolsas.json', bolsas)
            return jsonify({"mensagem": "Bolsa deletada com sucesso!"}), 200

    return jsonify({"mensagem": "Não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
    