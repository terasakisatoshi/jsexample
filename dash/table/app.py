# -*- coding: utf-8 -*-
import os
from datetime import datetime
import dash
import dash_table
from dash_table.Format import Format, Group, Padding
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

# ----------------------------------------------------------------

WEEKDAYS = ["月", "火", "水", "木", "金", "土", "日"]
ACTIVE_CELL = {"row": 0, "column": 2, "column_id": "Begin"}
CURRENT_YEAR_MONTH = datetime.today().strftime("%Y_%m")
ATTENDANCE_BOOK = (
    f"{os.path.dirname(__file__)}/.data/{CURRENT_YEAR_MONTH}_attendance_book.json"
)
BACKUP_FILE = f"{os.path.dirname(__file__)}/.backup/{os.path.basename(ATTENDANCE_BOOK)}"

# ----------------------------------------------------------------

if os.path.exists(ATTENDANCE_BOOK):
    df = pd.read_json(ATTENDANCE_BOOK)
    # preprocess
    df["Date"] = pd.to_datetime(df["Date"], format="%Y/%m/%d").dt.strftime("%Y/%m/%d")

    df.to_json(BACKUP_FILE)
else:
    y = datetime.today().year
    m = datetime.today().month
    year_month = f"{y}-{m}-1"
    year_next_month = f"{y}-{m+1}-1"
    dates = pd.to_datetime(pd.date_range(year_month, year_next_month)[:-1]).map(
        lambda d: d.to_pydatetime()
    )
    data = []
    for d in dates:
        data.append(
            dict(
                Date=d.to_pydatetime().strftime("%Y/%m/%d"),
                DoW=WEEKDAYS[d.weekday()],
                Begin="",
                End="",
                TODO="",
            )
        )
    df = pd.DataFrame(data)

data = list(df.to_dict("index").values())

app = dash.Dash(__name__)

columns = []
for col in df.columns:
    if col in ["Date", "DoW"]:
        columns.append(
            {
                "name": col,
                "id": col,
                "type": "text",
                "editable": False,
            }
        )
    elif col in ["Begin", "End"]:
        columns.append(
            {
                "name": col,
                "id": col,
                "type": "numeric",
                "format": Format(
                    group_delimiter=":",
                    padding=Padding.yes,
                    padding_width=4 + 1,
                    group=Group.yes,
                    groups=[2],
                ),
            }
        )
    else:
        columns.append(
            {
                "name": col,
                "id": col,
                "type": "text",
            }
        )

app.layout = html.Div(
    children=[
        html.H1("Attendance Book"),
        html.Button("Save", id="save-button"),
        html.Div("", id="save-status"),
        dash_table.DataTable(
            id="time-table",
            editable=True,
            columns=columns,
            data=data,
            active_cell=ACTIVE_CELL,
            style_data_conditional=[
                {
                    "if": {
                        "column_id": ["Date", "DoW", "Begin", "End"],
                        "filter_query": "{Begin} > {End}",
                    },
                    "backgroundColor": "tomato",
                },
                {
                    "if": {
                        "column_id": ["Date", "DoW"],
                        "filter_query": "{DoW} eq '土'",
                    },
                    "color": "blue",
                },
                {
                    "if": {
                        "column_id": ["Date", "DoW"],
                        "filter_query": "{DoW} eq '日'",
                    },
                    "color": "red",
                },
            ],
        ),
    ]
)


@app.callback(
    Output("save-status", "children"),
    Input("save-button", "n_clicks"),
    Input("time-table", "data"),
)
def saveData(n_clicks, data):
    if n_clicks:
        df = pd.DataFrame(data)
        df.to_json(ATTENDANCE_BOOK)
        return f"Saved data at {ATTENDANCE_BOOK}"
    else:
        return ""


active_cell_previous = ACTIVE_CELL


@app.callback(
    Output("time-table", "data"),
    Input("time-table", "active_cell"),
    Input("time-table", "data_previous"),
    Input("time-table", "data"),
    prevent_initial_call=True,
)
def updateData(active_cell, data_previous, data):
    global active_cell_previous
    if active_cell_previous["column_id"] in ["Data", "DoW"]:
        # Just upate activate_cell
        active_cell_previous = active_cell
        return data
    else:
        row = active_cell_previous["row"]
        column_id = active_cell_previous["column_id"]
        value = data[row][column_id]
        if isinstance(value, int):
            # e.g.
            # 145 -> 145
            # 12345 -> 2345
            # 99999 -> 9999
            value %= 10000
            # zero padding
            # 145 -> 0145
            # 2345 -> 2345
            # 9999 -> 9999
            str_value = str(value).zfill(4)
            # format with HH:MM
            # 0145 -> 01:45
            # 2345 -> 23:45
            # 9999 -> 99:99
            print("str_value", str_value)
            try:
                str_value = ":".join([str_value[0:2], str_value[2:4]])
                str_value = datetime.strptime(str_value, "%H:%M").strftime("%H:%M")
                data[row][column_id] = str_value
            except ValueError:
                print("Error")
                # revert data with `previous_data`
                data[row][column_id] = data_previous[row][column_id]
                pass
        active_cell_previous = active_cell
    return data


if __name__ == "__main__":
    app.run_server(debug=True)
