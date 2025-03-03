import streamlit as st
import time
import json
import os
from datetime import date, datetime
from datetime import time as tm
from dateutil.relativedelta import relativedelta
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
Banco_de_Medicos = "DataBase/Medicos.json"
Consulta = "DataBase/Consulta.json"

#Funções para carregar os aquivos locais
def load_user_db():
    if os.path.exists(Banco):
        with open(Banco, "r") as file:
            return json.load(file)
    return {}
def load_doctor_db():
    if os.path.exists(Banco_de_Medicos):
        with open(Banco_de_Medicos, "r") as file:
            return json.load(file)
    return {}
def load_consultation_db():
    if os.path.exists(Consulta):
        with open(Consulta, "r") as file:
            return json.load(file)
    return {}

#Funções para salvar os arquivos da execução
def save_user_db(user_db):
    with open(Banco, "w") as file:
        json.dump(user_db, file, indent=4)
def save_doctor_db(doctor_db):
    with open(Banco_de_Medicos, "w") as file:
        json.dump(doctor_db, file, indent=4)
def save_consultation_db(consultation_db):
    with open(Consulta, "w") as file:
        json.dump(consultation_db, file, indent=4)

#Funções para iniciar o banco de dados
if "user_db" not in st.session_state:
    st.session_state["user_db"] = load_user_db()
if "doctor_db" not in st.session_state:
    st.session_state["doctor_db"] = load_doctor_db()
if "consultation_db" not in st.session_state:
    st.session_state["consultation_db"] = load_consultation_db()

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
    st.session_state["authenticated"] = True
    st.session_state["Nome"] = Nome
    st.session_state["is_doctor"] = False   
    return True, "Usuário registrado com sucesso!"

def Change_data(Nome, Senha, Data_Nascimento, Morada, Localidade, Codigo_Postal, Numero, Email_Seguradora, Numero_Resp,Nova_Biografia,Novo_grupo_sanguineo, Conta):
    if Nome not in st.session_state["user_db"]:
        return False, "Usuário não encontrado!"
    #Atualizar o Dicionário que armazenas as informaçoes do usuário
    # Obter os dados antigos
    user_data = st.session_state["user_db"][Nome]

    # Atualizar apenas os campos preenchidos
    user_data["Senha"] = Senha if Senha else user_data.get("Senha")
    user_data["Data_Nascimento"] = str(Data_Nascimento) if Data_Nascimento else user_data.get("Data_Nascimento")
    user_data["Morada"] = Morada if Morada else user_data.get("Morada")
    user_data["Localidade"] = Localidade if Localidade else user_data.get("Localidade")
    user_data["Codigo_Postal"] = Codigo_Postal if Codigo_Postal else user_data.get("Codigo_Postal")
    user_data["Numero"] = str(Numero) if Numero else user_data.get("Numero", "")
    user_data["Email_Seguradora"] = Email_Seguradora if Email_Seguradora else user_data.get("Email_Seguradora")
    user_data["Numero_Resp"] = str(Numero_Resp) if Numero_Resp else user_data.get("Numero_Resp", "")
    user_data["Biografia"] = str(Nova_Biografia) if Nova_Biografia else user_data.get("Biografia")
    user_data["Conta"] = bool(Conta) if Conta is not None else user_data.get("Conta", False)

    # Salvar no banco de dados
    save_user_db(st.session_state["user_db"])
    
    return True, "Dados do Usuário Alterados com sucesso!"

def Change_doctor_data(Nome, Senha, Especialidade, Telefone, Email):
    if Nome not in st.session_state["doctor_db"]:
        return False, "Medico não encontrado!"
    doctor_data = st.session_state["doctor_db"][Nome]

    # Atualizar apenas os campos preenchidos
    doctor_data["Senha"] = Senha if Senha else doctor_data.get("Senha")
    doctor_data["Especialidade"] = str(Especialidade) if Especialidade else doctor_data.get("Especialidade")
    doctor_data["Telefone"] = str(Telefone) if Telefone else doctor_data.get("Telefone", "")
    doctor_data["Email"] = Email if Email else doctor_data.get("Email")

    # Salvar no banco de dados
    save_doctor_db(st.session_state["doctor_db"])
    
    return True, "Dados do Medico Alterados com sucesso!"

#Função para logar usuarios
def login_(Nome, Senha):
    user_db = st.session_state["user_db"]
    doctor_db = st.session_state["doctor_db"]
    
    # Verifica se é um usuário normal
    if Nome in user_db and user_db[Nome]['Senha'] == Senha:
        st.session_state["authenticated"] = True
        st.session_state["Nome"] = Nome
        st.session_state["is_doctor"] = False
        return True, "Logado com sucesso"

    # Verifica se é um médico
    if Nome in doctor_db and doctor_db[Nome]['Senha'] == Senha:
        st.session_state["authenticated"] = True
        st.session_state["Nome"] = Nome
        st.session_state["is_doctor"] = True
        return True, "Logado com sucesso como Médico"

    return False, "Nome ou Senha incorretos"

# Estado de autenticação
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def register_doctor(Nome, Senha, Especialidade, Telefone, Email):
    if Nome in st.session_state["doctor_db"]:
        return False, st.error("Medico já registrado!")
    
    # Criar um dicionário para armazenar todas as informações do usuário
    st.session_state["doctor_db"][Nome] = {
        "Senha": Senha,
        "Especialidade": str(Especialidade),  # Converter data para string
        "Telefone": str(Telefone)  if Telefone else "",
        "Email": Email,   
    }
    st.session_state["is_doctor"] = True
    save_doctor_db(st.session_state["doctor_db"]) 
    return True, "Medico registrado com sucesso!"

def show_medicos():
    st.header("Destaques", divider=True)
    medicos = st.session_state.get("doctor_db", {})

    if not medicos:
        st.info("Nenhum médico registrado ainda.")
        return

    # Criar um dicionário {índice: especialidade}
    option_map = {i: dados["Especialidade"] for i, (_, dados) in enumerate(medicos.items())}
    
    selection = st.pills("Escolha uma especialidade", options=option_map.keys(), format_func=lambda i: option_map[i], selection_mode="single")

    if selection is not None:
        especialidade = option_map[selection]

        # Buscar o primeiro médico com essa especialidade
        for nome, dados in medicos.items():
            if dados["Especialidade"] == especialidade:
                st.write(f"**Nome:** {nome}")
                st.write(f"**Especialidade:** {especialidade}")

                if st.session_state.get("authenticated", False):
                    data = st.date_input(f"Selecione a data para consulta com {nome}", min_value=date.today(), max_value=date.today() + relativedelta(months=3))
                    hora = st.time_input(f"Selecione o horário para consulta com {nome}", tm(0, 0))

                    if tm(8, 0) <= hora <= tm(19, 0):
                        if st.button("Marcar consulta"):
                            success, msg = marcar_consulta(st.session_state.get("Nome", "Paciente"), nome)
                            st.success(msg) if success else st.error(msg)
                    else:
                        st.info("A consulta deve ser marcada entre 08:00 e 19:00.")
                break  # Sai do loop após encontrar o primeiro médico

                        

def show_all():
    st.header("Visão Geral", divider=True)
    medicos = st.session_state.get("doctor_db", {})
    conta = st.session_state.get("user_db", {})
    if not medicos:
        st.info("Nenhum médico registrado ainda.")
        return
    if not conta:
        st.info("Nenhuma conta Registrada")   
    col1, col2 = st.columns(2)       
    with col1:
        st.write("### Médicos:")
        for nome, dados in medicos.items():  
            st.write(f"**Nome:** {nome}")   
    with col2:
        st.write("### Usuários:")
        for nome, dados in conta.items():  
            st.write(f"**Nome:** {nome}")
        
def marcar_consulta(nome_paciente, nome_medico, data, hora):
    consultas = load_consultation_db()
    
    # Garantir que a chave "consultas" existe
    if "consultas" not in consultas:
        consultas["consultas"] = []

    # Gerar um ID único para a consulta
    consulta_id = str(len(consultas["consultas"]) + 1)

    # Criar a nova consulta
    nova_consulta = {
        "consulta_id": consulta_id,
        "paciente": nome_paciente,
        "medico": nome_medico,
        "data": str(data),
        "hora": str(hora),
        "status": "pendente",
        "dados_paciente": {
            "nome": nome_paciente,
            "telefone": st.session_state["user_db"][nome_paciente].get("Numero", "Não informado"),
            "email": st.session_state["user_db"][nome_paciente].get("Email_Seguradora", "Não informado")
        }
    }
    # Adicionar consulta ao banco de dados
    consultas["consultas"].append(nova_consulta)
    save_consultation_db(consultas)
    return True, f"Consulta com Dr. {nome_medico} marcada para {data} às {hora}."

def show_consultation():
    consultas = load_consultation_db()
    medico = st.session_state["Nome"]

    if "consultas" not in consultas or not consultas["consultas"]:
        st.info("Nenhuma consulta encontrada.")
        return

    # Filtra as consultas para o médico logado
    consultas_do_medico = [consulta for consulta in consultas["consultas"] if consulta["medico"] == medico]

    if not consultas_do_medico:
        st.info("Nenhuma consulta agendada para você.")
        return

    for consulta in consultas_do_medico:
        with st.expander(f"Consulta ID: {consulta['consulta_id']} - Paciente: {consulta['paciente']}"):
            st.write(f"**Data:** {consulta['data']}")
            st.write(f"**Hora:** {consulta['hora']}")
            st.write(f"**Status:** {consulta['status']}")
            st.write(f"**Telefone:** {consulta['dados_paciente']['telefone']}")
            st.write(f"**Email:** {consulta['dados_paciente']['email']}")
            
            novo_telefone = st.text_input("Novo telefone", value=consulta["dados_paciente"].get("telefone", ""))
            novo_email = st.text_input("Novo email", value=consulta["dados_paciente"].get("email", ""))
            
            if st.button(f"Atualizar dados de {consulta['paciente']}", key=f"update_{consulta['consulta_id']}"):
                consulta["dados_paciente"]["telefone"] = novo_telefone
                consulta["dados_paciente"]["email"] = novo_email
                save_consultation_db(consultas)
                st.success("Dados do paciente atualizados com sucesso!")
                st.rerun()

    


#Interface
left, middle, right = st.columns(3, vertical_alignment="bottom")#Posicionamento H os widgets
middle.write("### Sistema Hospitalar BM.ao")
st.subheader("",divider=True)

if not st.session_state["authenticated"]:
    tab1, tab2,tab3 = st.tabs(["Login", "Registrar","Destaques"],)

    with tab1:
        left, middle, right = st.columns(3, vertical_alignment="bottom")
        st.subheader("Login",divider=True)
        Nome = st.text_input("Usuário")
        Senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            success, message = login_(Nome, Senha)
            st.success(message)
            time.sleep(2)
            st.rerun()

    with tab2:
        left, middle, right = st.columns(3, vertical_alignment="bottom")
        st.subheader("Registrar",divider=True)
        Novo_Nome = st.text_input("Novo Usuário")
        Nova_Senha = st.text_input("Nova Senha", type="password", key="nova_senha_registro")
        Nova_Data = st.date_input("Data de Nascimento", value=None, min_value=date(1926,1,1),max_value=date.today())
        Nova_Morada = st.text_input("Morada")
        Nova_Localidade = st.text_input("Localidade")
        Nova_Codigo_Postal = st.text_input("Codigo Postal",)
        Novo_Numero = st.text_input("Numero de telefone", value=None)
        Novo_Email_Da_Seguradora = st.text_input("Email Da Entidade Financeira Responsavel",)
        Novo_Numero_Resp = st.text_input("Numero do Responsavel", value=None)
        Nova_Biografia = st.text_input("Biografia")
        Novo_Genero = st.selectbox("Qual é o seu Genero?", ("Masculino","Feminino"),index=None, placeholder="Escolha uma opção...")
        Novo_grupo_sanguineo = st.selectbox("Qual é o seu grupo sanguineo?", ("A-","B-","AB-","O-","A+","B+","AB+","O+"),index=None, placeholder="Escolha uma opção...")
        Nava_Alergia = st.text_input("Você possuir alguma alergia?")
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
            if not Novo_Nome or not Nova_Senha or not Nova_Data or not Nova_Morada or not Nova_Localidade or not Nova_Codigo_Postal or not Novo_Numero or not Novo_Email_Da_Seguradora or not Novo_Numero_Resp:
                st.error("Todos os campos são obrigatórios! Preencha todos antes de continuar.")
            else:
                success, message = register_user(
                Novo_Nome, Nova_Senha, Nova_Data, Nova_Morada, 
                Nova_Localidade, Nova_Codigo_Postal, Novo_Numero, 
                Novo_Email_Da_Seguradora, Novo_Numero_Resp,Nova_Biografia,Novo_grupo_sanguineo,Conta
            )
                st.success(message) if success else st.error(message)
                time.sleep(2)
                st.rerun()

    with tab3:
        show_medicos()

else:
    if st.session_state["is_doctor"]:
        Perfil_Medico,Detalhes,Alterar_Dados,Consultas = st.tabs(["Perfil","Destaques","Alterar_Dados","Consultas"],)

        with Perfil_Medico:
            if "Nome" in st.session_state and st.session_state["Nome"] in st.session_state["doctor_db"]:
                usuario = st.session_state["doctor_db"][st.session_state["Nome"]]
                st.header("Perfil", divider=True)
                st.subheader(":material/person: Informações Pessoais")
                st.write(f"**Nome:** {st.session_state['Nome']}")
                st.write(f"**Especialidade:** {usuario['Especialidade']}")
                st.write(f"**Telefone:** {usuario['Telefone']}")
                st.write(f"**Email:** {usuario['Email']}")

            else:
                st.error("Medico não encontrado!") 

        with Consultas:
            show_consultation()

        with Alterar_Dados:
            st.write(f"### **Nome:** {st.session_state['Nome']}")
            Nova_Senha = st.text_input("Nova Senha", type="password", key="registro")
            Nova_Especialidade = st.text_input("Especialidade", value=None)
            Novo_Telefone = st.text_input("Numero de telefone", value=None, key="telefone_registro")
            Novo_Email= st.text_input("Email Do Medico",)
                
            if st.button("Actualizar Dados"):

                if not Nova_Senha or not Nova_Especialidade or not Novo_Telefone or not Novo_Email:
                    st.error("Todos os campos são obrigatórios! Preencha todos antes de continuar.")
                else:
                    success, message = Change_doctor_data(st.session_state["Nome"],Nova_Senha,Nova_Especialidade, Novo_Telefone, Novo_Email
                    )
                    st.success(message) if success else st.error(message)
                    time.sleep(2)
                    st.rerun()
            
    else:
        if st.session_state["user_db"][st.session_state["Nome"]]["Conta"]:
                tab1,tab2,tab3,tab4,tab5 = st.tabs(["Perfil","Destaques","Alterar_Dados","Visão geral","Registrar Medicos"],)
        else:
                tab1,tab2,tab3 = st.tabs(["Perfil","Destaques","Alterar_Dados"],)

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
                st.subheader(":material/call: Contato")
                st.write(f"**Telefone:** {st.session_state["user_db"][st.session_state["Nome"]]["Numero"]}")
                st.write(f"**Email Seguradora:** {st.session_state["user_db"][st.session_state["Nome"]]["Email_Seguradora"]}")
                st.write(f"**Número do Responsável:** {st.session_state["user_db"][st.session_state["Nome"]]["Numero_Resp"]}")
            else:
                    st.error("Usuário não encontrado!")

        with tab2:
            show_medicos()
        
        with tab3:
            st.subheader("Actualizar dados",divider=True)
            st.write(f"### **Nome:** {st.session_state['Nome']}")
            Nova_Senha = st.text_input("Nova Senha", type="password", key="nova_senha_atualizar")
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
        
        # Funções exclusivas para administradores, como gerenciar usuários
        if st.session_state["user_db"][st.session_state["Nome"]]["Conta"]:
            with tab5: 
                st.subheader("Registrar Medicos",divider=True)
                Novo_Nome = st.text_input("Novo Usuário")
                Nova_Senha = st.text_input("Nova Senha", type="password", key="nova_senha_registro")
                Nova_Especialidade = st.text_input("Especialidade", value=None)
                Novo_Telefone = st.text_input("Numero de telefone", value=None, key="telefone_registro")
                Novo_Email= st.text_input("Email Do Medico",)
                if st.button("Registrar Medico"):
                    success, message = register_doctor(Novo_Nome, Nova_Senha, Nova_Especialidade, Novo_Telefone, Novo_Email)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                        time.sleep(2)
                        st.rerun()
            
            with tab4:
                show_all()

    if st.button("Sair"):
        st.session_state["authenticated"] = False
        st.session_state["Nome"] = None
        st.rerun()

