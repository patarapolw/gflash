import re


def get_url_images_in_text(text):
    return re.findall(r'((?:(?<=^)|(?<=\s))(?<!<img src=["\'])[^\s<>"\']+\.(?:png|jpg|jpeg|gif))', text)


def compare_list_match_regex(subset, superset):
    def _sub_compare(sub_item):
        for super_item in superset:
            if re.search(sub_item, super_item, flags=re.IGNORECASE):
                return True

        return False

    result = []
    for sub_item in subset:
        result.append(_sub_compare(sub_item))

    return all(result)
