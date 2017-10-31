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
import sys
import os
#from utils import FILE_EXTENSIONS

def scrape_links(html):
    # function to scarpe links from html response
    soup=BeautifulSoup(html,'html.parser')
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
        resp=requests.get("https://www.google.com/search", params = params)
        print(resp.url)
        page_links=scrape_links(resp.content)
        return page_links
        
    
def validate(all_link):
    valid_links=[]
    for link in all_link:
        #print(link)
        if link[:7] in "http://" or link[:8] in "https://":
            #print(link)
            valid_links.append(link)        
    if not valid_links:
        print("NO FILES FOUND")
        sys.exit(0)        
    return valid_links
    
                 
def search(search_query,engine):
    search_query=search_query
    if engine=="g":
        params={
                'q':search_query,
                }
        all_link=get_google_links(10,params)
    valid_links=validate(all_link) 
    return valid_links





def download(**args):
    count=1
    limit=args['limit']
    
    if not args['query']:
        print("MISSING ARGUMENTS")
        sys.exit(0)
        
    search_query=args['query']
    if args['website'] == "":
        search_query = "filetype:{0} {1}".format(args["file_type"], search_query)
    else:
        search_query = "site:{0} filetype:{1} {2}".format(args["website"],args["file_type"], search_query)
    
    search_query=search_query+" FREE DOWNLOAD"
    #print(search_query)
   

    if not args['directory']:
        args['directory']=args['query'].replace(' ','-')
    
    if not os.path.exists(args['directory']):
        os.makedirs(args['directory'])
    
    all_link=search(search_query,args['engine'])

    for link in all_link:
        if count==limit:
            break
        book_name=link.split('/')[-1]
        path=args['directory']+'/'+book_name
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
        with open(path,'wb') as book:
            for data in tqdm_iter:
                book.write(data)  
        count+=1         
        
    
def main():
    parser=argparse.ArgumentParser(description="A SIMPLE DOWNLODER")
    parser.add_argument("query",type=str,default=None,help='specify the query')
    parser.add_argument('-f',"--file_type",type=str,default="pdf",help='specify to describe file type')
    parser.add_argument('-w','--website',type=str,default="",help="Specify the website")
    parser.add_argument('-e','--engine',type=str,default="g",help="from which platform you want to download")
    parser.add_argument('-l','--limit',type=int,default=2,help="how many files you want to download")
    parser.add_argument('-d','--directory',type=str,default=None,help="in which directory you want to download")
    args=parser.parse_args()
    args_dict=vars(args)
    
    download(**args_dict)
        
if __name__ == "__main__":
	main()

#comment1
#comment3
    
    
    
    
    
    
    
    
    
    
    
    
                 
        
