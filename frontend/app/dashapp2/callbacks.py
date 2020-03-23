from dash.dependencies import Input
from dash.dependencies import Output
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

def register_callbacks(dashapp):
	@dashapp.callback(
		Output('graph-with-slider', 'figure'),
		[Input('year-slider', 'value')])
	def update_figure(selected_year):
		filtered_df = df[df.year == selected_year]
		traces = []
		for i in filtered_df.continent.unique():
			df_by_continent = filtered_df[filtered_df['continent'] == i]
			traces.append(dict(
				x=df_by_continent['gdpPercap'],
				y=df_by_continent['lifeExp'],
				text=df_by_continent['country'],
				mode='markers',
				opacity=0.7,
				marker={
					'size': 15,
					'line': {'width': 0.5, 'color': 'white'}
				},
				name=i
			))

		return {
			'data': traces,
			'layout': dict(
				xaxis={'type': 'log', 'title': 'GDP Per Capita',
					   'range':[2.3, 4.8]},
				yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
				margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
				legend={'x': 0, 'y': 1},
				hovermode='closest',
				transition = {'duration': 500},
			)
		}