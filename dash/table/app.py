# -*- coding: utf-8 -*-
import os
from datetime import datetime
from typing import cast

import dash
import dash_table
from dash_table.Format import Format, Group, Padding, Symbol
import dash_html_components as html
from dash.dependencies import Input, Output
from numpy import isin, str_
import pandas as pd
import jpholiday

# -----------------------CONSTANTS-----------------------------------------

WEEKDAYS = ["月", "火", "水", "木", "金", "土", "日"]
HOLIDAY = "祝"
ACTIVE_CELL = {"row": 0, "column": 2, "column_id": "開始時刻"}
CURRENT_YEAR_MONTH = datetime.today().strftime("%Y_%m")
ATTENDANCE_BOOK = (
    f"{os.path.dirname(__file__)}/.data/{CURRENT_YEAR_MONTH}_attendance_book.json"
)
BACKUP_FILE = f"{os.path.dirname(__file__)}/.backup/{os.path.basename(ATTENDANCE_BOOK)}"
STANDARD_WORKING_TIME = 8

# ----------------------------------------------------------------


if os.path.exists(ATTENDANCE_BOOK):
    df = pd.read_json(ATTENDANCE_BOOK)
    # preprocess
    df["日付"] = pd.to_datetime(df["日付"], format="%Y/%m/%d").dt.strftime("%Y/%m/%d")

    df.to_json(BACKUP_FILE)
else:
    y = datetime.today().year
    m = datetime.today().month

    def is_holiday(d):
        holidays = [d[0] for d in jpholiday.month_holidays(y, m)]
        return d in holidays

    year_month = f"{y}-{m}-1"
    year_next_month = f"{y}-{m+1}-1"
    dates = pd.to_datetime(pd.date_range(year_month, year_next_month)[:-1]).map(
        lambda d: d.to_pydatetime()
    )
    data = []
    for d in dates:
        is_holiday(d)
        data.append(
            dict(
                日付=d.strftime("%Y/%m/%d"),
                曜日=HOLIDAY if is_holiday(d) else WEEKDAYS[d.weekday()],
                開始時刻="",
                終了時刻="",
                休憩=1,
                勤務時間="",
                残業時間="",
                進捗="",
            )
        )
    df = pd.DataFrame(data)

data = list(df.to_dict("index").values())

app = dash.Dash(__name__)

columns = []

for col in df.columns:
    if col in ["日付", "曜日"]:
        columns.append(
            {
                "name": col,
                "id": col,
                "type": "text",
                "editable": False,
            }
        )
    elif col in ["開始時刻", "終了時刻"]:
        columns.append(
            {
                "name": col,
                "id": col,
                "type": "text",
                # "format": Format(
                #    group_delimiter=":",
                #    padding=Padding.yes,
                #    padding_width=4 + 1,
                #    group=Group.yes,
                #    groups=[2],
                # ),
            }
        )
    elif col in ["勤務時間"]:
        columns.append(
            {
                "name": "勤務時間(＝終了-開始-休憩)",
                "id": col,
                "type": "numeric",
                "editable": False,
                "format": Format(symbol=Symbol.yes, symbol_suffix=" [h]"),
            }
        )
    elif col in ["残業時間"]:
        columns.append(
            {
                "name": f"残業時間(＝max(勤務時間-{STANDARD_WORKING_TIME}, 0))",
                "id": col,
                "type": "numeric",
                "editable": False,
                "format": Format(symbol=Symbol.yes, symbol_suffix=" [h]"),
            }
        )
    elif col in ["休憩"]:
        columns.append(
            {
                "name": col,
                "id": col,
                "type": "numeric",
                "format": Format(symbol=Symbol.yes, symbol_suffix=" [h]"),
            }
        )
    elif col in ["進捗"]:
        columns.append(
            {
                "name": col,
                "id": col,
                "type": "text",
            }
        )
    else:
        raise ValueError(f"Undefined column name {col} found")

app.layout = html.Div(
    children=[
        html.H1("Attendance Book"),
        html.Button("Save", id="save-button"),
        html.Div("", id="save-status"),
        html.H2("Summary"),
        dash_table.DataTable(
            id="summary-table",
            editable=False,
            columns=[
                dict(
                    name="合計勤務時間",
                    id="合計勤務時間",
                    type="numeric",
                    editable=False,
                    format=Format(symbol=Symbol.yes, symbol_suffix=" [h]"),
                ),
                dict(
                    name="合計残業時間",
                    id="合計残業時間",
                    type="numeric",
                    editable=False,
                    format=Format(symbol=Symbol.yes, symbol_suffix=" [h]"),
                ),
            ],
            style_data_conditional=[
                {
                    "if": {
                        "column_id": ["合計残業時間"],
                        "filter_query": "{合計残業時間} > 0",
                    },
                    "color": "purple",
                },
            ],
            style_header=dict(
                fontWeight="bold",
                textAlign="center",
                backgroundColor="rgb(230, 230, 230)",
            ),
            data=[dict(合計勤務時間="", 合計残業時間="")],
        ),
        html.H2("Table"),
        dash_table.DataTable(
            id="time-table",
            editable=True,
            columns=columns,
            data=data,
            active_cell=ACTIVE_CELL,
            style_header=dict(
                backgroundColor="rgb(230, 230, 230)",
                fontWeight="bold",
                textAlign="center",
            ),
            style_data_conditional=[
                {
                    "if": {
                        "column_id": ["日付", "曜日", "開始時刻", "終了時刻"],
                        "filter_query": "{開始時刻} > {終了時刻}",
                    },
                    "backgroundColor": "tomato",
                },
                {
                    "if": {
                        "column_id": ["日付", "曜日"],
                        "filter_query": f"{{曜日}} eq {WEEKDAYS[-2]}",
                    },
                    "color": "blue",
                },
                {
                    "if": {
                        "column_id": ["日付", "曜日"],
                        "filter_query": f"{{曜日}} eq {WEEKDAYS[-1]}",
                    },
                    "color": "red",
                },
                {
                    "if": {
                        "column_id": ["日付", "曜日"],
                        "filter_query": f"{{曜日}} eq {HOLIDAY}",
                    },
                    "color": "red",
                },
                {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"},
            ],
        ),
    ]
)


@app.callback(
    Output("save-status", "children"),
    Input("save-button", "n_clicks"),
    Input("time-table", "data"),
    prevent_initial_call=True,
)
def saveData(n_clicks, data):
    if n_clicks:
        df = pd.DataFrame(data)
        df.to_json(ATTENDANCE_BOOK)
        return f"Saved data at {ATTENDANCE_BOOK}"
    else:
        return ""


active_cell_previous = ACTIVE_CELL


def calculate_working_hours(data):
    for d in data:
        try:
            end = datetime.strptime(d["終了時刻"], "%H:%M")
            begin = datetime.strptime(d["開始時刻"], "%H:%M")
            break_time = d["休憩"]
            working_hours = (end - begin).seconds / 3600
            working_hours -= break_time
            d["勤務時間"] = working_hours
            d["残業時間"] = max(working_hours - STANDARD_WORKING_TIME, 0)
        except ValueError:
            d["勤務時間"] = ""
            d["残業時間"] = ""
    return data


@app.callback(
    Output("time-table", "data"),
    Output("summary-table", "data"),
    Input("time-table", "active_cell"),
    Input("time-table", "data_previous"),
    Input("time-table", "data"),
)
def updateData(active_cell, data_previous, data):
    global active_cell_previous
    if active_cell_previous["column_id"] in ["開始時刻", "終了時刻"]:
        row = active_cell_previous["row"]
        column_id = active_cell_previous["column_id"]
        value = data[row][column_id]
        if value.isdigit():
            value = int(value)
            if value in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
                value *= 100
            # zero padding
            # 145 -> 0145
            # 2345 -> 2345
            # 9999 -> 9999
            # 100000 -> 100000
            str_value = str(value).zfill(4)
            # format with HH:MM
            # 0145 -> 01:45
            # 2345 -> 23:45
            # 9999 -> 99:99
            str_value = ":".join([str_value[0:2], str_value[2:4]])
        else:
            str_value = value
        try:  # to parse timep
            str_value = datetime.strptime(str_value, "%H:%M").strftime("%H:%M")
            data[row][column_id] = str_value
        except Exception:
            # revert data with `previous_data`
            if str_value:
                data[row][column_id] = data_previous[row][column_id]
    data = calculate_working_hours(data)

    total_overwork_working_time = total_working_time = 0
    for d in data:
        wt = d["勤務時間"]
        over_wt = d["残業時間"]
        if not isinstance(wt, str):
            total_working_time += wt
        if not isinstance(over_wt, str):
            total_overwork_working_time += over_wt
    summary = [dict(合計勤務時間=total_working_time, 合計残業時間=total_overwork_working_time)]
    active_cell_previous = active_cell
    return data, summary


if __name__ == "__main__":
    app.run_server(debug=True)
