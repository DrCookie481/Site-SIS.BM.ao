import streamlit as st
import time
import json
import os
from datetime import date
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="SIS BM.ao",
    page_icon="Images/Logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# Desenvolvedores: \n ### Feio Elegante \n ### Jonnhy Costa \n ### Orlando Teixeira \n ### Marco Pires \n ### Geraldo Xaluinza "
    }
)
st.logo("Images/Logo.png")

Banco = "DataBase/Banco_De_Dados.json" #Caminho do arquivo Local para armazenar dados

#Função para carregar os aquivos locais
def load_user_db():
    if os.path.exists(Banco):
        with open(Banco, "r") as file:
            return json.load(file)
    return {}


#Função para salvar os arquivos da execução
def save_user_db(user_db):
    with open(Banco, "w") as file:
        json.dump(user_db, file, indent=4)


#Função para iniciar o banco de dados
if "user_db" not in st.session_state:
    st.session_state["user_db"] = load_user_db()




def register_user(Nome, Senha, Data_Nascimento, Morada, Localidade, Codigo_Postal, Numero, Email_Seguradora, Numero_Resp,Nova_Biografia, Conta):
    if Nome in st.session_state["user_db"]:
        return False, "Usuário já existe!"
    
    # Criar um dicionário para armazenar todas as informações do usuário
    st.session_state["user_db"][Nome] = {
        "Senha": Senha,
        "Data_Nascimento": str(Data_Nascimento),  # Converter data para string
        "Morada": Morada,
        "Localidade": Localidade,
        "Codigo_Postal": Codigo_Postal,
        "Numero": str(Numero),
        "Email_Seguradora": Email_Seguradora,
        "Numero_Resp": str(Numero_Resp),
        "Biografia": str(Nova_Biografia),
        "Conta": bool(Conta)
    }
    
    # Salvar no banco de dados
    save_user_db(st.session_state["user_db"])
    
    return True, "Usuário registrado com sucesso!"

def Change_data(Nome, Senha, Data_Nascimento, Morada, Localidade, Codigo_Postal, Numero, Email_Seguradora, Numero_Resp,Nova_Biografia, Conta):
    if Nome not in st.session_state["user_db"]:
        return False, "Usuário não encontrado!"
    #Atualizar o Dicionário que armazenas as informaçoes do usuário
    st.session_state["user_db"][Nome] = {
        "Senha": Senha,
        "Data_Nascimento": str(Data_Nascimento),  # Converter data para string
        "Morada": Morada,
        "Localidade": Localidade,
        "Codigo_Postal": Codigo_Postal,
        "Numero": str(Numero),
        "Email_Seguradora": Email_Seguradora,
        "Numero_Resp": str(Numero_Resp),
        "Biografia": str(Nova_Biografia),
        "Conta": bool(Conta)   
    }
    # Salvar no banco de dados
    save_user_db(st.session_state["user_db"])
    
    return True, "Dados do Usuário Alterados com sucesso!"



#Função para logar usuarios
def login_user(Nome, Senha):
    user_db = st.session_state["user_db"]
    if Nome in user_db and user_db[Nome]['Senha'] == Senha:
        st.session_state["authenticated"] = True
        st.session_state["Nome"] = Nome
        return True, st.success("Logado com sucesso")
    return False, st.error("Nome ou Senha incorretos")

# Estado de autenticação
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False



















#Interface
left, middle, right = st.columns(3, vertical_alignment="bottom")#Posicionamento H os widgets
middle.write("### Sistema Hospitalar BM.ao")
st.subheader("",divider=True)


col1, col2 = st.columns(2)#Posicionamento V os widgets

if not st.session_state["authenticated"]:
    tab1, tab2,tab3 = st.tabs(["Login", "Registrar","Destaques"],)

    with tab1:
        left, middle, right = st.columns(3, vertical_alignment="bottom")
        st.subheader("Login",divider=True)
        Nome = st.text_input("Usuário")
        Senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            success, message = login_user(Nome, Senha)
            st.success(message)
            time.sleep(2)
            st.rerun()

            

    with tab2:
        left, middle, right = st.columns(3, vertical_alignment="bottom")
        st.subheader("Registrar",divider=True)
        Novo_Nome = st.text_input("Novo Usuário")
        Nova_Senha = st.text_input("Nova Senha", type="password")
        Nova_Data = st.date_input("Data de Nascimento", value=None, min_value=date(1926,1,1),max_value=date.today())
        Nova_Morada = st.text_input("Morada")
        Nova_Localidade = st.text_input("Localidade")
        Nova_Codigo_Postal = st.text_input("Codigo Postal",)
        Novo_Numero = st.text_input("Numero de telefone", value=None)
        Novo_Email_Da_Seguradora = st.text_input("Email Da Entidade Financeira Responsavel",)
        Novo_Numero_Resp = st.text_input("Numero do Responsavel", value=None)
        Nova_Biografia = st.text_input("Biografia")
        Conta=False
        if st.checkbox("Conta Avançada"):
            cs = st.text_input("Código secreto")
            if cs=="O":
                st.success(f"A conta {Novo_Nome} tá no criativo")
                Conta=True
            elif cs=="":
                st.info("Por favor preencha o codigo secreto ou desmarque a caixa")
            else:
                st.error("Codigo incorreto")
                


        if st.button("Registrar"):
            success, message = register_user(
            Novo_Nome, Nova_Senha, Nova_Data, Nova_Morada, 
            Nova_Localidade, Nova_Codigo_Postal, Novo_Numero, 
            Novo_Email_Da_Seguradora, Novo_Numero_Resp,Nova_Biografia, Conta
        )
            st.success(message) if success else st.error(message)
            time.sleep(2)
            st.rerun()


    with tab3:
        st.header("Destaques", divider=True)
        
        medicos = [
            {"Nome": "Jorge", "Especialidade": "Cardiologista"},
            {"Nome": "Kauã", "Especialidade": "Fisioterapeuta"},
            {"Nome": "Paulo", "Especialidade": "Pediatra"}
                ]
                
        for medico in medicos:
            col1, col2 = st.columns([3, 1])
                    
            with col1:
                st.write(f"**Nome:** {medico['Nome']}")
                st.write(f"**Especialidade:** {medico['Especialidade']}")
                    
            #if st.session_state["authenticated"]:
                #with col2:
                    #if st.button(f"Marcar com {medico['Nome']}", key=medico["Nome"]):
                        #success, msg = marcar_consulta(st.session_state["Nome"], medico["Nome"])
                        #st.success(msg) if success else st.error(msg)
else:
    if st.session_state["user_db"][st.session_state["Nome"]]["Conta"]:
        tab1,tab2,tab3,tab4 = st.tabs(["Perfil","Destaques","Alterar_Dados","Registrar Medicos"],)
    else:
        tab1,tab2,tab3 = st.tabs(["Perfil","Destaques","Alterar_Dados"],)

    # Dentro da aba "Administração", mostre funcionalidades exclusivas
    if "Registrar Medicos" in st.session_state:
        with tab4:
        # Funções exclusivas para administradores, como gerenciar usuários
            pass



        
    with tab1:
        if "Nome" in st.session_state and st.session_state["Nome"] in st.session_state["user_db"]:
            usuario = st.session_state["user_db"][st.session_state["Nome"]]
            st.header("Perfil", divider=True)
            st.subheader(":material/person: Informações Pessoais")
            st.write(f"**Nome:** {st.session_state['Nome']}")
            st.write(f"**Data de Nascimento:** {usuario['Data_Nascimento']}")
            st.write(f"**Morada:** {usuario['Morada']}")
            st.write(f"**Localidade:** {usuario['Localidade']}")
            st.write(f"**Código Postal:** {usuario['Codigo_Postal']}")
            container = st.container(border=True)
            container.write(f"**{usuario['Biografia']}**")
        else:
            st.error("Usuário não encontrado!")

        



        st.subheader(":material/call: Contato")
        st.write(f"**Telefone:** {st.session_state["user_db"][st.session_state["Nome"]]["Numero"]}")
        st.write(f"**Email Seguradora:** {st.session_state["user_db"][st.session_state["Nome"]]["Email_Seguradora"]}")
        st.write(f"**Número do Responsável:** {st.session_state["user_db"][st.session_state["Nome"]]["Numero_Resp"]}")
        









        with tab2:
            st.header("Destaques", divider=True)
            
            medicos = [
                {"Nome": "Jorge", "Especialidade": "Cardiologista"},
                {"Nome": "Kauã", "Especialidade": "Fisioterapeuta"},
                {"Nome": "Paulo", "Especialidade": "Pediatra"}
            ]
            
            for medico in medicos:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Nome:** {medico['Nome']}")
                    st.write(f"**Especialidade:** {medico['Especialidade']}")
                
                #if st.session_state["authenticated"]:
                    #with col2:
                        #if st.button(f"Marcar com {medico['Nome']}", key=medico["Nome"]):
                            #success, msg = marcar_consulta(st.session_state["Nome"], medico["Nome"])
                            #st.success(msg) if success else st.error(msg)

    with tab3:
        st.subheader("Actualizar dados",divider=True)
        Novo_Nome = st.text_input("Novo Usuário", value=st.session_state["Nome"])
        Nova_Senha = st.text_input("Nova Senha", type="password")
        Nova_Data = st.date_input("Data de Nascimento", value=None, min_value=date(1926,1,1),max_value=date.today())
        Nova_Morada = st.text_input("Morada")
        Nova_Localidade = st.text_input("Localidade")
        Nova_Codigo_Postal = st.text_input("Codigo Postal",)
        Novo_Numero = st.text_input("Numero de telefone", value=None)
        Novo_Email_Da_Seguradora = st.text_input("Email Da Entidade Financeira Responsavel",)
        Novo_Numero_Resp = st.text_input("Numero do Responsavel", value=None)
        Nova_Biografia = st.text_input("Biografia")
        Conta = st.session_state["user_db"][st.session_state["Nome"]]["Conta"]
        if not Conta and st.checkbox("Conta Avançada"):
            cs = st.text_input("Código secreto")
            if cs == "O":
                st.success(f"A conta {st.session_state['Nome']} agora é avançada!")
                Conta = True
            else:
                st.error("Código incorreto")

                


        if st.button("Actualizar Dados"):
            success, message = Change_data(
            st.session_state["Nome"], Nova_Senha, Nova_Data, Nova_Morada, 
            Nova_Localidade, Nova_Codigo_Postal, Novo_Numero, 
            Novo_Email_Da_Seguradora, Novo_Numero_Resp,Nova_Biografia, Conta
        )
            st.success(message) if success else st.error(message)
            time.sleep(2)
            st.rerun()


    if st.button("Sair"):
        st.session_state["authenticated"] = False
        st.session_state["Nome"] = None
        st.rerun()

