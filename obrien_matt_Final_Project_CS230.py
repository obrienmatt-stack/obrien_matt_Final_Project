"""Author: Matty O'Brien
   Date: 4/26/2021
   This program is designed to manipulate data about used cars using Streamlit and other features to analyze the data.
   I pledge that I have completed the programming assignment independently.
I have not copied the code from a student or any source.
I have not given my code to any student.
"""


import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# to read in data and set columns


@st.cache
def read_data(filename):
    df = pd.read_csv(filename)
    df2 = df.dropna()
    lister = []

    columns = ['manufacturer', 'type', 'price', 'lat', 'long']

# to iterate through rows with pandas
    for index, row in df2.iterrows():
        sub = []
        for col in columns:
            index_no = df.columns.get_loc(col)
            sub.append(row[index_no])
        lister.append(sub)

    return lister

# filtered data


def load_data():
    filters = ['manufacturer', 'type', 'price', 'year', 'condition', 'drive', 'paint_color', 'lat', 'long']
    car_data = pd.read_csv('used_cars.csv')
    car_data = car_data.filter(filters)
    car_data = car_data.dropna()

    return car_data


car_data = load_data()
# Storing values in a list


def manufacturers_list(data):
    manufacturers = []

    for i in range(len(data)):
        if data[i][0] not in manufacturers:
            manufacturers.append(data[i][0])
            manufacturers.sort()
    return manufacturers

# Storing values in a dictionary


def freq_data(data, manufacturers, price):
    freq_dict = {}

    for manufacturer in manufacturers:
        freq = 0
        for i in range(len(data)):
            if data[i][0] == manufacturer and price >= data[i][2]:
                freq += 1
        freq_dict[manufacturer] = freq

    return freq_dict

# Visualization 1 - Bar Chart


def bar_chart(freq_dict):
    x = freq_dict.keys()
    y = freq_dict.values()

    plt.bar(x, y, color='cyan')
    plt.xticks(rotation=45)
    plt.xlabel('Manufacturer')
    plt.ylabel('Frequencies of Listings')
    title = 'Listing in: '
    for key in freq_dict.keys():        # makes title of graph fluid with manufacturers that are selected
        title += key + ', '
    plt.title(title)

    return plt

# Visual 2 - interactive map with filters


def show_map(data, manufacturers, price):
    loc = []
    for i in range(len(data)):
        if data[i][0] in manufacturers and price >= data[i][2]:
            loc.append([data[i][1], data[i][3], data[i][4]])
    map_df = pd.DataFrame(loc, columns=['type', 'lat', 'lon'])
    st.map(map_df)

# Visual 3 - Find the right car for you --> scatter? Function here


def main():
    data = read_data('used_cars.csv')
# Title to page on Streamlit
    st.title('An Analysis of Used Cars on Craigslist')
    st.subheader("Presented by Matty O'Brien")
    st.markdown('This page will manipulate large data from Craigslist, helping users to analyze the market and find the '
                'perfect used car for them!')
    # show filtered data and descriptive statistics
    st.header('\nFiltered Data for Used Cars on Craigslist')
    st.write(car_data)
    st.header('\nDescriptive Statistics for Filtered Data')
    st.write(car_data.describe())

# Sidebar with multiselect and slider
    manufacturers = st.sidebar.multiselect('Select a Manufacturer', manufacturers_list(data))
    price_lim = st.sidebar.slider('Set price limit', min_value=0, max_value=150000, value=25000, step=500)
# going to add another sidebar function here for third visual

    if len(manufacturers) > 0:
        st.write('Map of Listings by Manufacturer According to Price Limit')
        st.pyplot(bar_chart(freq_data(data, manufacturers, price_lim)))
        show_map(data, manufacturers, price_lim)


main()
