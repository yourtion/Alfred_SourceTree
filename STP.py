#!/usr/bin/python
from biplist import *
import json
import os

class SourceTree:

  filePath = os.path.expanduser('~') + "/Library/Application Support/SourceTree/browser.plist"

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
        'arg': p[1]
      }
      items.append(item)
    result = {'items': items}
    print(json.dumps(result))
