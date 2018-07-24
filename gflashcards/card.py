from markdown import markdown
from IPython.display import HTML
from typing import NamedTuple

from .tags import tag_reader
from .utils import parse_markdown


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
        html = parse_markdown(self.record.front)

        return html

    def show(self):
        html = markdown("**Card id:** {}".format(self.id))
        html += parse_markdown(self.record.back)
        html += markdown("**Keywords:** " + ', '.join(tag_reader(self.record.keywords)))
        html += markdown("**Tags:** " + ', '.join(tag_reader(self.record.tags)))

        return HTML(html)


class CardTuple(NamedTuple):
    front: str = ''
    back: str = ''
    keywords: str = ''
    tags: str = ''

    def to_formatted_tuple(self):
        return self.front, self.back, self.keywords, self.tags
