from markdown import markdown
from urllib.parse import urlparse
from IPython.display import HTML
import re
from pathlib import Path
import namedlist as nl

from .utils import get_url_images_in_text
from .tags import tag_reader
from .cache import file_to_base64

CardTuple = nl.namedlist('CardTuple', [
    ('front', ''),
    ('back', ''),
    ('keywords', ''),
    ('tags', '')
])


class CardQuiz:
    def __init__(self, card_id, record):
        """
        :param int card_id:
        :param dict|OrderedDict record:
        """
        assert isinstance(record, CardTuple)

        self.record = record
        self.id = card_id

    def _repr_html_(self):
        html = self._parse_markdown(re.sub(r'\n+', '\n\n', self.record.front))
        # html += "<br />" + markdown(self.record.keywords)
        # html += "<br />" + markdown(self.record.tags)

        return html

    def show(self):
        html = markdown("**Card id:** {}".format(self.id))
        html += self._parse_markdown(re.sub(r'\n+', '\n\n', self.record.back))
        html += markdown("**Keywords:** " + ', '.join(tag_reader(self.record.keywords)))
        html += markdown("**Tags:** " + ', '.join(tag_reader(self.record.tags)))

        return HTML(html)

    def _parse_markdown(self, text):
        for url in get_url_images_in_text(text):
            if urlparse(url).netloc:
                text = text.replace(url, '<img src="{}" />'.format(url))
            else:
                expected_tag = '<img src=""data:image/{};base64, {}" />'.format(Path(url).suffix, file_to_base64(url))
                print("Please use {} instead of {}".format(expected_tag, url))
                text = text.replace(url, expected_tag)

        return markdown(text)
