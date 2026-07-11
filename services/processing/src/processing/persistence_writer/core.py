import pandas as pd
from structlog import get_logger
from .interface import PersistenceWriterProtocol

logger = get_logger(__name__)

class TimescaleDBWriter(PersistenceWriterProtocol):
    def __init__(self, db_url: str):
        self.db_url = db_url
        
    def write_features(self, features_df: pd.DataFrame, table_name: str = "engineered_features") -> None:
        logger.info("writing_features_to_db", table=table_name)
        
        if features_df.empty:
            logger.warning("empty_dataframe_write_skipped")
            return
            
        try:
            from sqlalchemy import create_engine
            engine = create_engine(self.db_url)
            # This assumes the hypertable is created and schema matches
            features_df.to_sql(table_name, engine, if_exists='append', index=False)
            logger.info("write_successful", rows_inserted=len(features_df))
        except Exception as e:
            logger.error("db_write_failed", error=str(e))
            raise
