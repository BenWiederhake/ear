#!/usr/bin/env python3

# bs4==4.5.3
# html5lib==1.0.1
# requests==2.12.4

import bs4
import json
import requests
import time  # sleep
import urllib.parse


CRAWL_CONTACT_MAIL = 'i-am-an-idiot-for-not-filling-this-in-sorry'
CRAWL_PARSER = 'html5lib'
CRAWL_USERAGENT = 'python-requests/{} ear-collect-langs/0.0.1 (contact={})'.format(
    requests.__version__, CRAWL_CONTACT_MAIL
)
CRAWL_WAIT_SECONDS = 5


def get_bs(url):
    time.sleep(CRAWL_WAIT_SECONDS)
    # I already checked robots.txt by hand, so don't do it here.
    response = requests.get(url, headers={'user-agent': CRAWL_USERAGENT})
    assert response.status_code == 200, (url, response.status_code)
    soup = bs4.BeautifulSoup(response.content, CRAWL_PARSER)
    # Make all hrefs absolute
    for a in soup.find_all('a'):
        if a.has_attr('href'):
            a['href'] = urllib.parse.urljoin(url, a['href'])
    return soup

# All 'collect_from_DOMAIN' functions must return a:
# dict
#   key: language (ASCII English name, ISO code, or unicode native name)
#   value: list of words (unicode)
# where the lists of words should all have the same or at least similar length.


def collect_from_1000mostcommonwords_com():
    print('Beginning to crawl 1000mostcommonwords.com ...')
    # Their https is broken :-(
    homepage = get_bs('http://1000mostcommonwords.com/')
    homepage_content = homepage.find('div', class_='entry-content')
    result = dict()
    broken_urls = {
        'http://1000mostcommonwords.com/1000-most-common-luxembourgish-words',
        'http://1000mostcommonwords.com/1000-most-common-samoan-words',
        'http://1000mostcommonwords.com/1000-most-common-scots-gaelic-words',
        'http://1000mostcommonwords.com/1000-most-common-shona-words',
        'http://1000mostcommonwords.com/1000-most-common-sindhi-words',
        'http://1000mostcommonwords.com/1000-most-common-xhosa-words',
    }
    for langpage_a in homepage_content.find_all('a'):
        lang_key = langpage_a.text
        lang_value = []
        langpage_url = langpage_a['href']
        if langpage_url == 'http://1000mostcommonwords.com/%20http:/www.1000mostcommonwords.com/words/1000-most-common-ukrainian-words':
            # Seriously?!
            langpage_url = 'http://1000mostcommonwords.com/1000-most-common-ukrainian-words/'
        elif langpage_url in broken_urls:
            # That one is broken.  Sigh.
            continue
        print('    Subpage ' + langpage_url + ' ...')
        langpage = get_bs(langpage_url)
        langpage_content = langpage.find('div', class_='entry-content')
        langpage_table = langpage_content.find('table')
        look_at_col = 1 if langpage_url != 'http://1000mostcommonwords.com/1000-common-english-words' else 2
        for word_row in langpage_table.find_all('tr')[1:]:
            word_row_tds = word_row.find_all('td')
            assert len(word_row_tds) == 3, (langpage_url, word_row)
            word = word_row_tds[look_at_col].text.strip()
            if len(word) > 0:
                lang_value.append(word)
            else:
                print('    WARNING: dropping word', word_row)
        assert 990 < len(lang_value) <= 1000
        result[lang_key] = lang_value
    print('    Site complete.')
    return result


def run(source_fn=collect_from_1000mostcommonwords_com):
    collected = source_fn()
    with open('collected.json', 'w') as fp:
        json.dump(collected, fp)


if __name__ == '__main__':
    run()
