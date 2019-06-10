from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from setup import setup




def log(string):
    with open('logs.txt', 'w+', encoding='utf-8') as f:
        f.write(string)


def even(number):

  return any([number == i for i in [2, 4, 6, 8, 10, 12]])



def test():
  testy = {'a': 23, 'b': 45}
  print(testy)
  testy.update({'a':45})
  print(testy)

# test()




def find_str(test_str, str_to_find):
  counter = 0
  for i in test_str:
    if i == str_to_find:
      counter +=1
  return counter


def replace_string(string, find_string, replace_with):
  return_string = ""
  for i in string:
    if i == find_string:
      return_string += replace_with
      continue
    return_string += i
  return return_string


def main():
    document = setup()
    print('The title of the document is: {}'.format(document.get('title')))
    for i in document.get('body').get('content'):
      # intel(i)
      # print(i.get('paragraph').get('elements')[0].get('textRun').get('content'))
      # input("[ENTER]")
      try:
        content = i.get('paragraph').get('elements')[0].get('textRun').get('content')
        if content is not None: 
          print(content)
          if even(find_str(i.get('paragraph').get('elements')[0].get('textRun').get('content'), '`')):
            print(replace_string(content, '`', '||||||'))

      except AttributeError as e:
        print(f"no object: {e}")
    # log(f"-  -  -\n{document.get('body')}")

def intel(thing):
  log(f"Size: {len(thing)}\nType: {type(thing)}\n---\n{thing}")
  print(f"Size: {len(thing)}\nType: {type(thing)}\n---\n{thing}")


if __name__ == '__main__':
    main()

