from infra.configs.connection import DBConecctionHandleApp
from infra.entities.status_opcao import StatusOpcao
from sqlalchemy import text


class StatusOpcaoRepository:
    def add_status(self, nome):
        with DBConecctionHandleApp() as db:
            existente = db.session.query(StatusOpcao).filter(
                StatusOpcao.nome == nome).first()
            if existente:
                return False
            status = StatusOpcao(nome=nome)
            db.session.add(status)
            db.session.commit()
            return True

    def get_all_status_opcoes(self):
        with DBConecctionHandleApp() as db:
            return db.session.query(StatusOpcao).all()

    def get_status_opcoes(self):
        with DBConecctionHandleApp() as db:
            nomes = db.session.query(StatusOpcao.nome).all()
            return [nome[0] for nome in nomes]

    def update_status(self, status_id, novo_nome):
        with DBConecctionHandleApp() as db:
            existente = db.session.query(StatusOpcao).filter(
                StatusOpcao.nome == novo_nome,
                StatusOpcao.id != status_id
            ).first()
            if existente:
                return False
            db.session.query(StatusOpcao).filter(
                StatusOpcao.id == status_id).update({"nome": novo_nome})
            db.session.commit()
            return True

    def delete_status(self, status_id):
        with DBConecctionHandleApp() as db:
            db.session.query(StatusOpcao).filter(
                StatusOpcao.id == status_id).delete()
            db.session.commit()
