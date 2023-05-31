#Import the required dependency
import pandas as pd

#Define path to HTML file
html_path = 'history.html'
#Read tables from HTML file
tables = pd.read_html(html_path)

#Print tables separated by empty rows
for table in tables:
    print(table, '\n\n')
