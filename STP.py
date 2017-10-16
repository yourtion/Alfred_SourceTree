#!/usr/bin/python
from biplist import *
import json
import os
import re

class SourceTree:

  homePath=os.path.expanduser('~')
  filePath= homePath + "/Library/Application Support/SourceTree/browser.plist"

  def _camel_case_split(self, identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]

  def _splitMatchWords(self, title):
    res = []
    cam = self._camel_case_split(title)
    for m in cam:
      ret = re.split('-|_| |',m)
      for n in ret:
        res.append(n)
    return ' '.join(res);

  def _getProjects(self):
    try:
      plist = readPlist(self.filePath)
      tempName = ""
      res = []
      for item in plist['$objects']:
        if(type(item) is str and item[:1] == '/'):
          res.append([tempName, item])
        elif (type(item) is str):
          tempName = item
      return res
    except e:
      return []

  def getList(self):
    items = []
    projects = self._getProjects()
    for p in projects:
      item = {
        'title': p[0],
        'subtitle': p[1],
        'arg': p[1],
        'match': self._splitMatchWords(p[0])
      }
      items.append(item)
    result = {'items': items}
    print(json.dumps(result))
