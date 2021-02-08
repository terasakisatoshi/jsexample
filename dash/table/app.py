# -*- coding: utf-8 -*-
import os
from datetime import date, datetime

import dash
import dash_core_components as dcc
import dash_table
from dash_table.Format import Format, Symbol
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import jpholiday


# -----------------------CONSTANTS-----------------------------------------

WEEKDAYS = ["月", "火", "水", "木", "金", "土", "日"]
DAYS_OFF_INDEX = [5, 6]  # "土, 日"

DATE_FORMAT = "%Y/%m/%d"
UNREGISTERED = "未登録"
DAYS_OFF = "休日"
HOLIDAY = "祝"
EMPTY_VALUE = ""
ACTIVE_CELL = {"row": 0, "column": 2, "column_id": "開始時刻"}
CURRENT_YEAR_MONTH = datetime.today().strftime("%Y_%m")
CURRENT_YEAR = int(datetime.today().strftime("%Y"))
CURRENT_MONTH = int(datetime.today().strftime("%m"))
CURRENT_DAYS = pd.to_datetime(
    pd.date_range(
        datetime(CURRENT_YEAR, CURRENT_MONTH, 1),
        datetime(CURRENT_YEAR, CURRENT_MONTH + 1, 1),
    )[:-1]
).map(lambda d: d.to_pydatetime())

ATTENDANCE_BOOK = os.path.join(
    f"{os.path.dirname(__file__)}",
    ".data",
    f"{CURRENT_YEAR_MONTH}_attendance_book.json",
)

BACKUP_FILE = os.path.join(
    f"{os.path.dirname(__file__)}",
    ".backup",
    f"{CURRENT_YEAR_MONTH}_attendance_book.json",
)

if not os.path.exists(os.path.dirname(ATTENDANCE_BOOK)):
    os.makedirs(os.path.dirname(ATTENDANCE_BOOK))

if not os.path.exists(os.path.dirname(BACKUP_FILE)):
    os.makedirs(os.path.dirname(BACKUP_FILE))

STANDARD_WORKING_TIME = 8
WORKING_STATUS = [
    "勤務",
    "有給",
    DAYS_OFF,
    UNREGISTERED,
]


def is_holiday(d):
    holidays = [d[0] for d in jpholiday.month_holidays(CURRENT_YEAR, CURRENT_MONTH)]
    return d in holidays


def is_dayoff(d):
    return d.weekday() in DAYS_OFF_INDEX


# ----------------------------------------------------------------


def load_df():
    if os.path.exists(ATTENDANCE_BOOK):
        df = pd.read_json(ATTENDANCE_BOOK)
        # preprocess
        df["日付"] = pd.to_datetime(df["日付"], format=DATE_FORMAT).dt.strftime(DATE_FORMAT)

        df.to_json(BACKUP_FILE)
    else:
        year_month = f"{CURRENT_YEAR}-{CURRENT_MONTH}-1"
        year_next_month = f"{CURRENT_YEAR}-{CURRENT_MONTH+1}-1"
        data = []
        for d in CURRENT_DAYS:
            wd = HOLIDAY if is_holiday(d) else WEEKDAYS[d.weekday()]
            ws = DAYS_OFF if (is_holiday(d) or is_dayoff(d)) else UNREGISTERED
            data.append(
                dict(
                    日付=d.strftime(DATE_FORMAT),
                    曜日=wd,
                    勤務状態=ws,
                    開始時刻=EMPTY_VALUE,
                    終了時刻=EMPTY_VALUE,
                    休憩=EMPTY_VALUE,
                    勤務時間=EMPTY_VALUE,
                    残業時間=EMPTY_VALUE,
                    進捗報告=EMPTY_VALUE,
                )
            )
        df = pd.DataFrame(data)
    return df


df = load_df()
data = list(df.to_dict("index").values())
di = (datetime.today() - datetime(CURRENT_YEAR, CURRENT_MONTH, 1)).days
today_mission = data[di]["進捗報告"]

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
    elif col in ["進捗報告"]:
        columns.append(
            {
                "name": col,
                "id": col,
                "type": "text",
                "presentation": "markdown",
            }
        )
    elif col in ["勤務状態"]:
        columns.append(
            {
                "name": col,
                "id": col,
                "type": "text",
                "presentation": "dropdown",
                "clearable": False,
            }
        )
    else:
        raise ValueError(f"Undefined column name {col} found")

app.layout = html.Div(
    children=[
        html.H1("Attendance Book"),
        html.Button("Save", id="button-save"),
        html.Div(EMPTY_VALUE, id="save-notificaiton"),
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
            data=[dict(合計勤務時間=EMPTY_VALUE, 合計残業時間=EMPTY_VALUE)],
        ),
        html.H2("進捗報告"),
        html.Div(
            children=[
                html.Div(id="intermediate-value", style={"display": "none"}),
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id="dropdown-days",
                            options=[
                                {
                                    "label": d.strftime(DATE_FORMAT),
                                    "value": d.strftime(DATE_FORMAT),
                                }
                                for d in CURRENT_DAYS
                            ],
                            value=datetime.today().strftime(DATE_FORMAT),
                        ),
                        html.Button("Update", id="button-update"),
                        html.Div(EMPTY_VALUE, id="update-notificaiton"),
                        dcc.Textarea(
                            id="textarea-report",
                            placeholder="""本日の業務内容を入力してください．Markdown で書くことができます.\n画面右側に入力内容のプレビューが行われます.""",
                            value=today_mission,
                            style={
                                "width": "95%",
                                "height": 200,
                            },
                        ),
                    ],
                    style={
                        "width": "49%",
                        "display": "inline-block",
                    },
                ),
                dcc.Markdown(
                    id="markdown-report",
                    children="""こちらに更新されます．""",
                    style={"width": "49%", "height": 100, "display": "inline-block"},
                ),
            ]
        ),
        html.H2("Table"),
        dash_table.DataTable(
            id="time-table",
            editable=True,
            columns=columns,
            data=data,
            active_cell=ACTIVE_CELL,
            export_headers="display",
            export_format="xlsx",
            style_header=dict(
                backgroundColor="rgb(230, 230, 230)",
                fontWeight="bold",
                textAlign="center",
            ),
            dropdown={
                "勤務状態": {"options": [{"label": i, "value": i} for i in WORKING_STATUS]},
            },
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"},
                {
                    "if": {
                        "column_id": ["日付", "曜日", "開始時刻", "終了時刻"],
                        "filter_query": "{開始時刻} ne '' && {終了時刻} eq ''",
                    },
                    "backgroundColor": "green",
                },
                {
                    "if": {
                        "column_id": ["日付", "曜日", "開始時刻", "終了時刻"],
                        "filter_query": "{開始時刻} eq '' && {終了時刻} ne ''",
                    },
                    "backgroundColor": "tomato",
                },
                {
                    "if": {
                        "column_id": ["日付", "曜日", "開始時刻", "終了時刻"],
                        "filter_query": "{開始時刻} ne '' && {終了時刻} ne '' && {勤務時間} <=0",
                    },
                    "backgroundColor": "red",
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
            ],
        ),
    ]
)


@app.callback(Output("markdown-report", "children"), Input("textarea-report", "value"))
def updateReport2MD(value):
    return value


@app.callback(
    Output("update-notificaiton", "children"),
    Input("markdown-report", "children"),
    Input("button-update", "n_clicks"),
    Input("dropdown-days", "value"),
    prevent_initial_call=True,
)
def updateReport(value, n_clicks, day):
    if n_clicks:
        di = (
            datetime.strptime(day, DATE_FORMAT)
            - datetime(CURRENT_YEAR, CURRENT_MONTH, 1)
        ).days
        data[di]["進捗報告"] = value
        msg = save_data(data)
        return msg


def save_data(data):
    df = pd.DataFrame(data)
    df.to_json(ATTENDANCE_BOOK)
    return f"Saved data at {ATTENDANCE_BOOK}"


@app.callback(
    Output("textarea-report", "value"),  # report
    Input("dropdown-days", "value"),  # day
    prevent_initial_call=True,
)
def dispayReportContent(day):
    df = load_df()
    data = list(df.to_dict("index").values())
    di = (
        datetime.strptime(day, DATE_FORMAT) - datetime(CURRENT_YEAR, CURRENT_MONTH, 1)
    ).days
    return data[di]["進捗報告"]


@app.callback(
    Output("save-notificaiton", "children"),
    Input("button-save", "n_clicks"),
    Input("time-table", "data"),
    prevent_initial_call=True,
)
def saveData(n_clicks, data):
    if n_clicks:
        msg = save_data(data)
        return msg


active_cell_previous = ACTIVE_CELL


def format_datatable(data):
    for d in data:
        if d["勤務状態"] in ["有給"]:
            dt = datetime.strptime(d["日付"], DATE_FORMAT)
            dt = date(dt.year, dt.month, dt.day)
            if is_holiday(dt) or is_dayoff(dt):
                d["勤務状態"] = DAYS_OFF
            d["開始時刻"] = EMPTY_VALUE
            d["終了時刻"] = EMPTY_VALUE
            d["勤務時間"] = EMPTY_VALUE
            d["残業時間"] = EMPTY_VALUE
            continue
        try:
            break_time = d["休憩"]
            if break_time:
                if break_time < 0:
                    d["休憩"] = ""
            else:
                break_time = 0
            end = datetime.strptime(d["終了時刻"], "%H:%M")
            begin = datetime.strptime(d["開始時刻"], "%H:%M")
            if (end - begin).days < 0:
                raise ValueError
            working_hours = (end - begin).seconds / 3600
            working_hours -= break_time
            d["勤務時間"] = working_hours
            d["残業時間"] = max(working_hours - STANDARD_WORKING_TIME, 0)
            d["勤務状態"] = "勤務"
        except ValueError:
            d["勤務時間"] = EMPTY_VALUE
            d["残業時間"] = EMPTY_VALUE
            dt = datetime.strptime(d["日付"], DATE_FORMAT)
            dt = date(dt.year, dt.month, dt.day)
            if is_holiday(dt) or is_dayoff(dt):
                d["勤務状態"] = DAYS_OFF
            else:
                d["勤務状態"] = UNREGISTERED

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
        str_value: str = data[row][column_id]
        if str_value.isdigit():
            value: int = int(str_value)
            if value in range(24, 24 + 6):
                value = value % 24  # will be "00:00"
            if value in range(0, 24):
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
        try:  # to parse timep
            str_value = datetime.strptime(str_value, "%H:%M").strftime("%H:%M")
            data[row][column_id] = str_value
        except Exception:
            # revert data with `previous_data`
            if str_value:  # str_value is not empty
                data[row][column_id] = data_previous[row][column_id]

    data = format_datatable(data)

    # update summary
    total_overwork_working_time = total_working_time = 0
    for d in data:
        wt = d["勤務時間"]
        over_wt = d["残業時間"]
        if not isinstance(wt, str):
            total_working_time += wt
        if not isinstance(over_wt, str):
            total_overwork_working_time += over_wt
    summary = [dict(合計勤務時間=total_working_time, 合計残業時間=total_overwork_working_time)]

    # update active_cell_previous
    active_cell_previous = active_cell
    return data, summary


if __name__ == "__main__":
    app.run_server(debug=True)
