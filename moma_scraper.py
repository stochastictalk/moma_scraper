# -*- utf-8 -*-
# Created: 25th October 2020
# Author: Jerome Wynne
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
    work_tag_text = [v.text for v in work_tag.find('h1').findAll('span')]
    img_url = work_tag.find(
                        'picture').findAll('source')[-1]['srcset'].split(' ')[0]
    caption_keys = [t.text for t in
                            soup.findAll('dt', {'class':'work__caption__term'})]
    caption_values = [t.text for t in
                     soup.findAll('dd', {'class':'work__caption__description'})]
    caption_dct = {caption_keys[j]:caption_values[j] for j in
                                                       range(len(caption_keys))}
    return work_tag_text, img_url, caption_dct
