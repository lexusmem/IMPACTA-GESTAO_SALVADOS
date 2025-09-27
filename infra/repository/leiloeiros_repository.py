from infra.configs.connection import DBConecctionHandleApp
from infra.entities.leiloeiro import Leiloeiro
from sqlalchemy import text


class LeiloeiroRepository:
    def add_leiloeiro(self, nome, endereco, telefone, responsavel, email):
        with DBConecctionHandleApp() as db:
            leiloeiro = Leiloeiro(nome=nome, endereco=endereco,
                                  telefone=telefone, responsavel=responsavel, email=email)
            db.session.add(leiloeiro)
            db.session.commit()

    def get_all_leiloeiros(self):
        with DBConecctionHandleApp() as db:
            return db.session.query(Leiloeiro).all()

    def update_leiloeiro(self, leiloeiro_id, nome, endereco, telefone, responsavel, email):
        with DBConecctionHandleApp() as db:
            db.session.query(Leiloeiro).filter(Leiloeiro.id == leiloeiro_id).update({
                "nome": nome, "endereco": endereco, "telefone": telefone, "responsavel": responsavel, "email": email
            })
            db.session.commit()

    def delete_leiloeiro(self, leiloeiro_id):
        with DBConecctionHandleApp() as db:
            db.session.query(Leiloeiro).filter(
                Leiloeiro.id == leiloeiro_id).delete()
            db.session.commit()

    def get_leiloeiros_opcoes(self):
        with DBConecctionHandleApp() as db:
            nomes = db.session.query(Leiloeiro.nome).all()
            return [nome[0] for nome in nomes]
