import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

# Read the updated data from CSV
df = pd.read_csv('./assets/expense.csv')

# Reshape the data for plotting
df_melted = df.melt(id_vars=["Category"], 
                    value_vars=df.columns[1:], 
                    var_name="Month", 
                    value_name="Expense")

app.layout = html.Div([
    html.H1("Expense's Dashboard"),
    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': category, 'value': category} for category in df['Category']],
        value='Food'
    ),
    html.Div(id='average-display'),
    dcc.Graph(id='bar-graph'),
    dcc.Graph(id='pie-chart'),
    dcc.Graph(id='line-graph'),
    dcc.Graph(id='scatter-plot')
])

@app.callback(
    [Output('bar-graph', 'figure'),
     Output('pie-chart', 'figure'),
     Output('line-graph', 'figure'),
     Output('scatter-plot', 'figure'),
     Output('average-display', 'children')],
    [Input('category-dropdown', 'value')]
)
def update_graph(selected_category):
    filtered_df = df_melted[df_melted['Category'] == selected_category]
    
    category_sum = filtered_df['Expense'].sum()
    category_avg = filtered_df['Expense'].mean()
    
    overall_sum = df_melted['Expense'].sum()
    overall_avg = df_melted['Expense'].mean()

    color_list = px.colors.qualitative.Set3  
    
    # Bar chart
    bar_fig = px.bar(filtered_df, 
                     x='Month', 
                     y='Expense', 
                     title=f'{selected_category} Expenses Over Time',
                     color='Month',  
                     color_discrete_sequence=color_list)
    
    # Pie chart for category breakdown (total expenses by category)
    pie_fig = px.pie(df, 
                     names='Category', 
                     values=df.iloc[:, 1:].sum(axis=1),
                     title="Total Expenses by Category")

    # Line graph for trend analysis (expenses over time)
    line_fig = px.line(filtered_df, 
                       x='Month', 
                       y='Expense', 
                       title=f'{selected_category} Expenses Trend',
                       markers=True)

    # Scatter plot for correlation between months (e.g., correlation between January and February expenses)
    scatter_fig = px.scatter(df_melted, 
                             x='Month', 
                             y='Expense', 
                             color='Category', 
                             title='Correlation of Expenses by Month')

    avg_display = html.Div([
        html.H3(f"Total Expenses for {selected_category}: ${category_sum:,.2f}"),
        html.H3(f"Average Monthly Expense for {selected_category}: ${category_avg:,.2f}"),
        html.Hr(),
        html.H3(f"Overall Total Expenses: ${overall_sum:,.2f}"),
        html.H3(f"Overall Average Monthly Expense: ${overall_avg:,.2f}")
    ])
    
    return bar_fig, pie_fig, line_fig, scatter_fig, avg_display
server = app.server
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
