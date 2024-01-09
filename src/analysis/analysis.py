from bs4 import BeautifulSoup
import re
from database.database import *

def analyze(url, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    emails = list(set(re.findall(email_pattern, html_content)))

    usernames = [element.text.strip() for element in soup.find_all('span', class_='username')]

    links = [a['href'] for a in soup.find_all('a', href=True)]
    data = {
        'url': url,
        'emails': emails,
        'usernames': usernames,
        'links': links
    }
    print("work")
    insert_query = "INSERT INTO analytic_table (url, email, username, links) VALUES (%s, %s, %s, %s)"
    execute_query(insert_query, (data['url'], data['emails'], data['usernames'], data['links']))

