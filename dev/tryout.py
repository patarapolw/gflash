from gflashcards.utils import get_url_images_in_text

if __name__ == '__main__':
    url = 'https://docs.python.org/3/library/re2.jpg https://docs.python.org/3/library/re.jpg'
    print(get_url_images_in_text(url))
