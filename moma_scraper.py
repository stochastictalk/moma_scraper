# -*- utf-8 -*-
# Created: 25th October 2020
# Author: Jerome Wynne
# Summary: functions for grabbing images from the MoMA website.

import bs4 as bs
import requests
from os import mkdir
from shutil import rmtree
import json

def retrieve_item(n: int):
    ''' Gets image and metadata from https://www.moma.org/collection/works/n.

        Args:
            n: item number (at end of URL).

        Returns:
            dict: dictionary of metadata.
            str: complete URL of highest-res image available for item.
    '''
    # retrieve the webpage
    headers = {'User-Agent':'Mozilla/5.0'}
    src_url = 'https://www.moma.org/collection/works/' + str(n)
    r = requests.get(src_url, headers=headers)

    if r.status_code == 404:
        pass
    else:
        # parse into soup
        soup = bs.BeautifulSoup(r.text, 'html.parser')

        # get metadata from header
        work_tag = soup.find('section', attrs={'class':'work'})
        meta_work_v = [v.text for v in work_tag.find('h1').findAll('span')]
        meta_work_k = ['Artist', 'Work', 'Year']
        meta_work_dct = {k:v for k, v in zip(meta_work_k, meta_work_v)}

        # get image url
        img_url = work_tag.find(
                    'picture').findAll('source')[-1]['srcset'].split(' ')[0]
        img_url = 'https://www.moma.org' + img_url

        # get metadata from caption
        meta_caption_k = [t.text for t in
                            soup.findAll('dt', {'class':'work__caption__term'})]
        meta_caption_v = [t.text for t in
                            soup.findAll('dd',
                                        {'class':'work__caption__description'})]
        meta_caption_dct = {k:v for k, v in
                                zip(meta_caption_k, meta_caption_v)}

        # merge metadata dictionaries
        meta_dct = {**meta_work_dct, **meta_caption_dct}

        # clean metadata entries
        def clean(s:str): return(s.replace('/n', '').strip())
        meta_dct = {clean(k): clean(v) for k, v in meta_dct.items()}

        # include n and URL in metadata
        meta_dct['id'] = n
        meta_dct['url'] = img_url

        return meta_dct, img_url

def download_to_disk(n_start: int, n_end: int, dst_fp: str):
    ''' Writes images and metadata for the first N items in the online
        MoMA catalogue to disk. Metadata is written as JSON.
    '''

    dst_fp = './data/' + dst_fp

    for n in range(n_start, n_end+1):

        try:
            meta_dct, img_url = retrieve_item(n)
            json_str = json.dumps(meta_dct)
        except TypeError: # fails to unpack objects
            continue # skip this item

        with open(dst_fp, 'a', encoding='utf8') as file:
            file.write(json_str + ',')

download_to_disk(1, 5, 'test.json')
