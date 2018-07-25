## Advanced Usage

### `Flashcards` class

#### `Flashcards.iter_quiz()`

Create a generator for building a non-repeating quiz.

```python
>>> from gflashcards import Flashcards
>>> fc = Flashcards(spreadsheet_id)
>>> iter_quiz = fc.iter_quiz(keyword_regex)
>>> card = next(iter_quiz)
```

#### `Flashcards.view()`

View what `Flashcards.quiz()` and `Flashcards.iter_quiz()` would possibly show.

Also, you might actually learn more from a table, rather than from a flashcard.

#### `Flashcards.tags`

A property showing the list of all available tags.

## Uploading images to Imgur (programmatically)

Please get a client-ID from https://api.imgur.com/oauth2/addclient

Using [Postman](https://apidocs.imgur.com/) is the way recommended by Imgur. Postman is also available in Chrome browser.
