from infra.configs.connection import DBConecctionHandleApp
from infra.entities.salvado import Salvado
from sqlalchemy import text


class SalvadoRepository:
    def add_salvado(self, **kwargs):
        with DBConecctionHandleApp() as db:
            existente = db.session.query(Salvado).filter(
                Salvado.placa == kwargs.get('placa')).first()
            if existente:
                return False
            salvado = Salvado(**kwargs)
            db.session.add(salvado)
            db.session.commit()
            return True

    def get_columns(self):
        return [column.name for column in Salvado.__table__.columns if column.name != 'id']

    def get_all_salvados(self):
        with DBConecctionHandleApp() as db:
            return db.session.query(Salvado).all()

    def get_salvado_by_id(self, salvado_id):
        with DBConecctionHandleApp() as db:
            return db.session.query(Salvado).filter(Salvado.id == salvado_id).first()

    def update_salvado(self, salvado_id, **kwargs):
        with DBConecctionHandleApp() as db:
            db.session.query(Salvado).filter(
                Salvado.id == salvado_id).update(kwargs)
            db.session.commit()

    def deletar_salvado(self, salvado_id):
        with DBConecctionHandleApp() as db:
            db.session.query(Salvado).filter(Salvado.id == salvado_id).delete()
            db.session.commit()

    def deletar_todos_salvados(self):
        with DBConecctionHandleApp() as db:
            db.session.query(Salvado).delete()
            db.session.execute(text("DBCC CHECKIDENT ('salvados', RESEED, 0)"))
            db.session.commit()
