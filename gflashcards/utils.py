import re
from markdown import markdown


def get_url_images_in_text(text):
    return re.findall(r'((?:(?<=^)|(?<=\s))(?<!<img src=["\'])[^\s<>"\']+\.(?:png|jpg|jpeg|gif))', text)


def compare_list_match_regex(subset, superset):
    def _sub_compare():
        for super_item in superset:
            if re.search(sub_item, super_item, flags=re.IGNORECASE):
                return True

        return False

    result = []
    for sub_item in subset:
        result.append(_sub_compare())

    return all(result)


def parse_markdown(text, image_width=500):
    text = re.sub(r'\n+', '\n\n', text)
    for url in get_url_images_in_text(text):
        text = text.replace(url, '<img src="{}" width="{}"/>'.format(url, image_width))

    return markdown(text)
