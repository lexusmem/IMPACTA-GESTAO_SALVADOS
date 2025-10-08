from infra.configs.connection import DBConecctionHandleApp
from infra.entities.despesa import Despesa
from sqlalchemy import text


class DespesaRepository:
    def add_despesa(self, **kwargs):
        with DBConecctionHandleApp() as db:
            despesa = Despesa(**kwargs)
            db.session.add(despesa)
            db.session.commit()
            return True

    def get_columns(self):
        return [column.name for column in Despesa.__table__.columns if column.name != 'id']

    def get_all_despesas(self):
        with DBConecctionHandleApp() as db:
            return db.session.query(Despesa).all()

    def get_despesas_por_salvado(self, salvado_id):
        with DBConecctionHandleApp() as db:
            return db.session.query(Despesa).filter(Despesa.salvado_id == salvado_id).all()

    def get_despesa_by_id(self, despesa_id):
        with DBConecctionHandleApp() as db:
            return db.session.query(Despesa).filter(Despesa.id == despesa_id).first()

    def update_despesa(self, despesa_id, **kwargs):
        with DBConecctionHandleApp() as db:
            db.session.query(Despesa).filter(
                Despesa.id == despesa_id).update(kwargs)
            db.session.commit()
            return True

    def deletar_despesa(self, despesa_id):
        with DBConecctionHandleApp() as db:
            db.session.query(Despesa).filter(Despesa.id == despesa_id).delete()
            db.session.commit()

    def deletar_todas_despesas(self):
        with DBConecctionHandleApp() as db:
            db.session.query(Despesa).delete()
            db.session.execute(text("DBCC CHECKIDENT ('despesas', RESEED, 0)"))
            db.session.commit()
