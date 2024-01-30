import requests
import bs4
import ptt_topic_modeling.utils as utils
from tqdm import tqdm
from typing import Tuple, List


def links_to_posts(links: list) -> List[str]:
    '''
    Crawl posts from the given list of URLs.

    Parameters
    ----------
    links : list
        list of link to PTT pages

    Returns
    -------
    list
        list of content (comments are included by default)
    '''
    posts = []
    for link in tqdm(links.values()):
        text = crawl_post(link)[0]
        if text is None:
            print(f'fail to crawl the following page: {link}')
            posts.append('')
            continue
        text = utils.remove_html(text)
        text = utils.full_to_half(text)
        text = utils.strip_punctuation(text)
        text = utils.strip_multi_spaces(text)
        posts.append(text)
    return posts


def crawl_links(board_name: str, target_num: int = 1000) -> dict:
    '''
    Given a specific board on PTT (e.x. Boy-Girl),
    crawl the links to the individual posts.
    Number of links is determined by target_num.

    Parameters
    ----------
    board_name : str

    target_num : int
        a minimum of 100 is recommended

    Returns
    dict
        {title: content}
    -------
    '''
    if target_num <= 0:
        raise ValueError("target_num must be non-negative integer")

    links = {}
    while len(links) < target_num:
        if (len(links)) == 0:
            next, sublist = crawl_page(
                f"https://www.ptt.cc/bbs/{board_name}/index.html")
        else:
            next, sublist = crawl_page(next)
        if len(sublist) < target_num - len(links):
            links.update(sublist)
        else:
            links.update(list(sublist.items())[:target_num-len(links)])

    return links


def crawl_page(link: str) -> Tuple[str, dict]:
    '''
    Crawl individual links to post from the main pages.

    Parameters
    ----------
    link : str
        link to the main pages.
        E.x. https://www.ptt.cc/bbs/Gossiping/index.html

    Returns
    -------
    str
        the link to the previous page listing.
        This is used to crawl the next set of posts.
    dict
        {title: content}
    '''
    resp = send_request(link)
    resp.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(resp.text, features="html.parser")
    title_links = {}
    for post in soup.find_all('div', class_='title'):
        try:
            title_links[post.a.text] = "https://www.ptt.cc/" + \
                post.a['href']  # 若文章被刪除會沒有連結
        except TypeError:
            pass
    if soup.find('a', class_="btn wide", string="‹ 上頁") is None:
        raise TypeError("Can't find next page.")
    next_page = "https://www.ptt.cc/" + \
        soup.find('a', class_="btn wide", string="‹ 上頁")['href']
    return next_page, title_links


def crawl_post(link: str, combine_text: bool = True) -> List[str]:
    '''

    Parameters
    ----------
    link : str
        link to a single PTT post
    combine_text : bool
        Whether to combine comment into main text
        or output it seperately

    Returns
    -------
    list
        single item [content] if combine_text=True,
        two items [main_content.text, comment_text] if False
    '''
    resp = send_request(link)

    resp.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(resp.text, features="html.parser")
    main_content = soup.find('div', id="main-content")
    while True:
        temp = main_content.find('div', class_="article-metaline")
        if temp is None:
            break
        temp.extract()
    while True:
        temp = main_content.find('div', class_="article-metaline-right")
        if temp is None:
            break
        temp.extract()
    while True:
        temp = main_content.find('span', class_="f2")
        if temp is None:
            break
        temp.extract()
    comment_text = []
    for comment in main_content.find_all('div', class_='push'):
        comment_text.append(comment.find('span',
                            class_="f3 push-content").text[1:])
        main_content.find('div', class_='push').extract()
    if combine_text is True:
        result = main_content.text
        for text in comment_text:
            result += text
        return [result]
    else:
        return [main_content.text, comment_text]


def send_request(link: str) -> requests.models.Response:
    '''

    Parameters
    ----------
    link : str
        Any link to ptt.cc

    Returns
    -------
    requests.models.Response
    '''
    if 'https://www.ptt.cc/' not in link:
        raise ValueError(f'{link} does not belong to PTT')
    try:
        resp = requests.get(link, cookies={'over18': '1'})
    except ConnectionError:
        raise ConnectionError('No wifi')
    # add response check
    if resp.status_code != 200:
        print(f"Connection error, error code {resp.status_code}")
        raise ConnectionError('webpage not available')
    return resp
