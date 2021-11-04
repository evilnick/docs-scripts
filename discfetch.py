#!/bin/python3

import re
import requests
import click
from urllib.parse import urljoin
from urllib.parse import urlparse
import os.path

# example: 
# source_url = "https://discourse.charmhub.io/t/charmed-kubeflow-test/5286"

regex = r"\(\/t/.*\)"

def raw_url(string):
    u = urlparse(string)
    path = "/raw/"+u.path.split('/')[-1:][0]
    name = u.path.split('/')[-2:-1][0]
    return (urljoin(u.scheme+"://"+u.netloc,path), name)

def save_raw(original_url,dest):
    url, name = raw_url(original_url)
    r = requests.get(url)
    with open(dest+name+'.md', "w") as f:
        f.write("<!-- METADATA  \n")
        f.write('url: '+original_url)
        f.write("\n!-->\n")
        f.write(r.text)
    return(r)

@click.command()
@click.argument('source_url')
@click.option('--dest', '-d', default="docs/",show_default=True, \
    help="Destination directory.")
@click.option('--follow/--no-follow', default=False,show_default=True, \
    help=" Whether to follow links from the given URL and fetch those topics also (useful for grabbing the whole documentation set from the index topic)")
def main(source_url, dest, follow):

    """This tool will automatically download and save the
    Markdown content of the discourse post pointed to 
    by the SOURCE_URL argument.

    It will also download and save the Markdown files of 
    any discourse posts linked to in the initial document.

    By default these are saved in the local 'docs/' directory
    if it exists, or optionally a specified DEST destination.
    """

    if not os.path.isdir(dest):
        click.echo('not a valid destination directory')
        exit()
    u = urlparse(source_url)
    response = save_raw(source_url,dest)

    if follow:
        # search the response for links to other pages
        matches = re.finditer(regex, response.text, re.MULTILINE)
        link_set = set()
        click.echo("Found links-")
        
        #read matches into a set to de-dupe
        for i in matches:
            link_url = urljoin(u.scheme+"://"+u.netloc,i.group()[1:-1])
            link_set.add(link_url)
        
        for i in link_set:
            click.echo(i)
            save_raw(i,dest)

if __name__ == "__main__":
    main()

