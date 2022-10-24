
import os
import sys

import requests
import markdown
import markdownify

from bs4 import BeautifulSoup

class MD:
    def __init__(self, markdown_path):
        markdown_path = markdown_path.strip()
        self.path = markdown_path
        self.parent_folder = os.path.dirname(markdown_path)
        self.filename = os.path.basename(markdown_path)
        
    def prepare(self):
        # create working folder with assets folder inside it
        self.working_folder = os.path.join(self.parent_folder, self.filename.split('.')[0])
        if not os.path.exists(self.working_folder):
            os.mkdir(self.working_folder)
            os.mkdir(os.path.join(self.working_folder, 'assets'))
            self.destination = os.path.join(self.working_folder, self.filename)
        else:
            print('Working folder already exists. Please delete it first.', file=sys.stderr)
            sys.exit(1)

    def process(self):
        # download markdown file
        soup = BeautifulSoup(markdown.markdown(open(self.path).read()), 'html.parser')

        # download all images to assets folder
        # and replace image path in the soup
        for img in soup.find_all('img'):
            img_url = img['src']
            img_filename = img_url.split('/')[-1]
            img_path = os.path.join(self.working_folder, 'assets', img_filename)
            if not os.path.exists(img_path):
                with open(img_path, 'wb') as f:
                    f.write(requests.get(img_url).content)
            img['src'] = os.path.join('assets', img_filename)

        # markdownify the soup
        self.md = markdownify.markdownify(soup.prettify(), heading_style='ATX')

    def save(self):
        with open(self.destination, 'w') as f:
            f.write(self.md)

if __name__ == '__main__':
    for markdown_path in sys.argv[1:]:
        md = MD(markdown_path)
        md.prepare()
        md.process()
        md.save()




