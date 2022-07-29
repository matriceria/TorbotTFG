from modules.bcolors import Bcolors
from bs4 import BeautifulSoup
import re

def getMails(soup):

    """
        Searches for <a href> tags for links then checks if link contains the
        substring 'mailto' indicating that it's an email. If it is determined
        to be an email then the link is split and the username is appeneded to
        the list

        Args:
            soup: BeautifulSoup isntance that will be used for parsing

        Returns:
            emails: list of email IDs
    """
    b_colors = Bcolors()

    if isinstance(type(soup), type(BeautifulSoup)):

        emails = []
        links = soup.get_text()
        links=links.lower()
        #print(links)
        x = re.search(".*gas.*", links)
        if x!= None:
            print("keyword encontrada")
            return True
        return False
        """
        for ref in links:
            url = ref.get('href')
            if url and 'mailto' in url:
                email_addr = url.split(':')
                if (len(email_addr) > 1):
                    emails.append(email_addr[1])
        """

        """Pretty print output as below"""
        """
        print ('')
        print (b_colors.OKGREEN+'Mails Found - '+b_colors.ENDC+str(len(emails)))
        print ('-------------------------------')

        return emails
        """

    else:
        raise('Method parameter is not of instance BeautifulSoup')
