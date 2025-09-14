from flask import Flask, render_template, request, redirect, url_for
from models import Salvado, Database
from datetime import datetime

app = Flask(__name__)
db = Database()

FIELD_NAMES = {
    'status': 'Status',
    'sinistro': 'Sinistro',
    'apolice': 'Apólice',
    'data_recebimento_salvado': 'Data Recebimento do Salvado',
    'data_pedido_cotacao_remocao': 'Data Pedido Cotação Remoção',
    'nome_segurado': 'Nome Segurado',
    'nome_terceiro': 'Nome Terceiro',
    'placa': 'Placa',
    'marca': 'Marca',
    'modelo': 'Modelo',
    'ano': 'Ano'
}


def strftime_filter(value, format_string):
    if value and isinstance(value, (datetime, str)):
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                return value
        return value.strftime(format_string)
    return ''


def currency_filter(value):
    if value is None or value == '':
        return ''
    try:
        value = float(value)
        return f"R$ {value:,.2f}".replace('.', '#').replace(',', '.').replace('#', ',')
    except (ValueError, TypeError):
        return value


app.jinja_env.filters['strftime'] = strftime_filter
app.jinja_env.filters['currency'] = currency_filter


@app.route('/')
def index():
    salvados = db.get_all_salvados()
    return render_template('index.html', salvados=salvados)


@app.route('/salvado', methods=['GET', 'POST'])
def salvado():
    status_opcoes = db.get_status_opcoes()
    analistas_opcoes = db.get_analistas_opcoes()
    leiloeiros_opcoes = db.get_leiloeiros_opcoes()
    errors = {}
    form_data = {}
    if request.method == 'POST':
        form_data = {key: request.form.get(key, '')
                     for key in db.get_columns()}
        required_fields = ['status', 'sinistro', 'apolice', 'data_recebimento_salvado', 'data_pedido_cotacao_remocao',
                           'nome_segurado', 'nome_terceiro', 'placa', 'marca', 'modelo', 'ano']
        for field in required_fields:
            if not form_data[field] or form_data[field].strip() == '':
                errors[field] = True
        if not errors:
            for key in ['valor_fipe', 'valor_total_indenizacao', 'franquia_outros_descontos', 'valor_pago_pela_cia',
                        'valor_nf_entrada', 'valor_nf_saida', 'valor_venda']:
                value = form_data[key].strip()
                if value and value.lower() != 'none':
                    try:
                        form_data[key] = float(value.replace(',', '.'))
                    except ValueError:
                        form_data[key] = None
                else:
                    form_data[key] = None
            salvado = Salvado(**form_data)
            db.add_salvado(salvado)
            return redirect(url_for('index'))
        error_messages = [FIELD_NAMES[field] for field in errors.keys()]
        return render_template('salvado_form.html', status_opcoes=status_opcoes, analistas_opcoes=analistas_opcoes,
                               leiloeiros_opcoes=leiloeiros_opcoes, salvado=None, form_data=form_data, errors=errors,
                               error_messages=error_messages)
    return render_template('salvado_form.html', status_opcoes=status_opcoes, analistas_opcoes=analistas_opcoes,
                           leiloeiros_opcoes=leiloeiros_opcoes, salvado=None, form_data=form_data, errors=errors,
                           error_messages=[])


@app.route('/atualizar/<int:id>', methods=['GET', 'POST'])
def atualizar(id):
    status_opcoes = db.get_status_opcoes()
    analistas_opcoes = db.get_analistas_opcoes()
    leiloeiros_opcoes = db.get_leiloeiros_opcoes()
    salvado = db.get_salvado_by_id(id)
    errors = {}
    if request.method == 'POST':
        salvado_data = {key: request.form.get(
            key, '') for key in db.get_columns()}
        required_fields = ['status', 'sinistro', 'apolice', 'data_recebimento_salvado', 'data_pedido_cotacao_remocao',
                           'nome_segurado', 'nome_terceiro', 'placa', 'marca', 'modelo', 'ano']
        for field in required_fields:
            if not salvado_data[field] or salvado_data[field].strip() == '':
                errors[field] = True
        if not errors:
            for key in ['valor_fipe', 'valor_total_indenizacao', 'franquia_outros_descontos', 'valor_pago_pela_cia',
                        'valor_nf_entrada', 'valor_nf_saida', 'valor_venda']:
                value = salvado_data[key].strip()
                if value and value.lower() != 'none':
                    try:
                        salvado_data[key] = float(value.replace(',', '.'))
                    except ValueError:
                        salvado_data[key] = None
                else:
                    salvado_data[key] = None
            salvado = Salvado(id=id, **salvado_data)
            db.update_salvado(salvado)
            return redirect(url_for('index'))
        error_messages = [FIELD_NAMES[field] for field in errors.keys()]
        return render_template('salvado_form.html', status_opcoes=status_opcoes, analistas_opcoes=analistas_opcoes,
                               leiloeiros_opcoes=leiloeiros_opcoes, salvado=salvado, form_data=salvado_data,
                               errors=errors, error_messages=error_messages)
    return render_template('salvado_form.html', status_opcoes=status_opcoes, analistas_opcoes=analistas_opcoes,
                           leiloeiros_opcoes=leiloeiros_opcoes, salvado=salvado, form_data={}, errors=errors,
                           error_messages=[])


@app.route('/detalhes/<int:id>')
def detalhes(id):
    salvado = db.get_salvado_by_id(id)
    if salvado:
        return render_template('salvado_detalhes.html', salvado=salvado)
    return redirect(url_for('index'))


@app.route('/gerenciar', methods=['GET', 'POST'])
def gerenciar():
    secao = request.args.get('secao', 'status')
    if request.method == 'POST':
        acao = request.form['acao']
        if secao == 'status':
            if acao == 'inserir':
                db.add_status(request.form['novo_status'])
            elif acao == 'excluir':
                db.delete_status(request.form['status_id'])
            elif acao == 'alterar':
                db.update_status(
                    request.form['status_id'], request.form['novo_nome'])
        elif secao == 'analistas':
            if acao == 'inserir':
                db.add_analista(
                    request.form['nome'], request.form['email'], request.form['cargo'])
            elif acao == 'excluir':
                db.delete_analista(request.form['analista_id'])
            elif acao == 'alterar':
                db.update_analista(request.form['analista_id'], request.form['nome'], request.form['email'],
                                   request.form['cargo'])
        elif secao == 'leiloeiros':
            if acao == 'inserir':
                db.add_leiloeiro(request.form['nome'], request.form['endereco'], request.form['telefone'],
                                 request.form['responsavel'], request.form['email'])
            elif acao == 'excluir':
                db.delete_leiloeiro(request.form['leiloeiro_id'])
            elif acao == 'alterar':
                db.update_leiloeiro(request.form['leiloeiro_id'], request.form['nome'], request.form['endereco'],
                                    request.form['telefone'], request.form['responsavel'], request.form['email'])
    status_opcoes = db.get_all_status_opcoes()
    analistas = db.get_all_analistas()
    leiloeiros = db.get_all_leiloeiros()
    return render_template('gerenciar.html', status_opcoes=status_opcoes, analistas=analistas,
                           leiloeiros=leiloeiros, secao=secao)


if __name__ == '__main__':
    app.run(debug=True)
