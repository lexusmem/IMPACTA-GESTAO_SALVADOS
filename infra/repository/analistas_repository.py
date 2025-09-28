from infra.configs.connection import DBConecctionHandleApp
from infra.entities.analista import Analista
from sqlalchemy import text


class AnalistaRepository:
    def add_analista(self, nome, email, cargo):
        with DBConecctionHandleApp() as db:
            existente = db.session.query(Analista).filter(
                Analista.nome == nome).first()
            if existente:
                return False
            analista = Analista(nome=nome, email=email, cargo=cargo)
            db.session.add(analista)
            db.session.commit()
            return True

    def get_all_analistas(self):
        with DBConecctionHandleApp() as db:
            return db.session.query(Analista).all()

    def update_analista(self, analista_id, nome, email, cargo):
        with DBConecctionHandleApp() as db:
            db.session.query(Analista).filter(Analista.id == analista_id).update(
                {"nome": nome, "email": email, "cargo": cargo})
            db.session.commit()

    def delete_analista(self, analista_id):
        with DBConecctionHandleApp() as db:
            db.session.query(Analista).filter(
                Analista.id == analista_id).delete()
            db.session.commit()

    def get_analistas_opcoes(self):
        with DBConecctionHandleApp() as db:
            nomes = db.session.query(Analista.nome).all()
            return [nome[0] for nome in nomes]
