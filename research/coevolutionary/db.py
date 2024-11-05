import time
from typing import Dict

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INTEGER, TEXT, REAL

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

EntityMeta = declarative_base()


class Experiment(EntityMeta):
    __tablename__ = f"coevolution_experiment"

    id = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    experiment_name = Column(TEXT, nullable=False)
    algorithm_name = Column(TEXT, nullable=False)
    algorithm_params = Column(TEXT, nullable=False)
    is_coevolution = Column(INTEGER, nullable=False)
    adaptation_interval = Column(INTEGER, nullable=True)
    shared_resource = Column(INTEGER, nullable=True)
    penalty = Column(REAL, nullable=True)
    social_card = Column(REAL, nullable=True)
    input_regex = Column(TEXT, nullable=False)
    output_regex = Column(TEXT, nullable=False)
    input_metric = Column(REAL, nullable=False)
    output_metric = Column(REAL, nullable=False)
    created_at = Column(TEXT, nullable=False)

    def normalize(self):
        return {
            'id': self.id,
            'experiment_name': self.experiment_name.__str__(),
            'algorithm_name': self.algorithm_name.__str__(),
            'algorithm_params': self.algorithm_params.__str__(),
            'is_coevolution': self.is_coevolution,
            'adaptation_interval': self.adaptation_interval,
            'shared_resource': self.shared_resource,
            'penalty': self.penalty,
            'social_card': self.social_card,
            'input_regex': self.input_regex.__str__(),
            'output_regex': self.output_regex.__str__(),
            'input_metric': self.input_metric,
            'output_metric': self.output_metric,
            'created_at': self.created_at,
        }


class DBRepository:
    def __init__(self, database_url, entity_meta):
        self.engine = create_engine(
            database_url,
            echo=False,
            future=True,
            pool_pre_ping=True,
        )

        self.session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        entity_meta.metadata.create_all(bind=self.engine)
        self.entity_meta = entity_meta
        self.db = scoped_session(self.session)

    def get(self, meta: Experiment) -> Dict:
        meta = self.db.get(
            Experiment,
            meta.id,
        )
        return meta.normalize()

    def create(self, meta: Experiment) -> Dict:
        self.db.add(meta)
        self.db.commit()
        self.db.refresh(meta)
        return meta.normalize()

    def update(self, id: int, meta: Experiment) -> Dict:
        meta.id = id
        self.db.merge(meta)
        self.db.commit()
        return meta.normalize()

    def delete(self, meta: Experiment) -> None:
        self.db.delete(meta)
        self.db.commit()
        self.db.flush()
