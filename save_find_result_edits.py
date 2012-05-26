import sublime, sublime_plugin
import re
import time

# Saves the edits made in the Find Results view to the original files

find_result_edits = {}
def apply_edits(view):
  edited_lines = find_result_edits.get(unicode(view.file_name()), {})
  if unicode(view.file_name()) not in find_result_edits:
    print "file not edited: %s" % view.file_name()
    return

  try:
    edit = view.begin_edit()
    line_regions = view.lines(sublime.Region(0, view.size()))
    for line_number in reversed(sorted(edited_lines)):
      view.replace(
        edit, 
        line_regions[line_number - 1], 
        edited_lines[line_number])
    del find_result_edits[unicode(view.file_name())]
  finally:
    if edit:
      view.end_edit(edit)

class SaveFindResultEdits(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view

    if view.name() != u'Find Results':
      return

    file_name_matcher = re.compile('^[^ ].*:$')
    # maybe only the search result lines should be saved?
    result_line_matcher = re.compile('^  *([0-9]+)[: ] (.*)')

    line_regions = view.lines(sublime.Region(0, view.size()))
    current_file = None

    find_result_edits.clear()
    for line_region in line_regions:
      line = view.substr(line_region)
      if file_name_matcher.match(line):
        current_edits = {}
        find_result_edits[line[:-1]] = current_edits
      
      result_match = result_line_matcher.match(line)
      if result_match:
        line_number, line = result_match.groups()
        current_edits[int(line_number)] = line

    window = view.window()
    for file_name in find_result_edits:
      v = window.open_file(file_name)

class SaveFindResultEditsLoadListener(sublime_plugin.EventListener):
  def on_load(self, view):
    print "loaded: %s" % view.file_name()
    apply_edits(view)