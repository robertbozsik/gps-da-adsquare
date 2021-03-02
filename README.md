# Quick start

1. Clone this repository
2. Out of the cloned repository create the following folder structore of the received input files:
   ![folder_structure](/images/folder_structure.png)
3. Create a virtual environment (python3 -m venv <name-of-your-environment>)
4. Start the virtual environment (source <name-of-yout-environment/bin/activate>)
5. Install all the necessary modules (python -m pip install -r requirements)
6. In case there is a problem by installing the module 'fiona', install 'gdal' with brew (brew install gdal)
7. Run the [analysis.py](analysis.py) file (python3 analysis.py). You should see something like this in your iTerm:
   ![analysis](/images/analysis.png)
8. Run the [plot.py](plot.py) file (python3 plot.py)
9. Run the [map.ipynb](/notebooks/map.ipynb) notebook in a Jupyter Notebook (python3 -m jupyter notebook)
10. Check the output files in the [out_data](/out_data) folder

# Visualization of unique store visits

### Dashboard of unique store visits

See the big picture on this [dasboard](https://public.tableau.com/profile/robert.bozsik#!/vizhome/unique_visits/Dashboardofuniquevisists?publish=yes)

![dashboard_of_unique_visits_tableau](/images/dashboard_of_unique_visits_tableau.png)

### Trend of unique visits for each store:

Visualizing the unique visits for each store id caused a huge mess on the plot as there are 186 unique store ids, for this reason, I decided to plot the trend for each store name.

![trend_of_unique_visits_tableau](/images/trend_of_unique_visits_tableau.png)

Based on the sample data (smaller dataset): \
There is a significant drop in the number of unique visits on the 17th of January by Kaufland, Lexus, Burger King, Rewe, and Aldi. Almost all the shops must have been closed that day, as it was Sunday. The Chancellor announced extended lockdown, what was already expected a couple of days before. It could explain the rising trend before the 17th, the drop on the day, and the increase right after.

# Visualization of GPS data and stores

### Map of unique visits:

![map_of_unique_visits_folium](/images/map_of_unique_visits_folium.png)

### Map of stores

![map_of_stores_folium](/images/map_of_stores_folium.png)

### Fake latitudes and longitudes in the data

There are some "fake" latitudes and longitudes in the data. The numbers should be in decimal degrees format and range from -90 to 90 for latitude and -180 to 180 for longitude. The data should be cleaned in advance.

![map_anomaly_tableau](/images/map_anomaly_tableau.png)
