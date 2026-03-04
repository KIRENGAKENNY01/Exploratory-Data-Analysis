import plotly.express as px
import plotly.offline as opy
import plotly.graph_objects as go
import json
from plotly.utils import PlotlyJSONEncoder

import pandas as pd

def frequency_table(df):
    # Simple counts
    manufacturer_counts = df['manufacturer'].value_counts().reset_index()
    manufacturer_counts.columns = ['Manufacturer', 'Count']
    
    # Convert to HTML using the correct method name: .to_html()
    table_html = manufacturer_counts.to_html(
        classes="table table-bordered table-striped table-sm", 
        float_format='%.2f',
        justify='center'
    )
    return table_html


def display_my_dataset(df):
        return df.head(10).to_html(
        index=False, 
        classes="table table-bordered table-striped table-sm", 
        justify='center'
    )

def aggregated_df(df):
    df["profit"] = df["selling_price"] - df["wholesale_price"]
    
    grouped = df.groupby(['manufacturer', 'transmission', 'fuel_type']).agg({
        'selling_price': 'sum',
        'wholesale_price': 'sum',
        'profit': 'sum'
    })
    
    return grouped.to_html(
        classes="table table-bordered table-striped table-sm", 
        justify='center'
    )

def crossed_table(df):

    
    crossed = pd.crosstab(df['manufacturer'], df['body_type'], values = df['selling_price'], aggfunc=["sum"], margins=True)

    return crossed.to_html(
        classes="table table-bordered table-striped table-sm",
        justify='center'
    )

def pivot_table(df):
    pivot = pd.pivot_table(df, values='selling_price', index='manufacturer', columns='fuel_type', aggfunc=['sum','mean'])
    return pivot.to_html(
        classes="table table-bordered table-striped table-sm",
        float_format='%.2f',
        justify='center'
    )


def visualizing_sales_with_sunburst_chart(df, height=800):
    fig = px.sunburst(df, path=["manufacturer", "body_type"], values="selling_price")
    fig.update_traces(textinfo="label+value")
    fig.update_layout(height=height)
    return opy.plot(fig,auto_open=False,output_type="div")


def visualizing_sales_with_treemap_chart(df, height=800):
    fig = px.treemap(df, path=["manufacturer", "body_type"], values="selling_price")
    fig.update_traces(textinfo="label+value")
    fig.update_layout(height=height)
    return opy.plot(fig,auto_open=False,output_type="div")


def frequency_bar_chart(df):
    # Simple counts
    manufacturer_counts = df['manufacturer'].value_counts().reset_index()
    manufacturer_counts.columns = ['Manufacturer', 'Count']
    
    # Convert to HTML using the correct method name: .to_html()
    fig= px.bar(
        manufacturer_counts,
        x='Manufacturer',
        y='Count',
        title='Vehicle Count by Manufacturer',  
        text='Count'
    )
    fig.update_layout(
        xaxis_title='Manufacturer',
        yaxis_title='Count',
        template='plotly_white'
    )
    graph_html= opy.plot(fig,auto_open=False,output_type="div")
    return graph_html



def crosstab_multi(df):
    cross = pd.crosstab([df["manufacturer"],df['body_type'],df["fuel_type"]],[df["transmission"],df["vehicle_condition"],df["engine_type"]],values = df["selling_price"],aggfunc ="sum",margins=True)

    return cross.to_html(
        classes="table table-bordered table-striped table-sm",
        float_format='%.2f',
        justify='center'
    )

def crosstab(df):
    cross = pd.crosstab(df["manufacturer"],df['body_type'],values = df["selling_price"],aggfunc =["sum",(lambda x : x.max() - x.min())])

    return cross.to_html(
        classes="table table-bordered table-striped table-sm",
        float_format='%.2f',
        justify='center'
    )


def visualize_map(df,height=800):
    country_counts = df.groupby("client_country").size().reset_index(name="vehicle_count")
    fig = px.choropleth(
        country_counts,
        locations="client_country",
        locationmode="country names",
        color="vehicle_count",
        hover_name="client_country",
        projection="natural earth",
        title="Total Vehicles by Country",
        color_continuous_scale=px.colors.sequential.Plasma
    )



    fig.add_trace(
        go.Scattergeo(
            locations=country_counts["client_country"],
            locationmode="country names",
            text=country_counts.apply(lambda row: f"{row['client_country']}<br>{row['vehicle_count']} Vehicles", axis=1),
            mode="text",
            showlegend=False,
            hoverinfo="skip"
        )
        )

    # Layout adjustments to make labels more readable
    fig.update_layout(
        margin={"r":0,"t":50,"l":0,"b":0},
        title=dict(x=0.5, xanchor='center')
    )

    div = opy.plot(fig, auto_open=False, output_type='div', include_plotlyjs=True)
    return div