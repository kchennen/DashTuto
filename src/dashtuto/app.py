import time

import dash_ag_grid as dag
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, State, callback, dcc, html

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv"
)

# Initialize the Dash app
app = Dash(
    name=__name__,
    title="Dash Tutorial",
    description="A Dash app following the Dash documentation.",
)

# Requires Dash 2.17.0 or later
# Main layout wrapped in MantineProvider
logo = "https://github.com/user-attachments/assets/c1ff143b-4365-4fd1-880f-3e97aab5c302"
navbar_buttons = [
    dmc.Button("Home", variant="subtle", color="gray"),
    dmc.Button("Blog", variant="subtle", color="gray"),
    dmc.Button("Contacts", variant="subtle", color="gray"),
    dmc.Button("Support", variant="subtle", color="gray"),
]

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Group(
                        [
                            dmc.Burger(
                                id="burger",
                                size="sm",
                                hiddenFrom="sm",
                                opened=False,
                            ),
                            dmc.Image(src=logo, h=40, flex=0),
                            dmc.Title("Demo App", c="blue", order=1, ml="xs"),
                        ]
                    ),
                    dmc.Group(
                        children=navbar_buttons,
                        ml="xl",
                        gap=0,
                        visibleFrom="sm",
                    ),
                ],
                justify="space-between",
                style={"flex": 1},
                h="100%",
                px="md",
            ),
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=navbar_buttons,
            py="md",
            px=4,
        ),
        dmc.AppShellMain(
            [
                dmc.Title(children="My First App with Data", order=1),
                html.Hr(),
                dcc.RadioItems(
                    options=["pop", "lifeExp", "gdpPercap"],
                    value="lifeExp",
                    id="controls-and-radio-item",
                ),
                dag.AgGrid(
                    rowData=df.to_dict("records"),
                    columnDefs=[{"field": i} for i in df.columns],
                ),
                dcc.Graph(
                    id="controls-and-graph",
                    figure=px.histogram(df, x="continent", y="lifeExp", histfunc="avg"),
                ),
            ]
        ),
        dmc.AppShellFooter(
            id="footer",
            children="Footer content",
            py="xs",
            px=5,
        ),
    ],
    header={"height": 60},
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"desktop": True, "mobile": True},
    },
    padding="md",
    id="appshell",
)

app.layout = dmc.MantineProvider(layout)


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened, "desktop": True}
    return navbar


# Add controls to build the interaction
@callback(
    Output(component_id="controls-and-graph", component_property="figure"),
    Input(component_id="controls-and-radio-item", component_property="value"),
)
def update_graph(col_chosen):
    fig = px.histogram(df, x="continent", y=col_chosen, histfunc="avg")
    return fig


if __name__ == "__main__":
    app.run(debug=True, port=8060)
