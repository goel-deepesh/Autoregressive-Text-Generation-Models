# Importing Libararies

import random
import numpy as np
from collections import defaultdict, Counter
from tqdm import tqdm # Quality-of-life package, makes loading bars in for loops. See github.com/tqdm/tqdm for details.

import matplotlib.pyplot as plt
plt.style.use('classic') # Optional styling for the plots. I think it's pretty.

def _format_download_urls(etextno):
    """
    Returns the possible urls location on the Project Gutenberg servers for a
    given text. Mostly ripped from https://pypi.org/project/Gutenberg/.
    """
    uri_root = r'http://www.gutenberg.lib.md.us'

    if 0 < etextno < 10:
        oldstyle_files = (
            'when11',
            'bill11',
            'jfk11',
            'getty11',
            'const11',
            'liber11',
            'mayfl11',
            'linc211',
            'linc111',
        )
        etextno = int(etextno)
        return '{root}/etext90/{name}.txt'.format(
            root=uri_root,
            name=oldstyle_files[etextno - 1])

    else:
        etextno = str(etextno)
        extensions = ('.txt', '-8.txt', '-0.txt')
        urls = []
        for extension in extensions:
            uri = '{root}/{path}/{etextno}/{etextno}{extension}'.format(
                root=uri_root,
                path='/'.join(etextno[:len(etextno) - 1]),
                etextno=etextno,
                extension=extension)
            urls.append(uri)
        return urls

def download_from_book_id(bookid, bookname):
  """
  Downloads a from book from Project Gutenberg given the book's id number, and
  stores it locally in `bookname.txt`.

  :param      bookid:    The id of the book on Project Gutenberg
  :type       bookid:    int
  :param      bookname:  The name to give the book (or rather the file path to the book)
  :type       bookname:  str
  """

  book_dst = f'{bookname}.txt'

  import os
  from six.moves import urllib

  if os.path.isfile(book_dst):
      print('File %s is already downloaded' % book_dst)
  else:
      possible_urls = _format_download_urls(bookid)
      print(possible_urls)
      for url in possible_urls:
        print(f'trying {url}...')
        try:
          urllib.request.urlretrieve(url, book_dst)
          print(f'Downloaded {bookname}.txt, with book id {bookid}.')
          return
        except urllib.error.HTTPError:
          None
      raise NameError("Couldn't find that book on Gutenberg")

download_from_book_id(100, "Shakespeare")
download_from_book_id(5200, "Metamorphosis")
download_from_book_id(11, "Wonderland")
download_from_book_id(1184, "MonteCristo")

file_handle = open("Wonderland.txt", encoding="utf8")  # It's very important to mention utf8 encoding
wonderland_book_text = file_handle.read()  # Copies the book as a string in memory
file_handle.close()

print(wonderland_book_text[0:1000])

def word_sequence_from_file(filepath):
    """
    Given a filepath to a text file for a Project Gutenberg book, this splits
    the book into a list of strings, where each string is a word from the book.
    Formatting data, like where \n or spaces happen, is destroyed by this, but
    punctuation like "word." are preserved.

    :param      filepath:  The filepath to the book
    :type       filepath:  string

    :returns:   A list of strings without any whitespace.
    :rtype:     List of string
    """

    # Open the file
    with open(filepath, encoding="utf8") as file_handle:
        raw_book_text = file_handle.read()  # Copies the book as a string in memory

    # Find the start and end of the actual book content
    start_marker = '*** START OF'
    end_marker = '*** END OF'

    start_index = raw_book_text.find(start_marker)
    end_index = raw_book_text.find(end_marker)

    # Extract the actual book content between the start and end markers
    if start_index != -1 and end_index != -1:
        book_text = raw_book_text[start_index + len(start_marker):end_index]
    else:
        # If markers are not found, use the entire text
        book_text = raw_book_text

    # Split the book into words (by spaces)
    word_sequence = book_text.split()

    return word_sequence

shakespeare = word_sequence_from_file("Shakespeare.txt")
metamorphosis = word_sequence_from_file("Metamorphosis.txt")
wonderland = word_sequence_from_file("Wonderland.txt")
montecristo = word_sequence_from_file("MonteCristo.txt")

# Prints the first 100 words from Kafka's Metamorphosis
# It's okay if there's a couple extra words at the beginning like
# > "by Franz Kafka Translated by David Wyllie"
# This is just a couple words that will not change our model significantly

display(" ".join(metamorphosis[1:100]))
