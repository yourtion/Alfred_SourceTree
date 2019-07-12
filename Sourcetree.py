# encoding: utf-8
import sys
import os
import re
from workflow import Workflow3

log = None

class SourceTree:

  homePath=os.path.expanduser('~')
  filePath= homePath + "/Library/Application Support/SourceTree/browser.plist"

  def _camel_case_split(self, identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]

  def _splitMatchWords(self, title):
    res = [title]
    cam = self._camel_case_split(title)
    for m in cam:
      ret = re.split('-|_| |',m)
      for n in ret:
        res.append(n)
    return ' '.join(res);

  def getProjects(self):
    from biplist import readPlist
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
    

def main(wf):
    projects = SourceTree().getProjects()
    query = None
    if len(wf.args):
      query = wf.args[0]
    projects = wf.filter(query, projects, lambda project: project[0])
    for p in projects:
      wf.add_item(
        title=p[0],
        subtitle=p[1],
        arg=p[1],
        valid=True
      )
    wf.send_feedback()

if __name__ == u"__main__":
    wf = Workflow3(libraries=['./lib'])
    log = wf.logger
    sys.exit(wf.run(main))
