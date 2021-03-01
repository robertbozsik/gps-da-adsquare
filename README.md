# Quick start

1. Clone this repository
2. Out of the cloned repository create a folder structore of the received input files
   ![folder_structure](/images/folder_structure.png)
3. Create a virtual environment (python3 -m venv <name-of-your-environment>)
4. Start the virtual environment (source <name-of-yout-environment/bin/activate>)
5. Install all the necessary modules (python -m pip install -r requirements)
6. Set the path of the affinities folder in line 103 of the [analysis.py](analysis.py) file, then run it (python3 analysis.py)
7. Run the [plot.py](plot.py) file (python3 plot.py)
8. Run the [map.ipynb](/notebooks/map.ipynb) notebook

# Visualization store visits

Visualizing the unique visits for each store id caused a huge mess on the plot as there are 186 unique store ids, for this reason, I decided to plot the trend for each store name.

# Trend of unique visits for each store made by Seaborn:

![trend_of_unique_visits](/out_data/trend_of_unique_visits.png)

Based on the sample data (smaller dataset): \
There is a significant drop in the number of unique visits on the 17th of January by Kaufland, Lexus, Burger King, Rewe, and Aldi. Almost all the shops must have been closed that day, as it was Sunday. The Chancellor announced extended lockdown, what was already expected a couple of days before. It could explain the rising trend before the 17th, the drop on the day, and the increase right after.

# Visualization of GPS data and stores

# Map of unique visits made by Folium:

![map_of_unique_visits](/images/map_of_unique_visits.png)

# Map of stores

![map_of_stores](/images/map_of_stores.png)
