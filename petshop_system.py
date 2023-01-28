# Importção dos móudulos
import os
import platform
import cx_Oracle
import pandas as pd

# Try para tentativa de Conexão
# com o Banco de Dados
try:

    # Checa o sistema operacional
    op_sys = platform.system()
    comando = ''
 
    # Especifica o comando para limpeza de tela
    if op_sys == 'Windows':
        comando = 'cls'
    else:
        comando = 'clear'

    # Início da conexão com o Banco
    dsnStr = cx_Oracle.makedsn("oracle.fiap.com.br", "1521", "ORCL")
    conn = cx_Oracle.connect(user='PF1530', password="141212", dsn=dsnStr)
    
    # Geração dos cursores
    curs1 = conn.cursor()
    curs2 = conn.cursor()
    curs3 = conn.cursor()
    curs4 = conn.cursor()
    
    while True:
        os.system(comando)      # Limpa a tela
        print("-- Petshop System --\n")
        print("Escolha uma das opções:\n \
            1 - Cadastrar Pet\n \
            2 - Consultar Pet\n \
            3 - Alterar dados do Pet\n \
            4 - Excluir um PET\n \
            5 - Sair")
        escolha = input('>> ')  # Recebe a escolha do usuário
        
        # Condição que checa se o valor digitado 
        # não é um número 
        if not escolha.isdigit():
            os.system(comando)
            print("Valor incorreto, por favor digite um número!")
            input("Presione ENTER")
        
        else:

            # Condição para Cadastro de Pet
            if escolha == '1':
                os.system(comando)  # Limpa a tela
                print("-- Cadastrar Pet --\n")
                
                # Recebe os valores para cadastro
                tipo = input("Digite o tipo: ")
                nome = input("Digite o nome: ")
                idade = input("Digite a idade: ")
                
                # Condição que checa se valor 'idade'
                # é um número
                if idade.isdigit():
                    idade = int(idade)
                
                # Retorna um erro e volta para tela inicial
                # caso valor 'idade' não seja válido
                else:
                    os.system(comando)
                    print("Valor incorreto, digite no campo idade um número inteiro!")
                    input("Presione ENTER")
                    continue
                
                # Tentativa de inserção dos valores
                # no Banco de Dados
                try:
                    data_insert = f""" INSERT INTO petshop (tipo_pet, nome_pet, idade)VALUES ('{tipo}', '{nome}', {idade}) """

                    curs1.execute(data_insert)
                    conn.commit()

                # Captura qualquer exceção no processo
                # de inserção dos valores
                except Exception as e:
                    print("Erro: ", e)
                    input("\nPresione ENTER")
                    continue
                
                # Exibe mensagem de sucesso caso não
                # haja erros na inserção dos valores
                else:
                    os.system(comando)
                    print("Dados inseridos!")

                input("\nPresione ENTER")

            # Condição para Consulta de Pets
            elif escolha == '2':
                os.system(comando)  # Limpa a tela
                print("-- Consultar Pet --\n")
                lista_dados = []    # Lista para captura de dados do Banco

                # Tentativa de consulta dos valores
                # do Banco de Dados
                try:
                    curs2.execute('SELECT * FROM petshop')
                    data = curs2.fetchall()
                    
                    # Insere os valores do Banco
                    # dentro da lista 'lista_dados'
                    for dt in data:
                        lista_dados.append(dt)

                    # Gera um DataFrame com os dados da lista
                    dados_df = pd.DataFrame.from_records(lista_dados, columns=['Id', 'Tipo', 'Nome', 'Idade'], index='Id')

                # Captura qualquer exceção no processo
                # de consulta dos valores
                except Exception as e:
                    print("Erro: ", e)
                    input("\nPresione ENTER")
                    continue
                
                # Exibe uma mensagem caso o DataFrame
                # esteja vazio
                if dados_df.empty:
                    print("Não há animais cadastrados.")
                
                # Exibe os dados do Banco de Dados
                else:
                    print(dados_df)

                input("\nPresione ENTER")   # Pausa o loop para a leitura da mensagem

            # Condição para Alterar dados de um Pet
            elif escolha == '3':
                os.system(comando)  # Limpa a tela
                print("-- Alterar dados do Pet --\n")
        
                lista_dados = []    # Lista para captura de dados do Banco
                lista_ids = []      # Lista para captura dos ids do Banco

                # Tentativa de consulta dos valores
                # do Banco de Dados
                try:
                    curs3.execute('SELECT * FROM petshop')
                    data = curs3.fetchall()
                    
                    # Insere os valores do Banco
                    # dentro da lista 'lista_dados'
                    for dt in data:
                        lista_dados.append(dt)

                    # Gera um DataFrame com os dados da lista
                    dados_df = pd.DataFrame.from_records(lista_dados, columns=['Id', 'Tipo', 'Nome', 'Idade'])

                    # Insere os ids do Banco
                    # dentro da lista 'lista_ids'
                    for indice, item in dados_df['Id'].items():
                        lista_ids.append(item)

                # Captura qualquer exceção no processo
                # de consulta dos valores
                except Exception as e:
                    print("Erro: ", e)
                    input("\nPresione ENTER")
                    continue
                
                # Exibe uma mensagem caso o DataFrame
                # esteja vazio
                if dados_df.empty:
                    print("Não há animais cadastrados.")
                    input("\nPresione ENTER")
                    continue
                
                else:    
                    print(dados_df)                     # Exibe os dados do Banco
                    print("\nDigite para [S]air")       # Informa ao usuário como retornar a tela incial
                    pet_id = input("Escolha um Id: ")   # Permite o usuário escolher um Pet
                
                # Condição que permite ao usuário
                # retornar a tela incial
                if pet_id.upper() == 'S':
                    continue
                
                # Condição que checa se o valor digitado
                # é um numero, caso contrario exibe uma mensagem
                # e retorna para a tela inicial
                if not pet_id.isdigit():
                    os.system(comando)
                    print("Valor inválido, digite um número!")
                    input("\nPresione ENTER")
                    continue
                else:
                    os.system(comando)      # Limpa a tela
                    pet_id = int(pet_id)    # Converte variavel para um int
                    flag = False            # Gera uma variavel para verificação

                    # Laço que percorre lista de ids
                    for n in lista_ids:
                        
                        # Checa se o valor digitado
                        # está na lista de ids
                        if n == pet_id:

                            # Recebe os valores para atualização do Banco
                            novo_tipo = input("Digite um novo tipo: ")
                            novo_nome = input("Digite um novo nome: ")
                            nova_idade = input("Digite uma nova idade: ")
                            
                            # Condição que checa se valor 'idade'
                            # é um número
                            if nova_idade.isdigit():
                                data_update = f"""
                                UPDATE petshop SET tipo_pet='{novo_tipo}', nome_pet='{novo_nome}', idade='{nova_idade}' WHERE id={n}
                                """
                                curs3.execute(data_update)
                                conn.commit()
                                flag = True
                            
                            # Retorna um erro e volta para tela inicial
                            # caso valor 'idade' não seja válido
                            else:
                                print("Valor inválido, digite um número no campo idade!")
                                input("\nPresione ENTER")
                                continue
                        
                    # Retorna um erro e volta para tela inicial
                    # caso valor id não exista na lista
                    if not flag:
                        print("Valor inválido, digite um Id válido!")
                        input("\nPresione ENTER")
                        continue
                            
                os.system(comando)              # Limpa a tela
                print("Dados atualizados!")     # Exibe mensagem caso haja sucesso 
                input("\nPresione ENTER")       # Pausa o loop para a leitura da mensagem
        
            # Condição para Excluir um Pet
            elif escolha == '4':
                os.system(comando)  # Limpa a tela
                print("-- Excluir Pet --\n")
                
                lista_dados = []    # Lista para captura de dados do Banco
                lista_ids = []      # Lista para captura dos ids do Banco

                # Tentativa de consulta dos valores
                # do Banco de Dados
                try:
                    curs4.execute('SELECT * FROM petshop')
                    data = curs4.fetchall()

                    # Insere os valores do Banco
                    # dentro da lista 'lista_dados'
                    for dt in data:
                        lista_dados.append(dt)

                    # Gera um DataFrame com os dados da lista
                    dados_df = pd.DataFrame.from_records(lista_dados, columns=['Id', 'Tipo', 'Nome', 'Idade'])
                    
                    # Insere os ids do Banco
                    # dentro da lista 'lista_ids'
                    for indice, item in dados_df['Id'].items():
                        lista_ids.append(item)

                # Captura qualquer exceção no processo
                # de consulta dos valores
                except Exception as e:
                    print("Erro: ", e)
                    input("\nPresione ENTER")
                    continue
                
                # Exibe uma mensagem caso o DataFrame
                # esteja vazio
                if dados_df.empty:
                    print("Não há animais cadastrados.")
                    input("\nPresione ENTER")
                    continue
                else:
                    print(dados_df)                     # Exibe os dados do Banco
                    print("\nDigite para [S]air")       # Informa ao usuário como retornar a tela incial
                    pet_id = input("Escolha um Id: ")   # Permite o usuário escolher um Pet
                
                    if pet_id.isdigit():
                        os.system(comando)      # Limpa a tela
                        pet_id = int(pet_id)    # Converte variavel para um int
                        flag = False            # Gera uma variavel para verificação

                        # Laço que percorre lista de ids
                        for n in lista_ids:

                            # Checa se o valor digitado
                            # está na lista de ids
                            if n == pet_id:
                                data_delete = f"""
                                DELETE FROM petshop WHERE id={n}
                                """
                                curs4.execute(data_delete)
                                conn.commit()
                                flag = True
                        
                        # Retorna um erro e volta para tela inicial
                        # caso valor id não exista na lista
                        if not flag:
                            print("Valor inválido, digite um Id válido!")
                            input("\nPresione ENTER")
                            continue
                        
                        # Condição que checa se o último
                        # valor da lista foi deletado
                        if len(lista_ids) == 1:
                            data_reset_ids = """ ALTER TABLE petshop MODIFY(ID GENERATED AS IDENTITY (START WITH 1)) """
                            curs4.execute(data_reset_ids)
                            conn.commit()

                    else:
                        # Condição que permite ao usuário
                        # retornar a tela incial
                        if pet_id.upper() == 'S':
                            continue
                        
                        # Condição que checa se o valor digitado
                        # é um numero, caso contrario exibe uma mensagem
                        # e retorna para a tela inicial
                        else:
                            os.system(comando)
                            print("Valor inválido, digite um número!")
                            input("\nPresione ENTER")
                            continue

                os.system(comando)          # Limpa a tela
                print("Pet deletado!")      # Exibe mensagem caso haja sucesso
                input("\nPresione ENTER")   # Pausa o loop para a leitura da mensagem

            # Condição para Sair do Programa
            elif escolha == '5':
                os.system(comando)              # Limpa a tela
                print("Saindo do programa...")  # Exibe mensagem de saída
                input("Presione ENTER")         # Pausa o loop para a leitura da mensagem
                conn.close()                    # Fecha a conexão com o Banco de Dados
                break                           # Quebra o loop "while"
            
            # Condição de exibe mensagem de erro
            # e retorna para a tela incial, caso
            # valor digitado não seja válido
            else:
                os.system(comando)
                print("Valor incorreto, por favor uma das opções mostrada (digite o número)!")
                input("Presione ENTER")

# Captura de exceção para
# tentativa de conexão com
# o Banco de Dados
except Exception as ex:
    print("Ocorreu um erro...")
    print("Erro: ", ex)
