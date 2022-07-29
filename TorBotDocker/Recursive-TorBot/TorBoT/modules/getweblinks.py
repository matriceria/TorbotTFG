#encoding = utf8
import re
import requests
import tldextract

from modules import pagereader
from bs4 import BeautifulSoup
from modules.bcolors import Bcolors
from requests.exceptions import ConnectionError, HTTPError


def valid_url(url, extensions=False):
    """Checks for any valid url using regular expression matching

        Matches all possible url patterns with the url that is passed and
        returns True if it is a url and returns False if it is not.

        Args:
            url: string representing url to be checked

        Returns:
            bool: True if valid url format and False if not
    """
    pattern = r"^https?:\/\/(www\.)?([a-z,A-Z,0-9]*)\.([a-z, A-Z]+)(.*)"
    regex = re.compile(pattern)
    if not extensions:
        if regex.match(url) and not re.findall(r'.onion', url):
            return True
        return False

    parts = tldextract.extract(url)
    valid_sites = list()
    for ext in extensions:
        if regex.match(url) and '.'+parts.suffix in ext:
            valid_sites.append(url)
    return valid_sites


def valid_onion_url(url):
    """Checks for valid onion url using regular expression matching

        Only matches onion urls

        Args:
            url: string representing url to be checked

        Returns:
            bool: True if valid onion url format, False if not
    """
    pattern = r"^https?:\/\/(www\.)?([a-z,A-Z,0-9]*)\.onion/(.*)"
    regex = re.compile(pattern)
    if regex.match(url):
        return True
    return False


def is_link_alive(link):
    """Generator that yields links as they come

        Uses head request because it uses less bandwith than get and timeout is
        set to 10 seconds and then link is automatically declared as dead.

        Args:
            link: link to be tested
            colors: object containing colors for link

        Yields:
            string: link with either no color or red which indicates failure
    """

    try:
        resp = requests.head(link, timeout=10)
        resp.raise_for_status()
        return True
    except (ConnectionError, HTTPError):
        return False


def add_green(link):
    colors = Bcolors()
    return '\t'+ colors.OKGREEN + link + colors.ENDC


def add_red(link):
    colors = Bcolors()
    return '\t' + colors.On_Red + link + colors.ENDC


def get_links(soup, ext=False, live=False, printout=True):
    """
        Searches through all <a ref> (hyperlinks) tags and stores them in a
        list then validates if the url is formatted correctly.

        Args:
            soup: BeautifulSoup instance currently being used.

        Returns:
            websites: List of websites that were found
    """
    b_colors = Bcolors()
    if isinstance(soup, BeautifulSoup):
        websites = []
        onion_websites = []
        clear_websites = []

        links = soup.find_all('a')
        for ref in links:
            url = ref.get('href')
            if ext:
                if url and valid_url(url, ext):
                    clear_websites.append(url)
            else:
                if url and valid_onion_url(url):
                    onion_websites.append(url)

        """Pretty print output as below"""
        if printout:
            print(''.join((b_colors.OKGREEN,
                  'Websites Found - ', b_colors.ENDC, str(len(clear_websites) + len(onion_websites)))))
            print('------------------------------------')

            for link in (clear_websites + onion_websites):
                if is_link_alive(link):
                    coloredlink = add_green(link)
                    page = pagereader.read_page(link)
                    if page is not None and page.title is not None:
                        print_row(coloredlink, page.title.string)
                else:
                    coloredlink = add_red(link)
                    print_row(coloredlink, "Not found")

        return (onion_websites, clear_websites)


    else:
        raise(Exception('Method parameter is not of instance BeautifulSoup'))

def get_links_recursive(soup, rec_links, ext=False, live=False, printout=True):
    """
        Searches through all <a ref> (hyperlinks) tags and stores them in a
        list then validates if the url is formatted correctly.

        Args:
            soup: BeautifulSoup instance currently being used.
            rec_links: Number of onion links that should be crawled.

        Returns:
            websites: List of websites that were found
    """
    seed_websites = []
    number_of_seeds = rec_links
    b_colors = Bcolors()
    onion_websites, clear_websites = get_links(soup, False, False, False)

    """For a given number of seeds, crawls the links further, only live links are picked"""
    i = 0
    while (number_of_seeds >= 0 and i < len(onion_websites)):
        seed = onion_websites[i]
        i += 1
        if is_link_alive(seed):
            seed_websites.append(seed)
            number_of_seeds -= 1

    crawled_onion_links, crawled_clear_links = get_crawled_links(seed_websites)
    onion_websites_merged = onion_websites + crawled_onion_links
    clear_websites_merged = clear_websites + crawled_clear_links

    """Pretty print output as below"""
    if printout:
        print(''.join((b_colors.OKGREEN,
              'Onion Websites Found - ', b_colors.ENDC, str(len(onion_websites_merged)))))
        print('------------------------------------')

        for link in onion_websites_merged:
            if is_link_alive(link):
                coloredlink = add_green(link)
                page = pagereader.read_page(link)
                if page is not None and page.title is not None:
                    print_row(coloredlink, page.title.string)
            else:
                coloredlink = add_red(link)
                print_row(coloredlink, "Not found")

        print(''.join((b_colors.OKGREEN,
              'Clear Websites Found - ', b_colors.ENDC, str(len(clear_websites_merged)))))
        print('------------------------------------')

        for link in clear_websites_merged:
            if is_link_alive(link):
                coloredlink = add_green(link)
                page = pagereader.read_page(link)
                if page is not None and page.title is not None:
                    print_row(coloredlink, page.title.string)
            else:
                coloredlink = add_red(link)
                print_row(coloredlink, "Not found")
    keyword_link=[]
    """
    links = soup.get_text()
    links=links.lower()
    print(links)
    x = re.search("gas", links)
    if x!= None:
        print("keyword encontrada")
        keyword_link = keyword_link+onion_websites_merged
    """
    for link in onion_websites_merged:
        if is_link_alive(link):
            page=pagereader.read_page(link) 
            text=page.get_text()
            text= text.lower()
            
            x=re.search(".*spyware.*",text)
            if x!= None:
                #print("keyword encontrada")
                keyword_link.append(link)

    return (onion_websites_merged, clear_websites_merged, keyword_link)



def get_crawled_links(seed_websites):
    """ Takes a list of seed links and crawls them.

            Args:
                seed_websites : list of seed_websites.

            Returns:
                websites: List of onion links and clear links. """
    onion_websites = []
    clear_websites = []
    for site in seed_websites:
        page = pagereader.read_page(site, False)
        onion, clear = get_links(soup=page,ext=False, live=False, printout=False)
        onion_websites = onion_websites + onion
        clear_websites = clear_websites + clear

    return (onion_websites,clear_websites)




def print_row(url, description):
    print("%-80s %-30s" % (url, description))
