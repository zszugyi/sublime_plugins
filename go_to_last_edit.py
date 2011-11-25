import sublime, sublime_plugin

last_point = None
last_view_id = None

class EditListener(sublime_plugin.EventListener):
  def on_modified(self, view): 
    global last_point
    global last_view_id

    last_view_id = view.id() 
    last_point = view.sel()[0]

class GoToLastEditCommand(sublime_plugin.WindowCommand):

  def run(self):
    global last_point
    global last_view_id

    if last_point is None or last_view_id is None:
      print "no previous edit location"
    else:
      window = sublime.active_window()
      views = window.views()
      last_view = filter(lambda view: view.id() == last_view_id, views)
      if last_view:
        view = last_view[0]
        window.focus_view(view)
        view.sel().clear()
        view.sel().add(last_point)
        view.show(last_point) # why u no work?
      else:
        print "last view not found"
