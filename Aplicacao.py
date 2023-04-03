# Contruir a API --> FLASK --> Servidor local

# Importando as bibliotecas necessárias para a Construção da API, importação do modelo e trabalhar com DB
from flask import Flask, request
import joblib
import sqlite3
from datetime import datetime

# Instanciar o aplicativo
Aplicativo = Flask(__name__)

# Carregar o modelo
modelo = joblib.load('Modelo_RandomForest_v1.pkl')

# Definindo a rota da API, após acessar a rota, aparecerá a mensagem da função em caso de sucesso
# O método 'GET' permite fazer consultas dentro da função com parâmetros


@Aplicativo.route('/API_Preditivo/<area>;<quartos>;<banheiros>;<vagas_garagem>;<andar>;<animal>;<mobiliado>;<valor_condominio>;<valor_iptu>', methods=['GET'])
def Funcao_01(area, quartos, banheiros, vagas_garagem, andar, animal, mobiliado, valor_condominio, valor_iptu):

    # Recebendo a data e hora inicio
    data_inicio = datetime.now()

    # Recebendo os inputs da API
    lista = [
        float(area), float(quartos), float(
            banheiros), float(vagas_garagem), float(andar),
        float(animal), float(mobiliado), float(
            valor_condominio), float(valor_iptu)
    ]

    # Tentar a previsão
    try:
        previsao = round(float(modelo.predict([lista])), 2)

        # Inserir o valor da previsão na lista
        lista.append(previsao)

        # Termino do processo
        data_fim = datetime.now()
        processamento = data_fim - data_inicio

        # Conexão com Banco de Dados
        Conexao_Banco = sqlite3.connect('Banco_Dados_API.db')
        Cursor = Conexao_Banco.cursor()

        # Query --> Inserir os valores no Banco de Dados
        query_inserir = f'''
            INSERT INTO LOG_API (inputs, inicio, fim, processamento)
            VALUES ( '{str(lista)}', '{data_inicio}', '{data_fim}', '{processamento}' )
        '''

        # Executando a Query
        Cursor.execute(query_inserir)
        Conexao_Banco.commit()

        # Fechar a conexão com o Banco de Dados
        Cursor.close()

        return {'Valor_Aluguel': str(previsao)}

    # Exceção caso algum parâmetro estiver errado
    except:
        return {'Aviso': 'Deu algum erro!'}


if __name__ == '__main__':
    Aplicativo.run(debug=True)

'''
    Após construção do código acima, rode o código através do CMD para ligar o servidor e deixar rodando
    Ex:
        $ python Aplicacao.py
        * Serving Flask app 'Aplicacao'
        * Debug mode: on
        WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
        * Running on http://127.0.0.1:5000
        Press CTRL+C to quit
        * Restarting with stat
        * Debugger is active!
        * Debugger PIN: 129-927-942

    Obs: para acessar essa API, basta copiar a URL acima e colocar a rota na sequência
        Ex: http://127.0.0.1:5000/API_Preditivo
'''
