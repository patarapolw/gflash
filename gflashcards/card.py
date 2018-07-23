from markdown import markdown
from urllib.parse import urlparse
from IPython.display import HTML
import re
import namedlist as nl

from .utils import get_url_images_in_text
from .tags import tag_reader

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

    @staticmethod
    def _parse_markdown(text):
        for url in get_url_images_in_text(text):
            if urlparse(url).netloc:
                text = text.replace(url, '<img src="{}" />'.format(url))
            else:
                text = text.replace(url, '<img src="notebook/{}" />'.format(url))

        return markdown(text)
