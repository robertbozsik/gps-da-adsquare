# Quick start

1. Clone this repository
2. Out of the cloned repository create the following folder structore of the received input files:
   ![folder_structure](/images/folder_structure.png)
3. Create a virtual environment (python3 -m venv name-of-your-environment)
4. Start the virtual environment (source name-of-your-environment/bin/activate)
5. Install all the necessary modules (python -m pip install -r requirements)
6. In case there is a problem by installing the module 'fiona', install 'gdal' with brew (brew install gdal)
7. Run the [analysis.py](analysis.py) file (python3 analysis.py). You should see something like this in your iTerm:
   ![analysis](/images/analysis.png)
8. Run the [plot.py](plot.py) file by adding the following parameters to your command:
   - plot_all_stores (e.g. python3 plot.py plot_all_stores)
   - plot_a_store + storename (e.g. python3 plot.py plot_a_store Aldi)
9. Run the [map.ipynb](/notebooks/map.ipynb) notebook in a Jupyter Notebook (python3 -m jupyter notebook)
10. Check the output files in the [out_data](/out_data) folder

# Visualization of unique store visits

### Dashboard of unique store visits

See the big picture on this <a href="https://public.tableau.com/profile/robert.bozsik#!/vizhome/visits_dashboard_tableau/Dashboard1?publish=yes" target="_blank">dashboard</a>.

![visits_dashboard_tableau](/images/visits_dashboard_tableau.png)

### Trend of unique visits by store:

Visualizing the unique visits for each store id caused a huge mess on the plot as there are 186 unique store ids, for this reason, I decided to plot the trend for each store name.

![trend_of_unique_visits_tableau](/images/trend_of_unique_visits_tableau.png)

Based on the sample data (smaller dataset): \
There is a significant drop in the number of unique visits on the 17th of January by Kaufland, Rewe, and Aldi. All grocery sotres must have been closed that day, as it was Sunday. There were, however, no such huge drops by Kaufland one and two weaks before.

### Unique visits of a store:

![unique_visits_of_a_store_tableau](/images/unique_visits_of_a_store_tableau.png)

# Visualization of GPS data and stores

### Map of a store:

![map_of_a_store](/images/map_of_a_store.png)

### Map of a user in store:

![map_of_a_user_in_store](/images/map_of_a_user_in_store.png)

### Map of stores and users in store:

![map_of_stores_and_users_in_store](/images/map_of_stores_and_users_in_store.png)
