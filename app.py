# Import required libraries
import pickle
import copy
import pathlib
import dash
import math
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from data_preparation import loan_types, default_types, signed_dt_filtration, defaults_types_dropdown, \
    loans_types_dropdown, navbar_labels
from data_preparation import graph_count_data
from datetime import datetime as dt
import plotly.graph_objs as go
from data_provider import DataProvider

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.config.suppress_callback_exceptions = True


#region Navigation Bar
def build_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Портфель", href="#")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Выдачи", header=True)
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],
        brand="Мониторинг кредитов ММБ", brand_href="#",
        color="dark", dark=True, fluid=True,
    )
    return navbar
#endregion

# region DR and count blocks
def build_cards():

    def stat_card(value, desc, id):
        return dbc.Card(dbc.CardBody([
            html.Div(html.H5(value, className="text-dark", ), id=id),
            html.P(desc, className="text-muted", )
        ]), className='border border-light')

    cards = dbc.CardDeck(
        [
            stat_card(0, 'Доля дефолтов', id='dr-block'),
            stat_card(0, 'Количество заявок', id='count-block'),
            stat_card(0, 'Количество дефолтов', id='def-count-block'),
        ], id='stat-blocks',
    )

    return cards
# endregion

# region Plotting popularity graph
def plot_counts():
    count_plot_switches = dbc.FormGroup([
        dbc.Checklist(
            options=[
                {"label": "Дефолты", "value": 'default'},
                {"label": "Не дефолты", "value": 'healthy'},
                {"label": "Разбить на продукты", "value": 'decompose'},
            ],
            value=['default', 'healthy'],
            id="switches-inline-input-count-plot",
            inline=True, switch=True,
        )])
    data = provider.GetCountsData()

    graph_count = dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(html.H3("Количество клиентов/договоров"), ),
                dbc.Col(count_plot_switches, width='auto'), ], ),
            dcc.Graph(figure={"data": [{"x": data.index, "y": data.values, }, ], },
                      id='count-graph', ),
        ], className='m-1', ), ])
    return graph_count
# endregion

# region Plotting rating graph
def plot_ratings():
    #Тубмлеры графика численности
    rating_plot_switches = dbc.FormGroup([
        dbc.Checklist(
            options=[
                {"label": "Дефолты", "value": 'default'},
                {"label": "Не дефолты", "value": 'healthy'},
                {"label": "Разбить на продукты", "value": 'decompose'},
            ],
            value=['default', 'healthy'],
            id="switches-inline-input-count-plot",
            inline=True, switch=True,
        )])

    rating_graph_data = graph_count_data.groupby(['Рейтинг']).size()


    graph_rating = dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(html.H3("Рейтинги клиентов/договоров"), ),
                dbc.Col(rating_plot_switches, width='auto'), ], ),
            dcc.Graph(
                figure=go.Figure(
                    data=[go.Bar(x=rating_graph_data.index.tolist(), y=rating_graph_data.tolist(), name='SF Zoo'), ],
                    layout=go.Layout(barmode='stack')), id='rating-graph', ),
        ], className='m-1', ), ])

    return graph_rating
# endregion

def build_sidebar():
    """
    Создаёт боковую панель
    :return: Боковая панель
    """

    start_dt, end_dt = provider.GetDatesFilterBounds()
    dates_picker = {
        'start_date': start_dt,
        'end_date': end_dt,
        'label': 'Интервал дат подписания договора:',
        'html_for': "Минимальная и максимальная дата подписания договора для фильтрации выборки"
    }



    dark_theme_switch = daq.ToggleSwitch(
        id='light-dark-theme-toggle',
        label=['Light', 'Dark'],
        style={'width': '100px', 'margin': 'auto'},
        value=False,
    )

    sidebar = dbc.Col(
        [
            html.Div(
                [
                    dbc.Row(html.H5("Фильтрация портфеля")),
                    dbc.Row(dbc.Label(dates_picker['label'], html_for=dates_picker['html_for'])),
                    dbc.Row(dcc.DatePickerRange(id='date-picker-range', start_date=dates_picker['start_date'],
                                                end_date=dates_picker['end_date'], clearable=True,
                                                first_day_of_week=1, display_format='DD-MM-YYYY')),
                    dbc.Row(dbc.Label(defaults_types_dropdown['label'], html_for=defaults_types_dropdown['html_for'])),
                    dbc.Row(
                        dcc.Dropdown(options=defaults_types_dropdown['options'],
                                     value=defaults_types_dropdown['values'],
                                     id='default-types', multi=True)),
                    dbc.Row(dbc.Label(loans_types_dropdown['label'], html_for=loans_types_dropdown['html_for'])),
                    dbc.Row(dcc.Dropdown(options=loans_types_dropdown['options'], value=loans_types_dropdown['values'],
                                         id='loan-types', multi=True)),
                ], className='sticky-top',
            ),
            html.Hr(),
            dark_theme_switch,
        ], width=3,
    )
    return sidebar

def build_layout(app):
    app.layout = dbc.Container(
        [
            build_navbar(),
            html.Div(
                [
                    html.Br(),
                    dbc.Row(
                        [
                            build_sidebar(),
                            dbc.Col(
                                [
                                    build_cards(),
                                    html.Br(),
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(
                                                [
                                                    dbc.Tabs(
                                                        [
                                                            dbc.Tab(label="Количество", tab_id="tab-1",
                                                                    labelClassName="text-success"),
                                                            dbc.Tab(label="Рейтинги", tab_id="tab-2", ),
                                                        ], id="tabs", active_tab="tab-1",
                                                    ),
                                                ]
                                            ),
                                            dbc.CardBody(html.P(id="card-content", className="card-text")),
                                        ]
                                    ),
                                ], width=9,
                            )
                        ], className='m-1',
                    ),
                ], id='main-theme',
            ),
        ], fluid=True,
    )

def get_filtred_tbl(tbl, start_date, end_date, checked_default_types, checked_loan_types):
    if checked_loan_types:
        tbl = tbl[tbl['Тип продукта'].isin(checked_loan_types)]
    if checked_default_types:
        tbl = tbl[tbl['Тип дефолта'].isin(checked_default_types + [None, ])]
    if start_date:
        tbl = tbl[tbl['Дата'] >= start_date]
    if end_date:
        tbl = tbl[tbl['Дата'] < end_date]
    return tbl


@app.callback(
    Output('dr-block', 'children'),
    [
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input('default-types', 'value'),
        Input('loan-types', 'value')
    ])
def update_dr_stat_block(start_date, end_date, checked_default_types, checked_loan_types):
    plot_data = get_filtred_tbl(graph_count_data, start_date, end_date, checked_default_types, checked_loan_types)
    return html.H5('{}%'.format(round(plot_data['Дефолт'].sum() / plot_data.shape[0] * 100, 2)),
                   className="text-dark", )


@app.callback(
    Output('count-block', 'children'),
    [
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input('default-types', 'value'),
        Input('loan-types', 'value')
    ])
def update_count_stat_block(start_date, end_date, checked_default_types, checked_loan_types):
    plot_data = get_filtred_tbl(graph_count_data, start_date, end_date, checked_default_types, checked_loan_types)
    return html.H5(str(plot_data.shape[0]), className="text-dark", )


@app.callback(
    Output('def-count-block', 'children'),
    [
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input('default-types', 'value'),
        Input('loan-types', 'value')
    ])
def update_dc_stat_block(start_date, end_date, checked_default_types, checked_loan_types):
    plot_data = get_filtred_tbl(graph_count_data, start_date, end_date, checked_default_types, checked_loan_types)
    return html.H5(str(plot_data['Дефолт'].sum()), className="text-dark", )


@app.callback(
    Output('count-graph', 'figure'),
    [
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input("switches-inline-input-count-plot", "value"),
        Input('default-types', 'value'),
        Input('loan-types', 'value')
    ])
def update_count_graph(start_date, end_date, checkbox_flag, checked_default_types, checked_loan_types):
    flag_def = []
    if 'default' in checkbox_flag:
        flag_def.append(1)
    if 'healthy' in checkbox_flag:
        flag_def.append(0)
    #plot_data = graph_count_data[graph_count_data['Дефолт'].isin(flag_def)]

    #plot_data = get_filtred_tbl(plot_data, start_date, end_date, checked_default_types, checked_loan_types)
    plot_data = provider.GetCountsData(start_date, end_date, checked_default_types, checked_loan_types, 'decompose' in checkbox_flag)
    res = []
    if 'decompose' in checkbox_flag:
        for t in plot_data['Тип продукта'].unique():
            res.append({
                'x': plot_data.loc[plot_data['Тип продукта'] == t, 'Дата'],
                'y': plot_data.loc[plot_data['Тип продукта'] == t, 'Количество'],
                'name': list(loan_types.keys())[list(loan_types.values()).index(t)]
            })
        return {"data": res}
    else:
        return {"data": [{"x": plot_data.index, "y": plot_data.values, 'name': 'Сумма выбранных типов'}]}


@app.callback(
    Output('main-theme', 'style'),
    [Input('light-dark-theme-toggle', 'value')]
)
def change_bg(dark_theme):
    if dark_theme:
        return {'background-color': '#303030', 'color': '#f9f9f9'}
    else:
        return {'background-color': '#f9f9f9', 'color': 'black'}


@app.callback(
    Output("card-content", "children"),
    [Input("tabs", "active_tab")])
def tab_content(active_tab):
    if active_tab == 'tab-1':
        return plot_counts()
    elif active_tab == 'tab-2':
        return plot_ratings()
    else:
        return "Hello, where are we? I don't know {} tab.".format(active_tab)


@app.callback(
    Output("tabs", "children"),
    [Input("tabs", "active_tab")])
def tab_content(active_tab):
    if active_tab == 'tab-1':
        return [
            dbc.Tab(label="Количество", tab_id="tab-1", id='count-tab', labelClassName="text-success"),
            dbc.Tab(label="Рейтинги", tab_id="tab-2", id='rating-tab'),
        ]
    elif active_tab == 'tab-2':
        return [
            dbc.Tab(label="Количество", tab_id="tab-1", id='count-tab', ),
            dbc.Tab(label="Рейтинги", tab_id="tab-2", id='rating-tab', labelClassName="text-success"),
        ]
    else:
        return [
            dbc.Tab(label="Количество", tab_id="tab-1", id='count-tab'),
            dbc.Tab(label="Рейтинги", tab_id="tab-2", id='rating-tab'),
        ]


if __name__ == "__main__":
    provider = DataProvider()

    build_layout(app)
    app.run_server(debug=True)
