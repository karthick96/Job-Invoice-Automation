from numpy import column_stack
from calendar_events_extract import calendar_events_extract

import sqlite3
import pandas as pd

import os

import datetime
from dateutil.relativedelta import relativedelta
#import calendar


def generate_calendar_events_tsv(tsv_name, strt_frm_initial_dte=True, filtered_calendars=None):
    currentDate = datetime.date.today()
    # subtracting one month as I need one month old events. For example, if I run this application today, I need previous months results.
    PrevMonthSameDate = currentDate - relativedelta(months=1)
    PrevFirstDayOfMonth = str(PrevMonthSameDate.replace(day=1))[:10].split('-')
    FirstDayOfMonth = str(currentDate.replace(day=1))[:10].split('-')
    """
    lastDayOfMonth = datetime.date(PrevMonthSameDate.year, PrevMonthSameDate.month, calendar.monthrange(
        PrevMonthSameDate.year, PrevMonthSameDate.month)[1])
    lastDayOfMonth = str(lastDayOfMonth).split('-')
    """
    if strt_frm_initial_dte:
        start_date = datetime.datetime(
            2022, 3, 1, 00, 00, 00, 0).isoformat() + 'Z'  # this is the initial starting date of the events
    else:
        start_date = datetime.datetime(int(PrevFirstDayOfMonth[0]),
                                       int(PrevFirstDayOfMonth[1]),
                                       int(PrevFirstDayOfMonth[2]), 00, 00, 00, 0).isoformat() + 'Z'
    end_date = datetime.datetime(int(FirstDayOfMonth[0]),
                                 int(FirstDayOfMonth[1]),
                                 int(FirstDayOfMonth[2]), 00, 00, 00, 0).isoformat() + 'Z'

    df = calendar_events_extract.calendar_events_extract(
        filter_desc='class',
        start_date=start_date,
        end_date=end_date,
        filtered_calendars=filtered_calendars
    )

    if isinstance(df, pd.DataFrame) == False:
        print(
            "Refresh token expired! so, deleting token.json and requesting access to the user again!!!")
        df = calendar_events_extract.calendar_events_extract(
            filter_desc='class',
            start_date=start_date,
            end_date=end_date,
            filtered_calendars=filtered_calendars
        )
    else:
        df.to_csv(tsv_name+'.tsv', sep="\t", index=False)
        return df


def save_history_tsv(df, tsv_name, history_reload=False):
    if history_reload == True:
        print('*'*50+'History reloading'+'*'*50)
        os.remove(tsv_name+'.tsv')
        os.remove('history_'+tsv_name+'.tsv')
        os.remove(tsv_name+'.db')
        df = generate_calendar_events_tsv(
            tsv_name, strt_frm_initial_dte=True)  # False

    # connect to database
    conn = sqlite3.connect(tsv_name+'.db')
    # create a cursor
    cur = conn.cursor()
    insert_flag = False
    while (insert_flag == False):
        # finding if the table exists
        cur.execute(
            "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='"+tsv_name+"';")

        if cur.fetchone()[0] == 1:
            # inserting a record inside the table if table exists
            for i in range(len(df)):
                cur.execute("INSERT INTO "+tsv_name+" VALUES ( '" +
                            str(df.loc[i, 'event_start_dtm'])+"','" +
                            str(df.loc[i, 'event_end_dtm'])+"','" +
                            str(df.loc[i, 'event_description'])+"','" +
                            str(df.loc[i, 'event_hours']) +
                            "');")
            insert_flag = True
        else:
            # creating the table if it doesn't exist
            cur.execute("CREATE TABLE "+tsv_name+"""
            (
            event_start_dtm text,
            event_end_dtm text,
            event_description text,
            event_hours integer
             );""")

    # delete the duplicate records if there are any in the db
    cur.execute("""SELECT event_start_dtm,
                          event_end_dtm,
                          event_description,
                          COUNT(*) AS C
                          FROM """+tsv_name+"""
                          GROUP BY event_start_dtm,
                                   event_end_dtm,
                                   event_description
                          HAVING COUNT(*)>1""")

    if cur.fetchone() is None:
        pass
    elif cur.fetchone()[3] > 1:
        cur.execute("""
        DELETE FROM """+tsv_name+"""
        WHERE rowid IN (
            SELECT rowid FROM (
                SELECT rowid,
                row_number() over( partition by
                                    event_start_dtm,
                                    event_end_dtm,
                                    event_description) as N
            FROM """+tsv_name+""" )
        WHERE N>1
        );""")

    conn.commit()
    conn.close()

    if history_reload == True:
        return df


def fetch_history_tsv(df, tsv_name, save_output=False, print_history=False):
    # connect to database
    conn = sqlite3.connect(tsv_name+'.db')
    # create a cursor
    cur = conn.cursor()

    # fetching records
    cur.execute("select * from "+tsv_name+';')

    columns = [description[0] for description in cur.description]
    history = pd.DataFrame(cur.fetchall(), columns=columns)

    if save_output == True:
        history.to_csv('history_'+tsv_name+'.tsv', sep="\t", index=False)

    if print_history:
        print(history)

    conn.commit()
    conn.close()

    return history


if __name__ == '__main__':
    # User input required
    tsv_name = "Invoice_details"
    history_reload = False  # True
    filtered_calendars = ['My Schedule', 'karthickrajamrita@gmail.com']

    # Executing the program as per the input provided above
    if history_reload == True:
        df = save_history_tsv(df=None, tsv_name=tsv_name,
                              history_reload=True)
        fetch_history_tsv(df=df, tsv_name=tsv_name,
                          save_output=True, print_history=True)
    else:
        df = generate_calendar_events_tsv(
            tsv_name=tsv_name, strt_frm_initial_dte=False, filtered_calendars=filtered_calendars)  # True
        save_history_tsv(df=df, tsv_name=tsv_name, history_reload=False)
        fetch_history_tsv(df=df, tsv_name=tsv_name,
                          save_output=True, print_history=True)
