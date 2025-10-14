from flask import Flask, render_template, request, redirect, url_for
from flask import Response
from infra.repository.analistas_repository import AnalistaRepository
from infra.repository.leiloeiros_repository import LeiloeiroRepository
from infra.repository.salvados_repository import SalvadoRepository
from infra.repository.status_opcoes_repository import StatusOpcaoRepository
from infra.repository.despesas_repository import DespesaRepository
from infra.entities.analista import Analista
from infra.entities.salvado import Salvado
from infra.entities.leiloeiro import Leiloeiro
from infra.entities.despesa import Despesa
from infra.entities.status_opcao import StatusOpcao
from infra.configs.connection import DBConecctionHandleMaster
from infra.configs.connection import DBConecctionHandleMasterAutocommit
from infra.configs.connection import DBConecctionHandleApp
from sqlalchemy import text
from sqlalchemy_utils import database_exists, create_database
from infra.utils.formatters import strftime_filter, currency_filter

app = Flask(__name__)


app.jinja_env.filters['strftime'] = strftime_filter
app.jinja_env.filters['currency'] = currency_filter


conn_master_handle = DBConecctionHandleMaster()
engine_master = conn_master_handle.get_engine_master()
conn_master_autocommit_handle = DBConecctionHandleMasterAutocommit()
engine_master_autocommit = conn_master_autocommit_handle.get_engine_master()

if not database_exists(engine_master.url.set(database="salvados")):
    create_database(
        engine_master_autocommit.url.set(database="salvados"))


conn_app_handle = DBConecctionHandleApp()

# Criando as tabelas do banco 'salvados' explicitamente se não existir
engine_app = conn_app_handle.get_engine_app()

# Criando a tabela 'analistas' explicitamente se não existir
Analista.__table__.create(engine_app, checkfirst=True)

# Criando a tabela 'leiloeiros' explicitamente se não existir
Leiloeiro.__table__.create(engine_app, checkfirst=True)

# Criando a tabela 'salvados' explicitamente se não existir
Salvado.__table__.create(engine_app, checkfirst=True)

# Criando a tabela 'status_opcoes' explicitamente se não existir
StatusOpcao.__table__.create(engine_app, checkfirst=True)

# Criando a tabela 'despesas' explicitamente se não existir
Despesa.__table__.create(engine_app, checkfirst=True)

# Inicializando repositórios para utilizar os métodos existentes nas rotas
salvado_repo = SalvadoRepository()
status_repo = StatusOpcaoRepository()
analista_repo = AnalistaRepository()
leiloeiro_repo = LeiloeiroRepository()
despesa_repo = DespesaRepository()


@app.route('/')
def index():
    erro_modal = request.args.get('erro_modal')
    filtros = {
        'sinistro': request.args.get('sinistro'),
        'placa': request.args.get('placa'),
        'apolice': request.args.get('apolice'),
        'nome_segurado': request.args.get('segurado'),
        'analista_responsavel': request.args.get('analista'),
        'leiloeiro': request.args.get('leiloeiro'),
        'status': request.args.get('status'),
        'nome_terceiro': request.args.get('terceiro')
    }
    salvados = salvado_repo.get_salvados_filtrados(**filtros)

    possui_filtro = any(f for f in filtros.values() if f is not None)

    if not salvados and possui_filtro:
        erro_modal = "Não existem salvados para o filtro aplicado."

    status_opcoes = [s.nome for s in status_repo.get_all_status_opcoes()]
    analistas_opcoes = [a.nome for a in analista_repo.get_all_analistas()]
    leiloeiros_opcoes = [l.nome for l in leiloeiro_repo.get_all_leiloeiros()]
    return render_template('index.html', salvados=salvados, status_opcoes=status_opcoes,
                           analistas_opcoes=analistas_opcoes, leiloeiros_opcoes=leiloeiros_opcoes, erro_modal=erro_modal)


@app.route('/salvado', methods=['GET', 'POST'])
def salvado():
    status_opcoes = [s.nome for s in status_repo.get_all_status_opcoes()]
    analistas_opcoes = [a.nome for a in analista_repo.get_all_analistas()]
    leiloeiros_opcoes = [l.nome for l in leiloeiro_repo.get_all_leiloeiros()]
    errors = {}
    form_data = {}
    erro_modal = None
    sucesso = None

    if request.method == 'POST':
        # Pegar os campos do formulário
        form_data = {key: request.form.get(
            key, '') for key in Salvado.__table__.columns.keys() if key != 'id'}
        required_fields = ['status', 'sinistro', 'apolice', 'data_recebimento_salvado', 'data_pedido_cotacao_remocao',
                           'nome_segurado', 'nome_terceiro', 'placa', 'marca', 'modelo', 'ano', 'analista_responsavel']
        for field in required_fields:
            if not form_data[field] or form_data[field].strip() == '':
                errors[field] = True
        if not errors:
            # Converta campos numéricos
            for key in ['valor_fipe', 'valor_total_indenizacao', 'franquia_outros_descontos', 'valor_pago_pela_cia',
                        'valor_nf_entrada', 'valor_nf_saida', 'valor_venda']:
                value = form_data.get(key, '').strip()
                if value and value.lower() != 'none':
                    try:
                        form_data[key] = float(value.replace(',', '.'))
                    except ValueError:
                        form_data[key] = None
                else:
                    form_data[key] = None
            sucesso = salvado_repo.add_salvado(**form_data)

            if not sucesso:
                erro_modal = "Já Existe Salvado Cadastrado com esta Placa!"
                return render_template('salvado_form.html', status_opcoes=status_opcoes, analistas_opcoes=analistas_opcoes,
                                       leiloeiros_opcoes=leiloeiros_opcoes, salvado=None, form_data=form_data, errors=errors,
                                       error_messages=[], erro_modal=erro_modal)
            return redirect(url_for('index'))
        error_messages = [field for field in errors.keys()]
        return render_template('salvado_form.html', status_opcoes=status_opcoes, analistas_opcoes=analistas_opcoes,
                               leiloeiros_opcoes=leiloeiros_opcoes, salvado=None, form_data=form_data, errors=errors,
                               error_messages=error_messages, erro_modal=erro_modal)
    return render_template('salvado_form.html', status_opcoes=status_opcoes, analistas_opcoes=analistas_opcoes,
                           leiloeiros_opcoes=leiloeiros_opcoes, salvado=None, form_data=form_data, errors=errors,
                           error_messages=[], erro_modal=erro_modal)


@app.route('/detalhes/<int:id>')
def detalhes(id):
    salvado = salvado_repo.get_salvado_by_id(id)
    despesas = despesa_repo.get_despesas_por_salvado(id)
    return render_template('salvado_detalhes.html', salvado=salvado, despesas=despesas)


@app.route('/despesas_listagem', methods=['GET', 'POST'])
def despesas_listagem():
    erro_modal = request.args.get('erro_modal')
    filtros = {
        'fornecedor': request.form.get('fornecedor') if request.method == 'POST' else request.args.get('fornecedor'),
        'ocorrencia': request.form.get('ocorrencia') if request.method == 'POST' else request.args.get('ocorrencia'),
        'placa': request.form.get('placa') if request.method == 'POST' else request.args.get('placa'),
        'sinistro': request.form.get('sinistro') if request.method == 'POST' else request.args.get('sinistro'),
    }
    despesas = despesa_repo.get_despesas_filtradas(**filtros)

    possui_filtro = any(f for f in filtros.values() if f)

    if not despesas and possui_filtro:
        erro_modal = "Não existem despesas para o filtro aplicado."

    return render_template('despesas_listagem.html', despesas=despesas, erro_modal=erro_modal)


@app.route('/exportar_despesas')
def exportar_despesas():
    filtros = {
        'fornecedor': request.args.get('fornecedor'),
        'ocorrencia': request.args.get('ocorrencia'),
        'data': request.args.get('data'),
        'placa': request.args.get('placa'),
        'sinistro': request.args.get('sinistro'),
    }
    despesas = despesa_repo.get_despesas_filtradas(**filtros)

    if not despesas:
        possui_filtro = any(f for f in filtros.values() if f is not None)
        if possui_filtro:
            mensagem_retorno_erro = "Não existe despesas listadas para exportar."
        else:
            mensagem_retorno_erro = "Não existe despesas cadastradas no BD para exportar."
        return redirect(url_for('despesas_listagem', erro_modal=mensagem_retorno_erro))

    # Cabeçalho do CSV
    csv_data = "sinistro,placa,fornecedor,Tipo de Despesa,valor,data,observacao\n"
    for d in despesas:
        csv_data += f"{d.salvado.sinistro},{d.salvado.placa},{d.fornecedor},{d.ocorrencia},{d.valor},{d.data},{d.observacao}\n"
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=despesas.csv"}
    )


@app.route('/atualizar/<int:id>', methods=['GET', 'POST'])
def atualizar(id):
    salvado = salvado_repo.get_salvado_by_id(id)
    status_opcoes = [s.nome for s in status_repo.get_all_status_opcoes()]
    analistas_opcoes = [a.nome for a in analista_repo.get_all_analistas()]
    leiloeiros_opcoes = [l.nome for l in leiloeiro_repo.get_all_leiloeiros()]
    errors = {}
    form_data = {}
    erro_modal = None
    sucesso = None
    despesas = despesa_repo.get_despesas_por_salvado(id)

    if request.method == 'POST':
        form_data = {key: request.form.get(
            key, '') for key in Salvado.__table__.columns.keys() if key != 'id'}
        # Converta campos numéricos
        float_fields = ['valor_fipe', 'valor_total_indenizacao', 'franquia_outros_descontos', 'valor_pago_pela_cia',
                        'valor_nf_entrada', 'valor_nf_saida', 'valor_venda']
        for key in float_fields:
            value = form_data.get(key, '').replace(
                'R$', '').replace('.', '').replace(',', '.').strip()
            if value and value.lower() != 'none':
                try:
                    form_data[key] = float(value)
                except ValueError:
                    form_data[key] = None
            else:
                form_data[key] = None
        sucesso = salvado_repo.update_salvado(id, **form_data)
        if not sucesso:
            erro_modal = "Já Existe Salvado Cadastrado com esta Placa!"
            return render_template('salvado_form.html', status_opcoes=status_opcoes, analistas_opcoes=analistas_opcoes,
                                   leiloeiros_opcoes=leiloeiros_opcoes, salvado=salvado, form_data=form_data, errors=errors,
                                   error_messages=[], erro_modal=erro_modal, despesas=despesas)
        return redirect(url_for('index'))
    else:
        form_data = {key: getattr(salvado, key, '')
                     for key in Salvado.__table__.columns.keys() if key != 'id'}
    return render_template('salvado_form.html', salvado=salvado,
                           status_opcoes=status_opcoes,
                           analistas_opcoes=analistas_opcoes,
                           leiloeiros_opcoes=leiloeiros_opcoes,
                           errors=errors, form_data=form_data, error_messages=[], erro_modal=erro_modal, despesas=despesas)


@app.route('/exportar_salvados')
def exportar_salvados():
    filtros = {
        'sinistro': request.args.get('sinistro'),
        'placa': request.args.get('placa'),
        'apolice': request.args.get('apolice'),
        'nome_segurado': request.args.get('segurado'),
        'analista_responsavel': request.args.get('analista'),
        'leiloeiro': request.args.get('leiloeiro'),
        'status': request.args.get('status'),
        'nome_terceiro': request.args.get('terceiro')
    }
    salvados = salvado_repo.get_salvados_filtrados(**filtros)
    if not salvados:
        possui_filtro = any(f for f in filtros.values() if f is not None)
        if possui_filtro:
            mensagem_retorno_erro = "Não existe salvados listados para exportar."
        else:
            mensagem_retorno_erro = "Não existe salvados cadastrados no BD para exportar."
        return redirect(url_for('index', erro_modal=mensagem_retorno_erro))
    # Gere o CSV
    csv_data = "id,status,sinistro,apolice,analista_responsavel,data_entrada_salvado,placa\n"
    for s in salvados:
        csv_data += f"{s.id},{s.status},{s.sinistro},{s.apolice},{s.analista_responsavel},{s.data_recebimento_salvado},{s.placa}\n"
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=salvados.csv"}
    )


@app.route('/gerenciar', methods=['GET', 'POST'])
def gerenciar():
    secao = request.args.get('secao', 'status')
    erro_modal = None
    sucesso = None

    if request.method == 'POST':
        acao = request.form['acao']
        if secao == 'status':
            if acao == 'inserir':
                sucesso = status_repo.add_status(request.form['novo_status'])
                if sucesso:
                    erro_modal = "Status Cadastrado com Sucesso!"
                if not sucesso:
                    erro_modal = "Status já Cadastrado!"
            elif acao == 'excluir':
                status_repo.delete_status(request.form['status_id'])
            elif acao == 'alterar':
                sucesso = status_repo.update_status(
                    request.form['status_id'], request.form['novo_nome'])
                if sucesso:
                    erro_modal = "Leiloeiro Cadastrado com Sucesso!"
                if not sucesso:
                    erro_modal = "Leiloeiro já Cadastrado!"
        elif secao == 'analistas':
            if acao == 'inserir':
                sucesso = analista_repo.add_analista(
                    request.form['nome'], request.form['email'], request.form['cargo'])
                if sucesso:
                    erro_modal = "Analista Cadastrado com Sucesso!"
                if not sucesso:
                    erro_modal = "Analista já Cadastrado!"
            elif acao == 'excluir':
                analista_repo.delete_analista(request.form['analista_id'])
            elif acao == 'alterar':
                sucesso = analista_repo.update_analista(
                    request.form['analista_id'], request.form['nome'], request.form['email'], request.form['cargo'])
                if sucesso:
                    erro_modal = "Analista Cadastrado com Sucesso!"
                if not sucesso:
                    erro_modal = "Analista já Cadastrado!"
        elif secao == 'leiloeiros':
            if acao == 'inserir':
                sucesso = leiloeiro_repo.add_leiloeiro(
                    request.form['nome'], request.form['endereco'], request.form['telefone'],
                    request.form['responsavel'], request.form['email'])
                if sucesso:
                    erro_modal = "Leiloeiro Cadastrado com Sucesso!"
                if not sucesso:
                    erro_modal = "Leiloeiro já Cadastrado!"
            elif acao == 'excluir':
                leiloeiro_repo.delete_leiloeiro(request.form['leiloeiro_id'])
            elif acao == 'alterar':
                sucesso = leiloeiro_repo.update_leiloeiro(
                    request.form['leiloeiro_id'], request.form['nome'], request.form['endereco'],
                    request.form['telefone'], request.form['responsavel'], request.form['email'])
                if sucesso:
                    erro_modal = "Leiloeiro Cadastrado com Sucesso!"
                if not sucesso:
                    erro_modal = "Leiloeiro já Cadastrado!"
    status_opcoes = [(s.id, s.nome)
                     for s in status_repo.get_all_status_opcoes()]
    analistas = [(a.id, a.nome, a.email, a.cargo)
                 for a in analista_repo.get_all_analistas()]
    leiloeiros = [(l.id, l.nome, l.endereco, l.telefone, l.responsavel, l.email)
                  for l in leiloeiro_repo.get_all_leiloeiros()]
    return render_template('gerenciar.html', status_opcoes=status_opcoes, analistas=analistas,
                           leiloeiros=leiloeiros, secao=secao, erro_modal=erro_modal, sucesso=sucesso)


@app.route('/despesas/<int:id>', methods=['GET', 'POST'])
def despesas(id):
    salvado = salvado_repo.get_salvado_by_id(id)
    despesas = despesa_repo.get_despesas_por_salvado(id)
    if request.method == 'POST':
        despesa_data = {
            'salvado_id': id,
            'fornecedor': request.form.get('fornecedor'),
            'data': request.form.get('data'),
            'ocorrencia': request.form.get('ocorrencia'),
            'valor': float(request.form.get('valor', 0)),
            'observacao': request.form.get('observacao')
        }
        despesa_repo.add_despesa(**despesa_data)
        return redirect(url_for('despesas', id=id))
    return render_template('despesas.html', salvado=salvado, despesas=despesas)


@app.route('/incluir_despesa/<int:salvado_id>', methods=['POST'])
def incluir_despesa(salvado_id):
    # Pega os dados do formulário
    form = request.form
    despesa_data = {
        'salvado_id': salvado_id,
        'fornecedor': form.get('fornecedor'),
        'data': form.get('data'),
        'ocorrencia': form.get('ocorrencia'),
        'valor': float(form.get('valor', 0)),
        'observacao': form.get('observacao')
    }
    despesa_repo.add_despesa(**despesa_data)
    return redirect(url_for('despesas', id=salvado_id))


if __name__ == '__main__':
    app.run(debug=True)
