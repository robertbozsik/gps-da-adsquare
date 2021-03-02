# Quick start

1. Clone this repository
2. Out of the cloned repository create the following folder structore of the received input files (don't forget to upzip all files/folders):
   ![folder_structure](/images/folder_structure.png)
3. Create a virtual environment (python3 -m venv <name-of-your-environment>)
4. Start the virtual environment (source <name-of-yout-environment/bin/activate>)
5. Install all the necessary modules (python -m pip install -r requirements)
6. Run the [analysis.py](analysis.py) file (python3 analysis.py). You should see something like this in your iTerm:
   ![analysis](/images/analysis.png)
7. Run the [plot.py](plot.py) file (python3 plot.py)
8. Run the [map.ipynb](/notebooks/map.ipynb) notebook in a Jupyter Notebook
9. Check the output files in the [out_data](/out_data) folder

# Visualization of store visits

Visualizing the unique visits for each store id caused a huge mess on the plot as there are 186 unique store ids, for this reason, I decided to plot the trend for each store name.

### Trend of unique visits for each store made by Seaborn:

![trend_of_unique_visits](/out_data/trend_of_unique_visits.png)

Based on the sample data (smaller dataset): \
There is a significant drop in the number of unique visits on the 17th of January by Kaufland, Lexus, Burger King, Rewe, and Aldi. Almost all the shops must have been closed that day, as it was Sunday. The Chancellor announced extended lockdown, what was already expected a couple of days before. It could explain the rising trend before the 17th, the drop on the day, and the increase right after.

# Visualization of GPS data and stores

### Map of unique visits made by Folium:

![map_of_unique_visits](/images/map_of_unique_visits.png)

### Map of stores

![map_of_stores](/images/map_of_stores.png)
