# -*- utf-8 -*-
# Created: 25th October 2020
# Author: Jeorme Wynne
# Summary: functions for grabbing images from the MoMA website.

import bs4 as bs
import requests

def retrieve_item(n: int):
    ''' Gets image and metadata from https://www.moma.org/collection/works/n
    '''
    headers = {'User-Agent':'Mozilla/5.0'}
    src_url = 'https://www.moma.org/collection/works/' + str(n)
    r = requests.get(src_url, headers=headers)
    soup = bs.BeautifulSoup(r.text, 'html.parser')

    work_tag = soup.find('section', attrs={'class':'work'})
    work_short_caption_tags = tag.find('h1').findAll('span')
    soup.find('dl', {'class':'work__caption'})
    return soup
