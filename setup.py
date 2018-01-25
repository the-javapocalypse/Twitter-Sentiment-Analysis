from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Twitter Sentiment Analysis',
    version='1.3.0',

    description='This script can tell you the sentiments of people regarding to any events happening in the world by analyzing tweets related to that event. It will search for tweets about any topic and analyze each tweet to see how positive or negative it's emotion is.',
    long_description=long_description,


    url='https://github.com/the-javapocalypse/Twitter-Sentiment-Analysis',


    author='Muhammad Ali Zia',
    author_email='muhammad.17ali@gmail.com',


    classifiers=[

        'Development Status :: 4 - Beta',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],


    keywords='python twitter sentiment-analysis textblob nlp tweepy nltk',


    install_requires=['tweepy','textblob','matplotlib'],

   
)
