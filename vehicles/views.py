from django.shortcuts import render

# Create your views here.
import pandas as pd

from django.shortcuts import render
from .dashboard import frequency_table , display_my_dataset ,aggregated_df , crossed_table,  pivot_table ,visualizing_sales_with_sunburst_chart , visualizing_sales_with_treemap_chart ,frequency_bar_chart,visualize_map

def dashboard_view(request):
    queryset = pd.read_csv("dummy_data/vehicles_data_1000.csv")
    df = pd.DataFrame(queryset)

    return render(request, "vehicles/index.html", {
        "frequency_table": frequency_table(df),
        "my_dataset": display_my_dataset(df),
        "aggregated_data":aggregated_df(df),
        "crossed_table":crossed_table(df),
        "pivot_table": pivot_table(df),
        "Sunbust_chart":visualizing_sales_with_sunburst_chart(df),
        "Treemap_chart":visualizing_sales_with_treemap_chart(df),
        "frequency_bar_chart":frequency_bar_chart(df),
        "visualize_map":visualize_map(df)

    })
