import json
from dataclasses import dataclass

import redshift_connector

from django_pdf.logger import LOGGER
from django.core.cache import cache

TTL = 3600 * 24 * 7


@dataclass
class RedshiftConnection:
    host: str
    username: str
    password: str
    database: str = 'dev'

    def __enter__(self):
        self._conn = self._connect()
        self._cursor = self._conn.cursor()

    def _connect(self):
        LOGGER.info(f'Connecting to redshift {self.host}, database {self.database}...')
        conn = redshift_connector.connect(
            host=self.host,
            database=self.database,
            user=self.username,
            password=self.password
        )
        return conn

    def execute(self, script: str):
        return self._cursor.execute(script)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.commit()
        self._cursor.close()
        self._conn.close()


def create_tables(conn: RedshiftConnection):
    with conn:
        conn.execute("""
        create table if not exists transactions(username varchar,
        country varchar,
        category varchar,
        transaction_date varchar,
        description varchar(MAX),
        amount int) 
        """)


def load_data(conn: RedshiftConnection, source: str, iam_role: str):
    LOGGER.info(f'Loading data from {source}')
    with conn:
        conn.execute(f"""
        copy transactions(username, country, transaction_date, description, amount, category) 
        from '{source}' 
        iam_role '{iam_role}' 
        csv;
        """)


@dataclass
class Reports:
    conn: RedshiftConnection

    def user_count(self):
        result = self.conn.execute("""
        select count(*) from 
        (select distinct username from transactions)
        """).fetchall()
        return result[0][0] if result is not None else None

    def transactions_count(self):
        result = self.conn.execute("""
        select count(username) from transactions
        """).fetchall()
        return result[0][0] if result is not None else None

    def avg_expenses_per_category(self):
        LOGGER.info('Average expenses per category...')
        result = self.conn.execute("""
        select country, category, abs(median(amount)::int) 
        from (
                select username, country, category, year, month, sum(amount) as amount
                from (
                    select username, country, category, DATE_PART(year, tdate) as year, DATE_PART(month, tdate) as month, amount 
                    from transactions
                ) 
                group by username, country, category, year, month
        )
        group by country, category   
        having country in (select * from countries limit 5)
        order by country     
        """).fetchall()
        return {'columns': ('country', 'category', 'amount'), 'items': result}

    def expenses_per_month(self):
        LOGGER.info('Expenses per month...')
        result = self.conn.execute("""
        select country, year::int, month::int, abs(median(amount)::int) 
        from (
                select username, country, year, month, sum(amount) as amount
                from (
                    select username, country, DATE_PART(year, tdate) as year, DATE_PART(month, tdate) as month, amount 
                    from transactions
                ) 
                group by username, country, year, month
        )
        group by country, year, month                
        having country in (select * from countries limit 5)
        order by country     
        """).fetchall()
        return {'columns': ('country', 'year', 'month', 'amount'), 'items': result}


def create_reports_redshift(host, username, password, database, load_from, iam_role):
    conn = RedshiftConnection(host=host, username=username, password=password, database=database)
    create_tables(conn)
    conn = RedshiftConnection(host=host, username=username, password=password, database=database)
    load_data(conn, load_from, iam_role)
    reports = Reports(conn=conn)

    with conn:
        _avg_expenses_per_category = reports.avg_expenses_per_category()
        LOGGER.info(_avg_expenses_per_category)
        _expenses_per_month = reports.expenses_per_month()
        LOGGER.info(_expenses_per_month)
    LOGGER.info('Save reports to cache...')
    cache.set(f'redshift#admin#reports#expenses_per_month', json.dumps(_expenses_per_month), timeout=TTL)
    cache.set(f'redshift#admin#reports#avg_expenses_per_category', json.dumps(_avg_expenses_per_category), timeout=TTL)
