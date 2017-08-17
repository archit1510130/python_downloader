#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 18:17:49 2017

@author: andha_coder
"""

from selenium import webdriver
import requests
from bs4 import BeautifulSoup



def scrape_links(html):
    # function to scarpe links from html response
    soup=BeautifulSoup(html,'lxml')
    links=[]
    results=soup.findAll('h3',{'class':'r'})
    for result in results:
        link=result.a['href'][7:].split('&')[0]
        links.append(link)



def get_google_links(limit,params):
    # function to fetch links equal to the limit
    links=[]
    for start_index in range(0,limit,10):
        params['start']=start_index
        print(start_index)
        resp=requests.get("https://www.google.com/search", params = params)
        #print(resp.url)
        page_links=scrape_links(resp.content)
        

                 
def search():
    user_input=input()
    search_query=user_input
    params={
            'q':search_query,
            }
    get_google_links(10,params)    
    
search()    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
                 
        