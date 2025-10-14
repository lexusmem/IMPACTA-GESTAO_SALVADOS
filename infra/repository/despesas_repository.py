from infra.configs.connection import DBConecctionHandleApp
from infra.entities.despesa import Despesa
from sqlalchemy import text
from sqlalchemy.orm import joinedload
from sqlalchemy import and_


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
            return db.session.query(Despesa).options(joinedload(Despesa.salvado)).all()

    def get_despesas_filtradas(self, **filtros):
        with DBConecctionHandleApp() as db:
            query = db.session.query(Despesa).options(
                joinedload(Despesa.salvado))
            filters = []
            if 'fornecedor' in filtros and filtros['fornecedor']:
                filters.append(Despesa.fornecedor.ilike(
                    f'%{filtros["fornecedor"]}%'))
            if 'ocorrencia' in filtros and filtros['ocorrencia']:
                filters.append(Despesa.ocorrencia.ilike(
                    f'%{filtros["ocorrencia"]}%'))
            if 'placa' in filtros and filtros['placa']:
                filters.append(Despesa.salvado.has(placa=filtros['placa']))
            if 'sinistro' in filtros and filtros['sinistro']:
                filters.append(Despesa.salvado.has(
                    sinistro=filtros['sinistro']))
            if filters:
                query = query.filter(and_(*filters))
            return query.all()

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
