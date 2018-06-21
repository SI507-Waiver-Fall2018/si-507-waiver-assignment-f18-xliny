# Imports -- you may add others but do not need to
import plotly.plotly as py
import plotly.graph_objs as go

# Code here should involve creation of the bar chart as specified in instructions
# And opening / using the CSV file you created earlier with noun data from tweets

def data_preparation():
	file = open('noun_data.csv', "r", encoding = 'utf-8')
	words = []
	counts = []
	for line in file.readlines()[1:]:
		words.append(line[:-1].split(',')[0])
		counts.append(int(line[:-1].split(',')[1]))
	file.close()
	return words, counts


def plotting(words, counts):
	data = [go.Bar(
            x=words,
            y=counts
    )]

	plotly.offline.plot({'data': data, 
              'layout': {'title': 'Most frequent nouns from UMSI tweets', 
                         'font': dict(family='Comic Sans MS', size=16)}},
             auto_open=True, image = 'png', image_filename='part4_viz_image',
             image_width=800, image_height=600)

if __name__=="__main__":
	words, counts = data_preparation()
	plotting(words, counts)
