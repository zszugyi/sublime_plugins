import sublime, sublime_plugin
import re

class BreakLineAtCommas(sublime_plugin.TextCommand):
  def run(self, edit):
    for selection in reversed(self.view.sel()):
      current_line_region = self.view.line(selection)
      current_line = self.view.substr(current_line_region)
      indent = re.search('(^ *)', current_line).group(0)

      split_lines = [indent + chunk.strip() for chunk in current_line.split(',')]
      replacement = ",\n".join(split_lines)
      
      self.view.replace(edit, current_line_region, replacement)