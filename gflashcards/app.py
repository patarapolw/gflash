import re
import random
from pyhandsontable import view_table
from threading import Timer
from pathlib import Path
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

    def view(self, keyword_regex: str='', tags: list=None, width=800, height=500):
        renderers = {
            1: 'markdownRenderer',
            2: 'markdownRenderer'
        }
        config = {
            'colHeaders': ['id'] + list(CardTuple._fields),
            'rowHeaders': False
        }

        filename = Path('temp.handsontable.html')
        try:
            table = view_table(data=list(reversed([[i] + list(record.to_formatted_tuple())
                                                   for i, record in self.find(keyword_regex, tags)])),
                               width=width,
                               height=height,
                               renderers=renderers,
                               config=config,
                               filename=str(filename),
                               autodelete=False)
            with filename.open('r') as f:
                soup = BeautifulSoup(f.read(), 'html5lib')

            style = soup.new_tag('style')

            with Path('gflashcards/renderer/markdown-hot.css').open('r') as f:
                style.append(f.read())

            soup.head.append(style)

            div = soup.new_tag('div')

            js_markdown = soup.new_tag('script',
                                       src='https://cdn.rawgit.com/showdownjs/showdown/1.8.6/dist/showdown.min.js')
            js_custom = soup.new_tag('script')

            with Path('gflashcards/renderer/markdown-hot.js').open('r') as f:
                js_custom.append(f.read())

            div.append(js_markdown)
            div.append(js_custom)

            script_tag = soup.find('script', {'id': 'generateHandsontable'})
            soup.body.insert(soup.body.contents.index(script_tag), div)

            with filename.open('w') as f:
                f.write(str(soup))

            return table
        finally:
            Timer(5, filename.unlink).start()
            # pass

    def iter_quiz(self, keyword_regex: str='', tags: list=None, exclude: list =None, image_only=False,
                  begin:int=None, last: int=None):
        if exclude is None:
            exclude = list()

        all_records = list(reversed([(i, record)
                                     for i, record in self.find(keyword_regex, tags)
                                     if i not in exclude]))[begin:last]

        if image_only:
            all_records = [(i, record) for i, record in all_records
                           if len(get_url_images_in_text(record.front)) > 0]

        if len(all_records) == 0:
            return "There is no record matching the criteria."

        random.shuffle(all_records)
        for i, record in all_records:
            yield CardQuiz(i, record)

    def quiz(self, keyword_regex: str='', tags: list=None, exclude: list =None, image_only=False,
             begin: int=None, last: int=None):
        return next(self.iter_quiz(keyword_regex, tags, exclude, image_only, begin=begin, last=last))

    @property
    def tags(self):
        tags = set()

        for v in self.data:
            tags.update(tag_reader(v.tags))

        return tags
