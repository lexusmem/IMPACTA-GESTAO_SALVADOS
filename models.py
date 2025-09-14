import sqlite3


class Salvado:
    def __init__(self, id=None, status=None, sinistro=None, apolice=None, data_recebimento_salvado=None,
                 data_pedido_cotacao_remocao=None, nome_segurado=None, nome_terceiro=None, placa=None,
                 marca=None, modelo=None, ano=None, n_fipe=None, valor_fipe=None, mes_ano_ref_fipe=None,
                 leiloeiro=None, status_remocao_leiloeiro=None, local_atual_veiculo=None,
                 data_entrada_patio_leiloeiro=None, vistorias_solicitada_monta=None, vistorias_recebidas_monta=None,
                 vistorias_solicitada_ecv=None, vistorias_recebidas_ecv=None, classificacao_danos=None, ecv=None,
                 valor_total_indenizacao=None, franquia_outros_descontos=None, valor_pago_pela_cia=None,
                 data_pagto_indenizacao=None, data_recebimento_docs_nf_entrada=None, data_solicitacao_nf_entrada=None,
                 data_recebimento_nf_entrada=None, n_nf_entrada=None, valor_nf_entrada=None,
                 data_solicitacao_nf_saida=None, data_recebimento_nf_saida=None, n_nf_saida=None, valor_nf_saida=None,
                 data_solicitacao_recorte_chassi=None, data_recebimento_recorte_chassi=None,
                 data_docs_disponivel_transf_seguradora=None, data_recebimento_docs_transf_seguradora=None,
                 data_venda_salvado=None, valor_venda=None, nome_arrematante=None,
                 data_docs_disponivel_transf_arrematante=None, data_recebimento_docs_transf_arrematante=None,
                 doc_transferido_arrematante=None, analista_responsavel=None, historico=None):
        self.id = id
        self.status = status
        self.sinistro = sinistro
        self.apolice = apolice
        self.data_recebimento_salvado = data_recebimento_salvado
        self.data_pedido_cotacao_remocao = data_pedido_cotacao_remocao
        self.nome_segurado = nome_segurado
        self.nome_terceiro = nome_terceiro
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.n_fipe = n_fipe
        self.valor_fipe = valor_fipe
        self.mes_ano_ref_fipe = mes_ano_ref_fipe
        self.leiloeiro = leiloeiro
        self.status_remocao_leiloeiro = status_remocao_leiloeiro
        self.local_atual_veiculo = local_atual_veiculo
        self.data_entrada_patio_leiloeiro = data_entrada_patio_leiloeiro
        self.vistorias_solicitada_monta = vistorias_solicitada_monta
        self.vistorias_recebidas_monta = vistorias_recebidas_monta
        self.vistorias_solicitada_ecv = vistorias_solicitada_ecv
        self.vistorias_recebidas_ecv = vistorias_recebidas_ecv
        self.classificacao_danos = classificacao_danos
        self.ecv = ecv
        self.valor_total_indenizacao = valor_total_indenizacao
        self.franquia_outros_descontos = franquia_outros_descontos
        self.valor_pago_pela_cia = valor_pago_pela_cia
        self.data_pagto_indenizacao = data_pagto_indenizacao
        self.data_recebimento_docs_nf_entrada = data_recebimento_docs_nf_entrada
        self.data_solicitacao_nf_entrada = data_solicitacao_nf_entrada
        self.data_recebimento_nf_entrada = data_recebimento_nf_entrada
        self.n_nf_entrada = n_nf_entrada
        self.valor_nf_entrada = valor_nf_entrada
        self.data_solicitacao_nf_saida = data_solicitacao_nf_saida
        self.data_recebimento_nf_saida = data_recebimento_nf_saida
        self.n_nf_saida = n_nf_saida
        self.valor_nf_saida = valor_nf_saida
        self.data_solicitacao_recorte_chassi = data_solicitacao_recorte_chassi
        self.data_recebimento_recorte_chassi = data_recebimento_recorte_chassi
        self.data_docs_disponivel_transf_seguradora = data_docs_disponivel_transf_seguradora
        self.data_recebimento_docs_transf_seguradora = data_recebimento_docs_transf_seguradora
        self.data_venda_salvado = data_venda_salvado
        self.valor_venda = valor_venda
        self.nome_arrematante = nome_arrematante
        self.data_docs_disponivel_transf_arrematante = data_docs_disponivel_transf_arrematante
        self.data_recebimento_docs_transf_arrematante = data_recebimento_docs_transf_arrematante
        self.doc_transferido_arrematante = doc_transferido_arrematante
        self.analista_responsavel = analista_responsavel
        self.historico = historico


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('salvados.db', check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS salvados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                status TEXT,
                sinistro TEXT,
                apolice TEXT,
                data_recebimento_salvado DATE,
                data_pedido_cotacao_remocao DATE,
                nome_segurado TEXT,
                nome_terceiro TEXT,
                placa TEXT,
                marca TEXT,
                modelo TEXT,
                ano TEXT,
                n_fipe TEXT,
                valor_fipe REAL,
                mes_ano_ref_fipe TEXT,
                leiloeiro TEXT,
                status_remocao_leiloeiro TEXT,
                local_atual_veiculo TEXT,
                data_entrada_patio_leiloeiro DATE,
                vistorias_solicitada_monta DATE,
                vistorias_recebidas_monta DATE,
                vistorias_solicitada_ecv DATE,
                vistorias_recebidas_ecv DATE,
                classificacao_danos TEXT,
                ecv TEXT,
                valor_total_indenizacao REAL,
                franquia_outros_descontos REAL,
                valor_pago_pela_cia REAL,
                data_pagto_indenizacao DATE,
                data_recebimento_docs_nf_entrada DATE,
                data_solicitacao_nf_entrada DATE,
                data_recebimento_nf_entrada DATE,
                n_nf_entrada TEXT,
                valor_nf_entrada REAL,
                data_solicitacao_nf_saida DATE,
                data_recebimento_nf_saida DATE,
                n_nf_saida TEXT,
                valor_nf_saida REAL,
                data_solicitacao_recorte_chassi DATE,
                data_recebimento_recorte_chassi DATE,
                data_docs_disponivel_transf_seguradora DATE,
                data_recebimento_docs_transf_seguradora DATE,
                data_venda_salvado DATE,
                valor_venda REAL,
                nome_arrematante TEXT,
                data_docs_disponivel_transf_arrematante DATE,
                data_recebimento_docs_transf_arrematante DATE,
                doc_transferido_arrematante TEXT,
                analista_responsavel TEXT,
                historico TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS status_opcoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analistas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                cargo TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leiloeiros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                endereco TEXT,
                telefone TEXT,
                responsavel TEXT,
                email TEXT
            )
        ''')
        self.conn.commit()

    def add_salvado(self, salvado):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO salvados (
                status, sinistro, apolice, data_recebimento_salvado, data_pedido_cotacao_remocao,
                nome_segurado, nome_terceiro, placa, marca, modelo, ano, n_fipe, valor_fipe,
                mes_ano_ref_fipe, leiloeiro, status_remocao_leiloeiro, local_atual_veiculo,
                data_entrada_patio_leiloeiro, vistorias_solicitada_monta, vistorias_recebidas_monta,
                vistorias_solicitada_ecv, vistorias_recebidas_ecv, classificacao_danos, ecv,
                valor_total_indenizacao, franquia_outros_descontos, valor_pago_pela_cia,
                data_pagto_indenizacao, data_recebimento_docs_nf_entrada, data_solicitacao_nf_entrada,
                data_recebimento_nf_entrada, n_nf_entrada, valor_nf_entrada, data_solicitacao_nf_saida,
                data_recebimento_nf_saida, n_nf_saida, valor_nf_saida, data_solicitacao_recorte_chassi,
                data_recebimento_recorte_chassi, data_docs_disponivel_transf_seguradora,
                data_recebimento_docs_transf_seguradora, data_venda_salvado, valor_venda,
                nome_arrematante, data_docs_disponivel_transf_arrematante,
                data_recebimento_docs_transf_arrematante, doc_transferido_arrematante,
                analista_responsavel, historico
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            salvado.status, salvado.sinistro, salvado.apolice, salvado.data_recebimento_salvado,
            salvado.data_pedido_cotacao_remocao, salvado.nome_segurado, salvado.nome_terceiro,
            salvado.placa, salvado.marca, salvado.modelo, salvado.ano, salvado.n_fipe,
            salvado.valor_fipe, salvado.mes_ano_ref_fipe, salvado.leiloeiro,
            salvado.status_remocao_leiloeiro, salvado.local_atual_veiculo,
            salvado.data_entrada_patio_leiloeiro, salvado.vistorias_solicitada_monta,
            salvado.vistorias_recebidas_monta, salvado.vistorias_solicitada_ecv,
            salvado.vistorias_recebidas_ecv, salvado.classificacao_danos, salvado.ecv,
            salvado.valor_total_indenizacao, salvado.franquia_outros_descontos,
            salvado.valor_pago_pela_cia, salvado.data_pagto_indenizacao,
            salvado.data_recebimento_docs_nf_entrada, salvado.data_solicitacao_nf_entrada,
            salvado.data_recebimento_nf_entrada, salvado.n_nf_entrada, salvado.valor_nf_entrada,
            salvado.data_solicitacao_nf_saida, salvado.data_recebimento_nf_saida,
            salvado.n_nf_saida, salvado.valor_nf_saida, salvado.data_solicitacao_recorte_chassi,
            salvado.data_recebimento_recorte_chassi, salvado.data_docs_disponivel_transf_seguradora,
            salvado.data_recebimento_docs_transf_seguradora, salvado.data_venda_salvado,
            salvado.valor_venda, salvado.nome_arrematante,
            salvado.data_docs_disponivel_transf_arrematante,
            salvado.data_recebimento_docs_transf_arrematante, salvado.doc_transferido_arrematante,
            salvado.analista_responsavel, salvado.historico
        ))
        self.conn.commit()

    def update_salvado(self, salvado):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE salvados SET
                status=?, sinistro=?, apolice=?, data_recebimento_salvado=?, data_pedido_cotacao_remocao=?,
                nome_segurado=?, nome_terceiro=?, placa=?, marca=?, modelo=?, ano=?, n_fipe=?, valor_fipe=?,
                mes_ano_ref_fipe=?, leiloeiro=?, status_remocao_leiloeiro=?, local_atual_veiculo=?,
                data_entrada_patio_leiloeiro=?, vistorias_solicitada_monta=?, vistorias_recebidas_monta=?,
                vistorias_solicitada_ecv=?, vistorias_recebidas_ecv=?, classificacao_danos=?, ecv=?,
                valor_total_indenizacao=?, franquia_outros_descontos=?, valor_pago_pela_cia=?,
                data_pagto_indenizacao=?, data_recebimento_docs_nf_entrada=?, data_solicitacao_nf_entrada=?,
                data_recebimento_nf_entrada=?, n_nf_entrada=?, valor_nf_entrada=?, data_solicitacao_nf_saida=?,
                data_recebimento_nf_saida=?, n_nf_saida=?, valor_nf_saida=?, data_solicitacao_recorte_chassi=?,
                data_recebimento_recorte_chassi=?, data_docs_disponivel_transf_seguradora=?,
                data_recebimento_docs_transf_seguradora=?, data_venda_salvado=?, valor_venda=?,
                nome_arrematante=?, data_docs_disponivel_transf_arrematante=?,
                data_recebimento_docs_transf_arrematante=?, doc_transferido_arrematante=?,
                analista_responsavel=?, historico=?
            WHERE id=?
        ''', (
            salvado.status, salvado.sinistro, salvado.apolice, salvado.data_recebimento_salvado,
            salvado.data_pedido_cotacao_remocao, salvado.nome_segurado, salvado.nome_terceiro,
            salvado.placa, salvado.marca, salvado.modelo, salvado.ano, salvado.n_fipe,
            salvado.valor_fipe, salvado.mes_ano_ref_fipe, salvado.leiloeiro,
            salvado.status_remocao_leiloeiro, salvado.local_atual_veiculo,
            salvado.data_entrada_patio_leiloeiro, salvado.vistorias_solicitada_monta,
            salvado.vistorias_recebidas_monta, salvado.vistorias_solicitada_ecv,
            salvado.vistorias_recebidas_ecv, salvado.classificacao_danos, salvado.ecv,
            salvado.valor_total_indenizacao, salvado.franquia_outros_descontos,
            salvado.valor_pago_pela_cia, salvado.data_pagto_indenizacao,
            salvado.data_recebimento_docs_nf_entrada, salvado.data_solicitacao_nf_entrada,
            salvado.data_recebimento_nf_entrada, salvado.n_nf_entrada, salvado.valor_nf_entrada,
            salvado.data_solicitacao_nf_saida, salvado.data_recebimento_nf_saida,
            salvado.n_nf_saida, salvado.valor_nf_saida, salvado.data_solicitacao_recorte_chassi,
            salvado.data_recebimento_recorte_chassi, salvado.data_docs_disponivel_transf_seguradora,
            salvado.data_recebimento_docs_transf_seguradora, salvado.data_venda_salvado,
            salvado.valor_venda, salvado.nome_arrematante,
            salvado.data_docs_disponivel_transf_arrematante,
            salvado.data_recebimento_docs_transf_arrematante, salvado.doc_transferido_arrematante,
            salvado.analista_responsavel, salvado.historico, salvado.id
        ))
        self.conn.commit()

    def get_salvado_by_id(self, id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM salvados WHERE id=?', (id,))
        row = cursor.fetchone()
        if row:
            return Salvado(*row)
        return None

    def get_all_salvados(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM salvados')
        return [Salvado(*row) for row in cursor.fetchall()]

    def get_columns(self):
        cursor = self.conn.cursor()
        cursor.execute('PRAGMA table_info(salvados)')
        return [col[1] for col in cursor.fetchall() if col[1] != 'id']

    def add_status(self, nome):
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT OR IGNORE INTO status_opcoes (nome) VALUES (?)', (nome,))
        self.conn.commit()

    def delete_status(self, status_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM status_opcoes WHERE id=?', (status_id,))
        self.conn.commit()

    def update_status(self, status_id, novo_nome):
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE status_opcoes SET nome=? WHERE id=?', (novo_nome, status_id))
        self.conn.commit()

    def get_status_opcoes(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT nome FROM status_opcoes')
        return [row[0] for row in cursor.fetchall()]

    def get_all_status_opcoes(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM status_opcoes')
        return cursor.fetchall()

    def add_analista(self, nome, email, cargo):
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO analistas (nome, email, cargo) VALUES (?, ?, ?)', (nome, email, cargo))
        self.conn.commit()

    def update_analista(self, analista_id, nome, email, cargo):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE analistas SET nome=?, email=?, cargo=? WHERE id=?',
                       (nome, email, cargo, analista_id))
        self.conn.commit()

    def delete_analista(self, analista_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM analistas WHERE id=?', (analista_id,))
        self.conn.commit()

    def get_all_analistas(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, nome, email, cargo FROM analistas')
        return cursor.fetchall()

    def get_analistas_opcoes(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT nome FROM analistas')
        return [row[0] for row in cursor.fetchall()]

    def add_leiloeiro(self, nome, endereco, telefone, responsavel, email):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO leiloeiros (nome, endereco, telefone, responsavel, email) VALUES (?, ?, ?, ?, ?)',
                       (nome, endereco, telefone, responsavel, email))
        self.conn.commit()

    def update_leiloeiro(self, leiloeiro_id, nome, endereco, telefone, responsavel, email):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE leiloeiros SET nome=?, endereco=?, telefone=?, responsavel=?, email=? WHERE id=?',
                       (nome, endereco, telefone, responsavel, email, leiloeiro_id))
        self.conn.commit()

    def delete_leiloeiro(self, leiloeiro_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM leiloeiros WHERE id=?', (leiloeiro_id,))
        self.conn.commit()

    def get_all_leiloeiros(self):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT id, nome, endereco, telefone, responsavel, email FROM leiloeiros')
        return cursor.fetchall()

    def get_leiloeiros_opcoes(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT nome FROM leiloeiros')
        return [row[0] for row in cursor.fetchall()]
