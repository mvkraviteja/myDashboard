#!/usr/bin/env python3.7

"""
####################################################################################################################################################################
Application : dashBoard
Description : Simple dashboard to play around with word clouds from data extracted from NYT articles
Author      : RaviTeja Manda
Date        : 03/30/2020
####################################################################################################################################################################
"""

"""
__author__ = "RaviTeja Manda"
"""

import os
import sys
import argparse
import time
import numpy
import pandas
import matplotlib
from wordcloud import WordCloud
import csv
import nltk
from nltk.corpus import stopwords 

import dash
import dash_bootstrap_components
import dash_core_components
import dash_html_components
from dash.dependencies import Input, Output
import dash_table

#DATA_PATH='/home/raviteja/Projects/quarantine/scrapper/reddit_scrapper.csv'
#DATA_PATH='/home/raviteja/Projects/quarantine/scrapper/data/reddit/posts/reddit_scrapper_posts_20200330-034806.csv'
DATA_PATH='/home/raviteja/Projects/quarantine/scrapper/data/nyt/search/2020-03-30.csv'
STOPWORDS='Comments'

class dashBoard:
    def __init__(self, args, standalone=False):
        print(" START : Initializing dashBoard ...\n")
        #print(sys.executable)
        if(standalone == True):
            print(" \tSTANDALONE : I will be doing what I am supposed to do ... \n")
            if(args.data_local):
                print(" \tData can be read locally")
                self.data_local = True
            else:
                print(" \tNeed to access Data from a remote location\n")
                self.data_local = False
            if(args.data_path):
                self.data_path = args.data_path
            else:
                print(" \tNeed access to Data to continue work \n")
                print(" \tChecking default location (%s) for now ...\n" %DATA_PATH)
                self.data_path = DATA_PATH
        else:
            print(" \tINVOKED as an object : Doing what I am told to do ...\n")
        print(" DONE : Initializing dashBoard ...\n")

    def printWordCloud(self):
        stopwords = set(STOPWORDS)
        stopwords.update(["Daily", "Discussion", "Top", "comments", "going", "to", "see"])
        #wordcloud = WordCloud(max_font_size=50,max_words=100, background_color="white").generate(text)
        wordcloud = WordCloud(max_font_size=50, stopwords=stopwords, background_color="white").generate(text)
        matplotlib.pyplot.imshow(wordcloud, interpolation='bilinear')
        matplotlib.pyplot.axis("off")
        imageName = 'data/wordcloud/reddit_scrapper_' + (time.strftime("%Y%m%d-%H%M%S")) + '.png' 
        wordcloud.to_file(imageName)
        matplotlib.pyplot.show()


    def readData(self):
        print(" \tNeed to read Data in to the app here \n")
        fileName = self.data_path
        dataFrame = pandas.read_csv(fileName)
        #print(dataFrame.columns)
        #print(dataFrame.head())
        #print(dataFrame.count(axis=0))
        #print(dataFrame.count(axis=1))
        print(dataFrame.shape)
        #print(dataFrame.iloc[5][1])
        #print(dataFrame.tail())
        #print(dataFrame.dtypes)
        #transpose_dataFrame = dataFrame.T
        #print(dataFrame.shape)
        #print(dataFrame.head)
        #print("\n")
        #data_by_type = dataFrame.groupby("worldnews")
        #print(data_by_type.describe().head())

    def readCSVData(self):
        fileName = self.data_path
        self.dataFrame = pandas.read_csv(fileName)
        print(self.dataFrame.head)
        print(self.dataFrame.shape)
        print(self.dataFrame.columns)
        #dateGroup = self.dataFrame.groupby('date')
        #dateGroup.first()
        #keywordsGroup = self.dataFrame.groupby('keywords')
        #print(keywordsGroup.first())
        #print(type(keywordsGroup))
        headlinesFrame = pandas.DataFrame()
        headlinesFrame = self.dataFrame[['headline', 'date']]
        #print(headlinesFrame.head)
        #print(headlinesFrame.iloc[0])
        headlinesFrame['date'] = headlinesFrame['date'].str.replace('2020-03-30T', '')
        headlinesFrame['date'] = headlinesFrame['date'].str.replace('0000', '')
        headlinesFrame['date'] = headlinesFrame['date'].str.replace('+', '')
        #print(headlinesFrame.iloc[0])
        #pd.to_datetime(headlinesFrame['date'], format="%H:%M:%S.%f").sort_values()
        headlinesFrame['date'] = pandas.to_datetime(headlinesFrame['date'])
        #print(headlinesFrame.head)
        headlinesFrame = headlinesFrame.sort_values(by='date')
        print(headlinesFrame.head)        
        self.headlinesFrame = headlinesFrame

    def initDashboard(self):
        print(" \tDoing necessary logic to initialise Dash and building a dashboard ...\n")
        #external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        self.app = dash.Dash(__name__, external_stylesheets = [dash_bootstrap_components.themes.BOOTSTRAP])
        self.server = self.app.server
        self.app.config.suppress_callback_exceptions = True
        #set the app.layout
        self.app.layout = dash_html_components.Div([
            dash_core_components.Input(id='my-id', value = 'initial value', type = 'text'), dash_html_components.Div(id='my-div'),
            dash_core_components.Tabs(id="tabs", value='tab-1', children=[
            dash_core_components.Tab(label='Tab one', value='tab-1'),
            dash_core_components.Tab(label='Tab two', value='tab-2'),
            ]),
            dash_html_components.Div(id='tabs-content')
        ])
        '''
        #callback to control the tab content
        @self.app.callback(Output('tabs-content', 'children'),
                      [Input('tabs', 'value')])
        def render_content(tab):
            if tab == 'tab-1':
                return dash_html_components.H1('Tab 1')
            elif tab == 'tab-2':
                return dash_html_components.H1('Tab 2')
        '''

    def buildStoryData(self):
        print(" \tBuilding story content\n")

    def buildwordCloudData(self):
        print(" \tBuilding wordCloud content\n")


    def buildDataForDashboard(self):
        print(" \tBuilding Dashboard data ...\n")
        self.buildStoryData()
        self.buildwordCloudData()
        @self.app.callback(Output('tabs-content', 'children'),
                      [Input('tabs', 'value')])
        def render_content(tab):
            if tab == 'tab-1':
                return dash_html_components.H1('Storyboard of all headlines against time')
            elif tab == 'tab-2':
                return dash_html_components.H1('Wordcloud of all headlines for the day')
        def update_output_div(input_value):
            return 'You\'ve entered "{}"'.format(input_value)


    def startDashboard(self):
        print(" \tStarting Dashboard data ...\n")
        self.app.run_server()


    def dumpData(self):
        print(" \tDoing necessary logic here for dumping data ... (can later write to a pdf or something)\n")

    def run(self):
        print(" Starting extraction of data from reddit server ...\n")
        #self.readData()
        self.readCSVData()
        self.initDashboard()
        self.buildDataForDashboard()
        self.startDashboard()
        self.dumpData()
        print(" Done with extracting and dumping it in to a database\n")

def get_args():
    """ Arguments Parsing """
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument(
    '-local?',
    dest='data_local',
    required=False,
    type=bool,
    action='store',
    help='Are Data stored locally or remotely'
    )
    parser.add_argument(
    '-data-path',
    dest='data_path',
    required=False,
    type=str,
    action='store',
    help='Location to access Data'
    )
    args = parser.parse_args()
    return args

"""
####################################################################################################################################################################
START : Main Function
####################################################################################################################################################################
"""
if __name__ == "__main__":
    print(" I generate word clouds ... \n")
    arguments_passed = get_args()
    myWordCloud = dashBoard(arguments_passed, True)
    start_time = time.time()
    myWordCloud.run()
    print(" Done generating the dashBoard \n")

else:
    print(" I am being asked by (###) to do work \n")
"""
####################################################################################################################################################################
END : Main Function
####################################################################################################################################################################
"""
