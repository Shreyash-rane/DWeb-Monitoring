from lib2to3.pytree import type_repr
from pydoc import cli
from browser.ahima import *
from connection.tor import *
import click

QUERY = ["arms","carding","drugs","hacker","murder"]
BROWSER = ["tor","ahima"]

'''
    function return type:
    List= [important , logging message , error message]
'''
def print_blue_text(text):
    blue_code = '\033[34m'  # ANSI escape code for blue color
    reset_code = '\033[0m'  # ANSI escape code to reset color

    print(f"{blue_code}{text}{reset_code}")
logo = r'''
▓█████▄  ▄▄▄       ██▀███   ██ ▄█▀    █     █░▓█████  ▄▄▄▄       ███▄ ▄███▓ ▒█████   ███▄    █  ██▓▄▄▄█████▓ ▒█████   ██▀███  
▒██▀ ██▌▒████▄    ▓██ ▒ ██▒ ██▄█▒    ▓█░ █ ░█░▓█   ▀ ▓█████▄    ▓██▒▀█▀ ██▒▒██▒  ██▒ ██ ▀█   █ ▓██▒▓  ██▒ ▓▒▒██▒  ██▒▓██ ▒ ██▒
░██   █▌▒██  ▀█▄  ▓██ ░▄█ ▒▓███▄░    ▒█░ █ ░█ ▒███   ▒██▒ ▄██   ▓██    ▓██░▒██░  ██▒▓██  ▀█ ██▒▒██▒▒ ▓██░ ▒░▒██░  ██▒▓██ ░▄█ ▒
░▓█▄   ▌░██▄▄▄▄██ ▒██▀▀█▄  ▓██ █▄    ░█░ █ ░█ ▒▓█  ▄ ▒██░█▀     ▒██    ▒██ ▒██   ██░▓██▒  ▐▌██▒░██░░ ▓██▓ ░ ▒██   ██░▒██▀▀█▄  
░▒████▓  ▓█   ▓██▒░██▓ ▒██▒▒██▒ █▄   ░░██▒██▓ ░▒████▒░▓█  ▀█▓   ▒██▒   ░██▒░ ████▓▒░▒██░   ▓██░░██░  ▒██▒ ░ ░ ████▓▒░░██▓ ▒██▒
 ▒▒▓  ▒  ▒▒   ▓▒█░░ ▒▓ ░▒▓░▒ ▒▒ ▓▒   ░ ▓░▒ ▒  ░░ ▒░ ░░▒▓███▀▒   ░ ▒░   ░  ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ░▓    ▒ ░░   ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
 ░ ▒  ▒   ▒   ▒▒ ░  ░▒ ░ ▒░░ ░▒ ▒░     ▒ ░ ░   ░ ░  ░▒░▒   ░    ░  ░      ░  ░ ▒ ▒░ ░ ░░   ░ ▒░ ▒ ░    ░      ░ ▒ ▒░   ░▒ ░ ▒░
 ░ ░  ░   ░   ▒     ░░   ░ ░ ░░ ░      ░   ░     ░    ░    ░    ░      ░   ░ ░ ░ ▒     ░   ░ ░  ▒ ░  ░      ░ ░ ░ ▒    ░░   ░ 
   ░          ░  ░   ░     ░  ░          ░       ░  ░ ░                ░       ░ ░           ░  ░               ░ ░     ░     
 ░                                                         ░                                                                  

'''
print_blue_text(logo)




@click.command() 
@click.option("--query",type=click.Choice(QUERY),prompt="Choose your Query",help="Choose a word from: {}".format(','.join(QUERY)))
@click.option("--engine",type=click.Choice(BROWSER),prompt="Choose search Engine",help="Choose a word from: {}".format(','.join(BROWSER)))


def query_to_browser(query,engine):
    tor_Proxy = set_tor_proxy()
    if tor_Proxy[1]==True:
        print ("Proxy Enable")
        if engine==BROWSER[0]:
            print("UPCOMONG >>>")
        if engine==BROWSER[1]:
            a = AhimaScraper(query,tor_Proxy[0])
            print(query," Run and size ",len(a))


   


if  __name__ == "__main__":
    query_to_browser()