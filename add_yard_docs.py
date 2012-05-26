import sublime, sublime_plugin
import re

class AddYardDocs(sublime_plugin.TextCommand):
  def run(self, edit):
    for selection in reversed(self.view.sel()):
      current_line_region = self.view.line(selection)
      current_line = self.view.substr(current_line_region)
      
      params_match = re.search('def +[^ (]+[ (]*([^)]*)\)?', current_line)
      if not params_match: return

      params = [p.strip() for p in params_match.group(1).split(',') if len(p.strip()) > 0]

      indent = re.search('(^ *)', current_line).group(0)

      lines = ["%s# @param [] %s" % (indent, param) for param in params]
      lines.insert(0, indent + "# ")
      lines.append(indent + "# @return ")

      # TODO: get the line ending from sublime
      comment = "\r\n".join(lines) + "\r\n"
      self.view.insert(edit, current_line_region.begin(), comment)