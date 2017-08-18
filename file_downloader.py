#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 18:17:49 2017

@author: andha_coder
"""

from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
chunk_size=512
import argparse

def scrape_links(html):
    # function to scarpe links from html response
    soup=BeautifulSoup(html,'lxml')
    links=[]
    results=soup.findAll('h3',{'class':'r'})
    for result in results:
        link=result.a['href'][7:].split('&')[0]
        links.append(link)
    return links    



def get_google_links(limit,params):
    # function to fetch links equal to the limit
    for start_index in range(0,limit,10):
        params['start']=start_index
        print(start_index)
        resp=requests.get("https://www.google.com/search", params = params)
        #print(resp.url)
        page_links=scrape_links(resp.content)
        return page_links
        
                 
def search(user_input):
    search_query=user_input
    params={
            'q':search_query,
            }
    all_link=get_google_links(10,params)
    return all_link

def download(**args):
    count=1
    user_input=args['query']
    user_input=user_input+args['file_type']+"free download"
    all_link=search(user_input)
    for link in all_link:
        if count==4:
            break
        book_name=link.split('/')[-1]
        print(book_name)
        resp=requests.get(link,stream=True)
        if not resp.status_code==200:
            return
        try:
            total_size=int(resp.headers['content-length'])
        except KeyError:
            total_size=len(resp.content)
            
        #print(total_size)
        total_chunks=total_size/chunk_size
        file_iterable = resp.iter_content(chunk_size=chunk_size)
        tqdm_iter = tqdm(iterable = file_iterable,total=total_chunks,position=0,desc=book_name,
            unit = 'KB')
        with open("/Users/andha_coder/Python/python_downloader/book_name",'wb') as book:
            for data in tqdm_iter:
                book.write(data)  
        count+=1         
        
    
def main():
    parser=argparse.ArgumentParser(description="A SIMPLE DOWNLODER")
    parser.add_argument("query",type=str,default=None,help='specify the query')
    parser.add_argument('-f',"--file_type",type=str,default="pdf",help='specify to describe file type')
    args=parser.parse_args()
    args_dict=vars(args)
    download(**args_dict)
        
if __name__ == "__main__":
	main()   


    
    
    
    
    
    
    
    
    
    
    
    
                 
        