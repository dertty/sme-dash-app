# Import required libraries
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
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
            stat_card(0, 'Доля дефолтов', id='er-block'),
            stat_card(0, 'Количество заявок', id='count-block'),
            stat_card(0, 'Количество дефолтов', id='def-count-block'),
        ], id='stat-blocks',
    )

    return cards
# endregion

# region Plotting popularity graph
def plot_counts():

    data = provider.GetCountsData()
    graph_count = dbc.Row([
        dbc.Col([
            dbc.Row(dbc.Col(html.H3("Количество клиентов/договоров"))),
            dcc.Graph(figure={"data": [{"x": data.index, "y": data.values, }, ], },
                      id='count-graph', ),
        ], className='m-1', ), ])
    return graph_count
# endregion

# region Plotting rating graph
def plot_ratings():
    rating_graph_data = provider.GetRatingData()

    graph_rating = dbc.Row([
        dbc.Col([
            dbc.Row(dbc.Col(html.H3("Рейтинги клиентов/договоров"))),
            dcc.Graph(
                figure=go.Figure(
                    data=[go.Bar(x=rating_graph_data.index.tolist(), y=rating_graph_data.tolist(), name='SF Zoo'), ],
                    layout=go.Layout(barmode='stack')), id='rating-graph', ),
        ], className='m-1', ), ])

    return graph_rating
# endregion

# region Plotting DR graph
def plot_dr():
    dr_data = provider.GetDRData()
    dr_graph = dbc.Row([
        dbc.Col([
            dbc.Row(dbc.Col(html.H3("Default rate"))),
            dcc.Graph(figure={"data": [{"x": dr_data.index, "y": dr_data.values, }, ], },
                      id='dr-graph', ),
        ], className='m-1', ), ])
    return dr_graph
# endregion


def build_sidebar():
    """
    Создаёт боковую панель
    :return: Боковая панель
    """

    start_dt, end_dt = provider.GetDatesBounds
    dates_picker = {
        'start_date': start_dt,
        'end_date': end_dt,
        'label': 'Интервал дат подписания договора:',
        'html_for': "Минимальная и максимальная дата подписания договора для фильтрации выборки"
    }

    product_types = provider.GetProductTypes;
    loans_types_dropdown = {
        'options': [{'label':t, 'value':t} for t in product_types],
        'values': [*product_types],
        'label': 'Типы ссуд:',
        'html_for': "Выберите типы ссуд для фильтрации выборки"
    }

    default_reasons = provider.GetDefaultReasons
    defaults_types_dropdown = {
        'options': [{'label':r, 'value': r} for r in default_reasons],
        'values': [*default_reasons],
        'label': 'Виды дефолтов:',
        'html_for': "Выберите типы дефолтов для фильтрации выборки"
    }

    count_plot_switches = dbc.FormGroup([
        dbc.Checklist(
            options=[
                {"label": "Находящиеся в дефолте", "value": 'default'},
                {"label": "Ненаходящиеся в дефолте", "value": 'healthy'},
                {"label": "Разбить на продукты", "value": 'decompose'},
            ],
            value=['default', 'healthy'],
            id="switches-inline-input-count-plot",
            inline=True, switch=True,
        )])

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
                    dbc.Row(dbc.Label('Что показывать:', html_for='')),
                    count_plot_switches
                ], className='sticky-top',
            ),
            html.Hr(),
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
                                                            dbc.Tab(label="DR", tab_id="tab-3", ),
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


#region Callbacks
@app.callback(
    Output('er-block', 'children'),
    [
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input('default-types', 'value'),
        Input('loan-types', 'value')
    ])
def update_dr_stat_block(start_date, end_date, checked_default_types, checked_loan_types):
    dr = provider.GetEventRateStat(start_date = start_date, end_date = end_date, checked_default_types=checked_default_types, checked_loan_types=checked_loan_types)
    return html.H5('{}%'.format(round(dr * 100, 2)), className="text-dark", )


@app.callback(
    Output('count-block', 'children'),
    [
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input('default-types', 'value'),
        Input('loan-types', 'value')
    ])
def update_count_stat_block(start_date, end_date, checked_default_types, checked_loan_types):
    count_stat = provider.GetCountStat(start_date = start_date, end_date=end_date, checked_default_types=checked_default_types, checked_loan_types=checked_loan_types)
    return html.H5(str(count_stat), className="text-dark", )


@app.callback(
    Output('def-count-block', 'children'),
    [
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input('default-types', 'value'),
        Input('loan-types', 'value')
    ])
def update_dc_stat_block(start_date, end_date, checked_default_types, checked_loan_types):
    defaults_count = provider.GetDefaultsCount(start_date=start_date, end_date=end_date, checked_default_types=checked_default_types,
                                               checked_loan_types=checked_loan_types)
    return html.H5(str(defaults_count), className="text-dark", )


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
    default_state = []
    if 'default' in checkbox_flag:
        default_state.append(1)
    if 'healthy' in checkbox_flag:
        default_state.append(0)

    plot_data = provider.GetCountsData(default_state = default_state, start_date = start_date, end_date = end_date,
                                       checked_default_types = checked_default_types, checked_loan_types = checked_loan_types,
                                       product_decompose='decompose' in checkbox_flag)
    res = []
    if 'decompose' in checkbox_flag:
        for t in plot_data['credit_type'].unique():
            res.append({
                'x': plot_data.loc[plot_data['credit_type'] == t, 'report_dt'],
                'y': plot_data.loc[plot_data['credit_type'] == t, 'total'],
                'name': t
            })
        return {"data": res}
    else:
        return {"data": [{"x": plot_data.index, "y": plot_data.values, 'name': 'Сумма выбранных типов'}]}

@app.callback(
    Output('rating-graph', 'figure'),
    [
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input("switches-inline-input-count-plot", "value"),
        Input('default-types', 'value'),
        Input('loan-types', 'value')
    ])
def update_rating_graph(start_date, end_date, checkbox_flag, checked_default_types, checked_loan_types):
    flag_def = []
    if 'default' in checkbox_flag:
        flag_def.append(1)
    if 'healthy' in checkbox_flag:
        flag_def.append(0)

    rating_data = provider.GetRatingData(start_date = start_date, end_date = end_date, checked_default_types=checked_default_types,
                                         checked_loan_types = checked_loan_types)

    return {"data": [go.Bar(x=rating_data.index, y=rating_data.values, name='Распределение рейтингов')]}

@app.callback(
    Output('dr-graph', 'figure'),
    [
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input("switches-inline-input-count-plot", "value"),
        Input('default-types', 'value'),
        Input('loan-types', 'value')
    ])
def update_dr_graph(start_date, end_date, checkbox_flag, checked_default_types, checked_loan_types):
    plot_data = provider.GetDRData(start_date = start_date, end_date = end_date,
                                       checked_default_types = checked_default_types, checked_loan_types = checked_loan_types,
                                       product_decompose='decompose' in checkbox_flag)
    res = []
    if 'decompose' in checkbox_flag:
        for t in plot_data['credit_type'].unique():
            res.append({
                'x': plot_data.loc[plot_data['credit_type'] == t, 'report_dt'],
                'y': plot_data.loc[plot_data['credit_type'] == t, 'dr'],
                'name': t
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
    elif active_tab == 'tab-3':
        return plot_dr()
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
            dbc.Tab(label="DR", tab_id="tab-3", id='dr-tab'),
        ]
    elif active_tab == 'tab-2':
        return [
            dbc.Tab(label="Количество", tab_id="tab-1", id='count-tab', ),
            dbc.Tab(label="Рейтинги", tab_id="tab-2", id='rating-tab', labelClassName="text-success"),
            dbc.Tab(label="DR", tab_id="tab-3", id='dr-tab'),
        ]
    elif active_tab == 'tab-3':
        return [
            dbc.Tab(label="Количество", tab_id="tab-1", id='count-tab', ),
            dbc.Tab(label="Рейтинги", tab_id="tab-2", id='rating-tab'),
            dbc.Tab(label="DR", tab_id="tab-3", id='dr-tab', labelClassName="text-success"),
        ]
    else:
        return [
            dbc.Tab(label="Количество", tab_id="tab-1", id='count-tab'),
            dbc.Tab(label="Рейтинги", tab_id="tab-2", id='rating-tab'),
            dbc.Tab(label="DR", tab_id="tab-3", id='dr-tab'),
        ]
#endregion

if __name__ == "__main__":
    provider = DataProvider()

    build_layout(app)
    app.run_server(debug=True)
