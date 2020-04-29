from datetime import datetime, date, timedelta
import pandas as pd


class Dates:
    @staticmethod
    def last_monday(dt=''):
        dt = datetime.fromisoformat(str(dt)).date() if dt else date.today()

        while dt.weekday() != 0:
            dt -= timedelta(1)

        return dt

    @staticmethod
    def last_45day():
        return Dates.back_days(days=45)

    @staticmethod
    def back_days(dt='', days=1):
        dt = datetime.fromisoformat(str(dt)).date() if dt else date.today()
        return dt - timedelta(days)

    @staticmethod
    def first_month_day(dt):
        dt = datetime.fromisoformat(str(dt)).date()
        dt = dt.replace(day=1)
        return dt

    @staticmethod
    def last_month_day(dt):
        dt = datetime.fromisoformat(dt)
        month, year = dt.month + 1, dt.year

        if month > 12:
            month, year = 1, year + 1

        dt = dt.replace(day=1, month=month, year=year) - timedelta(1)
        return dt.date()

    @staticmethod
    def last7days(dt=None):
        if date:
            dt = datetime.fromisoformat(dt).date()
        else:
            dt = datetime.now().date()
        return [dt + timedelta(i) for i in range(-6, 1)]

    @staticmethod
    def append_table(insert_df, table_df):

        added = False

        # Checks if all columns from base table are within the insert dataframe
        all_within = all([col in insert_df.columns.tolist() for col in table_df.columns.tolist()])

        if all_within:
            df = pd.concat([insert_df[table_df.columns], table_df])
        else:
            df = pd.concat([insert_df.reindex(columns=table_df.columns), table_df])

        df = df.drop_duplicates().reset_index(drop=True)

        if len(df) > len(table_df):
            added = True

        return df, added

