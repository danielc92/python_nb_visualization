import pygal
from pygal import style
import pandas
import datetime

colour_dict = {"BlueStyle": style.BlueStyle,
               "DefaultStyle": pygal.style.DefaultStyle,
               "DarkStyle": pygal.style.DarkStyle,
               "NeonStyle": pygal.style.NeonStyle,
               "DarkSolarizedStyle": pygal.style.DarkSolarizedStyle,
               "LightSolarizedStyle": pygal.style.LightSolarizedStyle,
               "LightStyle": pygal.style.LightStyle,
               "CleanStyle": pygal.style.CleanStyle,
               "RedBlueStyle": pygal.style.RedBlueStyle,
               "DarkColorizedStyle": pygal.style.DarkColorizedStyle,
               "LightColorizedStyle": pygal.style.LightColorizedStyle,
               "TurquoiseStyle": pygal.style.TurquoiseStyle,
               "LightGreenStyle": pygal.style.LightGreenStyle,
               "DarkGreenStyle": pygal.style.DarkGreenStyle,
               "DarkGreenBlueStyle": pygal.style.DarkGreenBlueStyle,
               "BlueStyle": pygal.style.BlueStyle}

#SET COLOUR HERE
global_style = colour_dict["RedBlueStyle"]

# HELPER FUNCTIONS
def return_aggregate_series(series_object, agg_type):
    
    agg_type = agg_type.lower().strip()
    
    if agg_type != "sum" and agg_type !=  "count" and agg_type != "countd":
        print("Incorrect aggregate type chosen, aggregate type has been set to sum.")
        agg_type = "sum"
    
    if agg_type == "sum":
        return series_object.sum()
    
    elif agg_type == "count":
        return series_object.count()
    
    elif agg_type == "countd":
        return series_object.nunique()


# CORE FUNCTIONS

def pandas_to_pygal_Bar(
    data,
    groupby1,
    aggregate,
    colourstyle=colour_dict["DefaultStyle"],
    decimal_places=0,
    print_values = False,
    rounded_bars = 0,
    title = "Test Bar Chart",
    value_suffix = "",
    x_label_rotation = 0,
    legend_at_bottom=False,
    legend_at_bottom_columns = 3,
    horizontal = False,
    agg_type = "sum"):
    
    
    '''
    Create pygal object
    '''
    if horizontal == True:
        pyg = pygal.HorizontalBar()
    else:
        pyg = pygal.Bar()
    
    '''
    Transform data for pygal object
    '''
    groupby1_distinct = sorted(data[groupby1].unique())
    
    value_dict = {}
    
    for name in groupby1_distinct:
            subset_data = data[data[groupby1] == name]
            aggregate_value = return_aggregate_series(subset_data[aggregate], agg_type)
            value_dict[name] = aggregate_value
      
    zipped = sorted(zip(value_dict.values(),
                        value_dict.keys()), reverse = True)
    
    '''
    Add data to pygal object
    '''
    
    for tuple_item in list(zipped):
        pyg.add(tuple_item[1], tuple_item[0])
        
    '''
    Chart configuration options
    '''
    pyg.config.rounded_bars = rounded_bars
    pyg.config.style = colourstyle
    pyg.config.title = title
    pyg.config.legend_at_bottom = legend_at_bottom
    pyg.config.legend_at_bottom_columns = legend_at_bottom_columns
    pyg.config.x_label_rotation = x_label_rotation
    pyg.config.print_values = print_values
    formatter = "{:,." + str(decimal_places) + "f} " + str(value_suffix)
    pyg.config.formatter = lambda x : formatter.format(x)

    '''
    Return chart object
    '''
    return pyg


def pandas_to_pygal_Line(
    data,
    groupby1,
    aggregate,
    colourstyle=colour_dict["DefaultStyle"],
    decimal_places=0,
    print_values = False,
    title = "Test Bar Chart",
    value_suffix = "",
    x_label_rotation = 0,
    fill = False,
    legend_at_bottom=False,
    legend_at_bottom_columns = 3,
    agg_type = "sum"):
    
    '''
    Create pygal object
    '''
    pyg = pygal.Line()
    
    '''
    Transform data for pygal object
    '''
    groupby1_distinct = sorted(data[groupby1].unique())
    values = []
    for name in groupby1_distinct:
            subset_data = data[data[groupby1] == name]
            aggregate_value = return_aggregate_series(subset_data[aggregate], agg_type)
            values.append(aggregate_value)
    
    '''
    Add data to pygal object
    '''
    pyg.add(aggregate , values)
    
    
    '''
    Chart configuration options
    '''
    pyg.config.style = colourstyle
    pyg.config.x_labels = groupby1_distinct
    pyg.config.title = title
    pyg.config.fill = fill
    pyg.config.legend_at_bottom = legend_at_bottom
    pyg.config.legend_at_bottom_columns = legend_at_bottom_columns
    pyg.config.x_label_rotation = x_label_rotation
    pyg.config.print_values = print_values
    formatter = "{:,." + str(decimal_places) + "f} " + str(value_suffix)
    pyg.config.formatter = lambda x : formatter.format(x)
    pyg.x_labels_major_every = 3
    pyg.x_labels_major_count = 6
    
    '''
    Return chart object
    '''
    return pyg

def pandas_to_pygal_Radar(
    data,
    groupby1,
    groupby2,
    aggregate,
    absolute_values=True,
    colourstyle=colour_dict["DefaultStyle"],
    decimal_places=0,
    fill=True,
    horizontal = False,
    print_values = False,
    title = "Test Grouped Bar Chart",
    value_suffix = "",
    legend_at_bottom = False,
    legend_at_bottom_columns = 3,
    agg_type = "sum"):

    '''
    Create pygal object
    '''
    
    pyg = pygal.Radar()
        
    '''
    Transform data for pygal object
    '''
    
    groupby1_distinct = sorted(data[groupby1].unique())
    groupby2_distinct = sorted(data[groupby2].unique())

    dict = {}

    for name in groupby2_distinct:
        dict[name] = []

    for name in groupby2_distinct:
        for name2 in groupby1_distinct:
            subset_data = data[(data[groupby1] == name2) & (data[groupby2] == name)]
            rows_in_subset_data = subset_data.shape[0]
            aggregate_value = return_aggregate_series(subset_data[aggregate], agg_type)

            if rows_in_subset_data > 0:
                dict[name].append(aggregate_value)
            else:
                dict[name].append(None)
                
    if absolute_values == False:
        totals = []

        dict_values_lists = list(dict.values())
        number_of_lists = len(dict_values_lists)
        number_of_items_per_list = len(dict_values_lists[0])

        for index in range(number_of_items_per_list):
            total = 0
            for index2 in range(number_of_lists):
                current_value = dict_values_lists[index2][index]
                if current_value is not None:
                    total = total + current_value
            totals.append(total)

        percentage_dict = {}
        
        for key in dict.keys():
            percentage_dict[key] = []

        for key in dict.keys():
            for index in range(len(dict[key])):
                numerator = dict[key][index]
                denominator = totals[index]
                if numerator is not None and denominator is not None:
                    percentage_dict[key].append(numerator/denominator *100)
                else:
                    percentage_dict[key].append(None)
    '''
    Add data to pygal object
    '''
    if absolute_values == True:
        for key in dict.keys():
            pyg.add(key, dict[key])
    else:
        for key in percentage_dict.keys():
            pyg.add(key, percentage_dict[key])
    
    
    '''
    Chart configuration options
    '''
    pyg.config.legend_at_bottom = legend_at_bottom
    pyg.config.legend_at_bottom_columns = legend_at_bottom_columns
    pyg.config.style = colourstyle
    pyg.config.x_labels = groupby1_distinct
    pyg.config.fill = fill
    pyg.config.title = title
    pyg.config.print_values = print_values
    formatter = "{:,." + str(decimal_places) + "f} " + str(value_suffix)
    pyg.config.formatter = lambda x : formatter.format(x)
    
    '''
    Return chart object
    '''
    return pyg


def pandas_to_pygal_Dot(
    data,
    groupby1,
    groupby2,
    aggregate,
    absolute_values=True,
    colourstyle=colour_dict["DefaultStyle"],
    decimal_places=0,
    fill=False,
    print_values = False,
    title = "Test Dot Chart",
    value_suffix = "",
    x_label_rotation = 0,
    legend_at_bottom = False,
    legend_at_bottom_columns = 3,
    agg_type = "sum"):

    '''
    Create pygal object
    '''
    
    pyg = pygal.Dot()
        
    '''
    Transform data for pygal object
    '''
    
    groupby1_distinct = sorted(data[groupby1].unique())
    groupby2_distinct = sorted(data[groupby2].unique())

    dict = {}

    for name in groupby2_distinct:
        dict[name] = []

    for name in groupby2_distinct:
        for name2 in groupby1_distinct:
            subset_data = data[(data[groupby1] == name2) & (data[groupby2] == name)]
            rows_in_subset_data = subset_data.shape[0]
            aggregate_value = return_aggregate_series(subset_data[aggregate], agg_type)

            if rows_in_subset_data > 0:
                dict[name].append(aggregate_value)
            else:
                dict[name].append(None)
                
    if absolute_values == False:
        totals = []

        dict_values_lists = list(dict.values())
        number_of_lists = len(dict_values_lists)
        number_of_items_per_list = len(dict_values_lists[0])

        for index in range(number_of_items_per_list):
            total = 0
            for index2 in range(number_of_lists):
                current_value = dict_values_lists[index2][index]
                if current_value is not None:
                    total = total + current_value
            totals.append(total)

        percentage_dict = {}
        
        for key in dict.keys():
            percentage_dict[key] = []

        for key in dict.keys():
            for index in range(len(dict[key])):
                numerator = dict[key][index]
                denominator = totals[index]
                if numerator is not None and denominator is not None:
                    percentage_dict[key].append(numerator/denominator *100)
                else:
                    percentage_dict[key].append(None)
    '''
    Add data to pygal object
    '''
    if absolute_values == True:
        for key in dict.keys():
            pyg.add(key, dict[key])
    else:
        for key in percentage_dict.keys():
            pyg.add(key, percentage_dict[key])
    
    
    '''
    Chart configuration options
    '''
    pyg.config.legend_at_bottom = legend_at_bottom
    pyg.config.legend_at_bottom_columns = legend_at_bottom_columns
    pyg.config.style = colourstyle
    pyg.config.x_labels = groupby1_distinct
    pyg.config.fill = fill
    pyg.config.title = title
    pyg.config.x_label_rotation = x_label_rotation
    pyg.config.print_values = print_values
    formatter = "{:,." + str(decimal_places) + "f} " + str(value_suffix)
    pyg.config.formatter = lambda x : formatter.format(x)
    
    '''
    Return chart object
    '''
    return pyg

def pandas_to_pygal_StackedMultiBar(
    data,
    groupby1,
    groupby2,
    aggregate,
    absolute_values=True,
    colourstyle=colour_dict["DefaultStyle"],
    decimal_places=0,
    fill=False,
    horizontal = False,
    print_values = False,
    rounded_bars = 0,
    stacked = False,
    title = "Test Grouped Bar Chart",
    value_suffix = "",
    x_label_rotation = 0,
    legend_at_bottom = False,
    legend_at_bottom_columns = 3,
    agg_type = "sum"):

    '''
    Create pygal object
    '''
    
    if horizontal == True and stacked == True:
        pyg = pygal.HorizontalStackedBar()

    elif horizontal == True and stacked == False:
        pyg = pygal.HorizontalBar()

    elif horizontal == False and stacked == True:
        pyg = pygal.StackedBar()

    else:
        pyg = pygal.Bar()
        
    '''
    Transform data for pygal object
    '''
    
    groupby1_distinct = sorted(data[groupby1].unique())
    groupby2_distinct = sorted(data[groupby2].unique())

    dict = {}

    for name in groupby2_distinct:
        dict[name] = []

    for name in groupby2_distinct:
        for name2 in groupby1_distinct:
            subset_data = data[(data[groupby1] == name2) & (data[groupby2] == name)]
            rows_in_subset_data = subset_data.shape[0]
            aggregate_value = return_aggregate_series(subset_data[aggregate], agg_type)

            if rows_in_subset_data > 0:
                dict[name].append(aggregate_value)
            else:
                dict[name].append(None)
                
    if absolute_values == False:
        totals = []

        dict_values_lists = list(dict.values())
        number_of_lists = len(dict_values_lists)
        number_of_items_per_list = len(dict_values_lists[0])

        for index in range(number_of_items_per_list):
            total = 0
            for index2 in range(number_of_lists):
                current_value = dict_values_lists[index2][index]
                if current_value is not None:
                    total = total + current_value
            totals.append(total)

        percentage_dict = {}
        
        for key in dict.keys():
            percentage_dict[key] = []

        for key in dict.keys():
            for index in range(len(dict[key])):
                numerator = dict[key][index]
                denominator = totals[index]
                if numerator is not None and denominator is not None:
                    percentage_dict[key].append(numerator/denominator *100)
                else:
                    percentage_dict[key].append(None)
    '''
    Add data to pygal object
    '''
    if absolute_values == True:
        for key in dict.keys():
            pyg.add(key, dict[key])
    else:
        for key in percentage_dict.keys():
            pyg.add(key, percentage_dict[key])
    
    
    '''
    Chart configuration options
    '''
    pyg.config.rounded_bars = rounded_bars
    pyg.config.legend_at_bottom = legend_at_bottom
    pyg.config.legend_at_bottom_columns = legend_at_bottom_columns
    pyg.config.style = colourstyle
    pyg.config.x_labels = groupby1_distinct
    pyg.config.fill = fill
    pyg.config.title = title
    pyg.config.x_label_rotation = x_label_rotation
    pyg.config.print_values = print_values
    formatter = "{:,." + str(decimal_places) + "f} " + str(value_suffix)
    pyg.config.formatter = lambda x : formatter.format(x)
    
    '''
    Return chart object
    '''
    return pyg

def pandas_to_pygal_Pie(data,
                        groupby1,
                        aggregate,
                        colourstyle = colour_dict["DarkGreenStyle"],
                        decimal_places = 0,
                        value_suffix = "",
                        inner_rad = .5,
                        half_pie = False,
                        title = "Pie Chart Title",
                        fill = False,
                        print_values = False,
                        x_label_rotation = False,
                        absolute_values = True,
                        legend_at_bottom = False,
                        legend_at_bottom_columns = 3,
                        agg_type = "sum"):

    '''
    Create pygal object
    '''
    pyg = pygal.Pie()
    
    
    '''
    Transform data for visualization
    '''
    groupby1_distinct = sorted(data[groupby1].unique())

    dict = {}
    for item in groupby1_distinct:
        dict[item] = []
        
    total = return_aggregate_series(data[aggregate], agg_type)
    
    for name in groupby1_distinct:
        subset_data = data[(data[groupby1] == name)]
        aggregate_value = return_aggregate_series(subset_data[aggregate], agg_type)

        if absolute_values == True:
            dict[name].append(aggregate_value)
        else:
            dict[name].append(aggregate_value/total*100)
            
    '''
    Add values to pygal object
    '''

    zipped = sorted(zip(dict.values(),dict.keys()))
    
    for value_tuple in zipped:
        pyg.add(value_tuple[1], value_tuple[0])

    '''
    Chart configuration options
    '''
                    
    pyg.config.legend_at_bottom = legend_at_bottom
    pyg.config.half_pie = half_pie
    pyg.config.inner_radius = inner_rad
    pyg.config.style = colourstyle
    pyg.config.fill = fill
    pyg.config.title = title
    pyg.config.x_label_rotation = x_label_rotation
    pyg.config.print_values = print_values
    pyg.config.legend_at_bottom_columns = legend_at_bottom_columns
    formatter = "{:,." + str(decimal_places) + "f} " + str(value_suffix)
    pyg.config.formatter = lambda x: formatter.format(x)

    '''
    Return chart object
    '''
    return pyg


def pandas_to_pygal_Gauge(data,
                          groupby1,
                          aggregate,
                          target_value=100,
                          colourstyle=colour_dict["DarkGreenStyle"],
                          decimal_places=0,
                          value_suffix="",
                          inner_rad=.5,
                          half_pie=False,
                          title="Pie Chart Title",
                          absolute_values=True,
                          fill=False,
                          print_values=False,
                          x_label_rotation=False,
                          legend_at_bottom=False,
                          legend_at_bottom_columns=3,
                          agg_type="sum"):
    '''
    Create pygal object
    '''
    pyg = pygal.SolidGauge()
    
    '''
    Transform data for pygal object
    '''

    groupby1_distinct = sorted(data[groupby1].unique())

    dict = {}
    for item in groupby1_distinct:
        dict[item] = []

    total = return_aggregate_series(data[aggregate], agg_type)

    for name in groupby1_distinct:
        subset_data = data[(data[groupby1] == name)]
        aggregate_value = return_aggregate_series(subset_data[aggregate],
                                                  agg_type)

        if absolute_values == True:
            dict[name] = aggregate_value
        else:
            dict[name] = aggregate_value / total * 100

    '''
    Add data to pygal object
    '''
    
    zipped = sorted(zip(dict.values(), dict.keys()), reverse=True)
    
    for value_tuple in zipped:
        pyg.add(value_tuple[1], [{
            "value": float(value_tuple[0]),
            "max_value": target_value
        }])
        
    '''
    Chart configuration options
    '''
    pyg.config.legend_at_bottom = legend_at_bottom
    pyg.config.legend_at_bottom_columns = legend_at_bottom_columns
    pyg.config.half_pie = half_pie
    pyg.config.inner_radius = inner_rad
    pyg.config.style = colourstyle
    pyg.config.x_labels = groupby1_distinct
    pyg.config.fill = fill
    pyg.config.title = title
    pyg.config.x_label_rotation = x_label_rotation
    pyg.config.print_values = print_values
    formatter = "{:,." + str(decimal_places) + "f} " + str(value_suffix)
    pyg.config.formatter = lambda x: formatter.format(x)
    
    '''
    Return chart object
    '''
    return pyg


def pandas_to_pygal_StackedMultiLine(data,
                                     groupby1,
                                     groupby2,
                                     aggregate,
                                     absolute_values=True,
                                     colourstyle=colour_dict["DefaultStyle"],
                                     decimal_places=0,
                                     fill=False,
                                     print_values=False,
                                     horizontal=False,
                                     stacked=False,
                                     title="Test Grouped Bar Chart",
                                     value_suffix="",
                                     x_label_rotation=0,
                                     cubic=False,
                                     legend_at_bottom=False,
                                     legend_at_bottom_columns=3,
                                     agg_type="sum"):
    '''
    Create pygal object
    '''

    if stacked == True and horizontal == True:
        pyg = pygal.HorizontalStackedLine()
    elif horizontal == True and stacked == False:
        pyg = pygal.HorizontalLine()
    elif horizontal == False and stacked == True:
        pyg = pygal.StackedLine()
    else:
        pyg = pygal.Line()
        
    '''
    Transform data for pygal object
    '''
    groupby1_distinct = sorted(data[groupby1].unique())
    groupby2_distinct = sorted(data[groupby2].unique())

    dict = {}

    for name in groupby2_distinct:
        dict[name] = []

    for name in groupby2_distinct:
        for name2 in groupby1_distinct:
            subset_data = data[(data[groupby1] == name2)
                               & (data[groupby2] == name)]
            rows_in_subset_data = subset_data.shape[0]
            aggregate_value = return_aggregate_series(subset_data[aggregate],
                                                      agg_type)

            if rows_in_subset_data > 0:
                dict[name].append(aggregate_value)
            else:
                dict[name].append(None)

    if absolute_values == False:
        totals = []

        dict_values_lists = list(dict.values())
        number_of_lists = len(dict_values_lists)
        number_of_items_per_list = len(dict_values_lists[0])

        for index in range(number_of_items_per_list):
            total = 0
            for index2 in range(number_of_lists):
                current_value = dict_values_lists[index2][index]
                if current_value is not None:
                    total = total + current_value
            totals.append(total)

        percentage_dict = {}
        for key in dict.keys():
            percentage_dict[key] = []

        for key in dict.keys():
            for index in range(len(dict[key])):
                numerator = dict[key][index]
                denominator = totals[index]
                if numerator is not None and denominator is not None:
                    percentage_dict[key].append(numerator / denominator * 100)
                else:
                    percentage_dict[key].append(None)
    '''
    Add data to pygal object
    '''
    if absolute_values == True:
        for key in dict.keys():
            pyg.add(key, dict[key])
    else:
        for key in percentage_dict.keys():
            pyg.add(key, percentage_dict[key])
    
    
    '''
    Chart configuration options
    '''
    if cubic == True:
        pyg.config.interpolate = "cubic"

    pyg.config.legend_at_bottom = legend_at_bottom
    pyg.config.legend_at_bottom_columns = legend_at_bottom_columns
    pyg.config.style = colourstyle
    pyg.config.x_labels = groupby1_distinct
    pyg.config.fill = fill
    pyg.config.title = title
    pyg.config.x_label_rotation = x_label_rotation
    pyg.config.print_values = print_values
    formatter = "{:,." + str(decimal_places) + "f} " + str(value_suffix)
    pyg.config.formatter = lambda x: formatter.format(x)

    
    '''
    Return chart object
    '''
    return pyg


def pygal_to_pandas_Scatter(data,
                           x_col_name,
                           y_col_name,
                           groupby1,
                           split = False,
                           colourstyle=colour_dict["DefaultStyle"],
                           decimal_places=0,
                           print_values = False,
                           title = "Test Scatter Chart",
                           x_label_rotation = 0,
                           legend_at_bottom = False,
                           stroke = False,
                           legend_at_bottom_columns = 3,
                           dots_size = 1):
    '''
    Create pygal object
    '''
    pyg = pygal.XY()
    
    
    '''
    Transformn and add data to pygal object
    '''
    if split == False:
        
        subset = data[[x_col_name, y_col_name]]
        points_list = []
        
        for index in range(subset.shape[0]):
            x_point = round(subset.loc[index, x_col_name],decimal_places)
            y_point = round(subset.loc[index, y_col_name], decimal_places)
            coord_tuple = (x_point, y_point)
            points_list.append(coord_tuple)
        
        pyg.add("Test", points_list)
    
    else:
        
        group_names = sorted(data[groupby1].unique())
                            
        for name in group_names:
            points_list = []
            
            subset = data[[groupby1, x_col_name, y_col_name]]
            subset2 = subset.dropna(how = "any", axis = 0)
            subset3 = subset2[subset2[groupby1] == name]
            subset3 = subset3.reset_index(drop = True)

            
            for index in range(subset3.shape[0]):
                x_point = round(subset3.loc[index, x_col_name],decimal_places)
                y_point = round(subset3.loc[index, y_col_name], decimal_places)
                coord_tuple = (x_point, y_point)
                points_list.append(coord_tuple) 
            pyg.add(name, points_list)
    
    
    '''
    Chart configuration options
    '''
    pyg.config.stroke = stroke
    pyg.config.legend_at_bottom = legend_at_bottom
    pyg.config.legend_at_bottom_columns = legend_at_bottom_columns
    pyg.config.x_label_rotation = x_label_rotation
    pyg.config.print_values = print_values
    pyg.config.style = colourstyle
    pyg.config.title = title
    pyg.config.dots_size = dots_size

    '''
    Return chart object
    '''
    return pyg