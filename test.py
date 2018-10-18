from pandas2pygal import pandas_to_pygal_Bar, colour_dict
import pandas2pygal
import pandas
from pygal.style import Style

data_path = "./data/Sample - Superstore Sales (Excel).xlsx"
data = pandas.read_excel(data_path, sheet_name = "Orders")

pyg = pandas_to_pygal_Bar(
    data = data,
    groupby1 = 'Region',
    aggregate = 'Sales',
    colourstyle= colour_dict["RedBlueStyle"],
    decimal_places=0,
    print_values = False,
    rounded_bars = 0,
    title = "Test Bar Chart",
    value_suffix = "",
    x_label_rotation = 0,
    legend_at_bottom=True,
    legend_at_bottom_columns = 3,
    horizontal = False,
    agg_type = "sum")

pyg.render_in_browser()