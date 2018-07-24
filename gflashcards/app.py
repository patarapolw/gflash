import re
import random
from pathlib import Path
from pyhandsontable import view_table
from threading import Timer
import os
from bs4 import BeautifulSoup

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from .tags import tag_reader
from .utils import get_url_images_in_text
from .card import CardQuiz, CardTuple
from .utils import compare_list_match_regex


class Flashcards:
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

    def __init__(self, spreadsheet_id: str, sheet_name: str= 'flashcards', clientsecrets_path=None, token_path=None):
        """
        :param str spreadsheet_id: Google Sheets spreadsheet id
        :param str sheet_name: Google Sheets sheet_name
        :param str|Path clientsecrets_path:
        :param str|Path token_path:
        """
        range = '{}!A2:D'.format(sheet_name)

        if clientsecrets_path is None:
            clientsecrets_path = Path('user/google/credentials.json')
            if not clientsecrets_path.parent.exists():
                clientsecrets_path.parent.mkdir()
        if token_path is None:
            token_path = clientsecrets_path.with_name('token.json')

        store = file.Storage(str(token_path))
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(str(clientsecrets_path), self.SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('sheets', 'v4', http=creds.authorize(Http()))

        # Call the Sheets API
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                     range=range).execute()
        values = result.get('values', [])
        self.data = list()
        if not values:
            print('No data found.')
        else:
            for row in values:
                self.data.append(CardTuple(*row))

    def find(self, keyword_regex: str = '', tags=None):
        if tags is None:
            tags = list()
        elif isinstance(tags, str):
            tags = [tags]
        else:
            tags = tags

        matched_entries = set()
        for i, item in enumerate(self.data):
            keywords = tag_reader(item.keywords)
            keywords.add(item.front)
            keywords.add(item.back)

            for keyword in keywords:
                if re.search(keyword_regex, keyword, flags=re.IGNORECASE):
                    matched_entries.add(i)

        for i in matched_entries:
            if len(tags) == 0:
                yield i, self.data[i]
            elif compare_list_match_regex(tags, tag_reader(self.data[i].tags)):
                yield i, self.data[i]

    def preview(self, keyword_regex: str='', tags: list=None,
                width=800, height=500):
        config = {
            'colHeaders': ['id'] + list(CardTuple._fields),
            'columns': [
                {'data': 0},
                {'data': 1, 'renderer': 'markdownRenderer'},
                {'data': 2, 'renderer': 'markdownRenderer'},
                {'data': 3},
                {'data': 4}
            ]
        }

        filename = 'temp.handsontable.html'
        try:
            table = view_table(data=([[i] + list(record.to_formatted_tuple())
                                 for i, record in self.find(keyword_regex, tags)]),
                               width=width,
                               height=height,
                               config=config,
                               filename=filename,
                               autodelete=False)
            with open(filename, 'r') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

            div = soup.new_tag('div')

            js_markdown = soup.new_tag('script',
                                       src='https://cdn.rawgit.com/showdownjs/showdown/1.8.6/dist/showdown.min.js')
            js_custom = soup.new_tag('script')

            with open('gflashcards/js/markdown-hot.js') as f:
                js_custom.append(f.read())

            div.append(js_markdown)
            div.append(js_custom)

            script_tag = soup.find('script')
            soup.body.insert(soup.body.contents.index(script_tag) + 1, div)

            with open(filename, 'w') as f:
                f.write(str(soup))

            return table
        finally:
            Timer(5, os.unlink, args=[filename]).start()

    def iter_quiz(self, keyword_regex: str='', tags: list=None, exclude: list =None, image_only=False):
        if exclude is None:
            exclude = list()

        all_records = [(i, record) for i, record in self.find(keyword_regex, tags) if i not in exclude]

        if image_only:
            all_records = [(i, record) for i, record in all_records
                           if len(get_url_images_in_text(record.front)) > 0]

        if len(all_records) == 0:
            return "There is no record matching the criteria."

        random.shuffle(all_records)
        for i, record in all_records:
            yield CardQuiz(i, record)

    def quiz(self, keyword_regex: str='', tags: list=None, exclude: list =None, image_only=False):
        return next(self.iter_quiz(keyword_regex, tags, exclude, image_only))

    @property
    def tags(self):
        tags = set()

        for v in self.data:
            tags.update(tag_reader(v.tags))

        return tags
