# Open the document in a different encoding
# Install: copy mencode.plugin and mencode.py to ~/.local/share/gedit/plugins/
# Copyright (C) 2012 Oleg Malovichko privatbank@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# version 1.0

from gettext import gettext as _
from gi.repository import GObject, Gtk, Gedit, Gio
import functools


#all codepage list
encs = []
i = 0
enc = Gedit.encoding_get_from_index(i)

while(enc != None):
 encs.append(enc)
 i = i + 1
 enc = Gedit.encoding_get_from_index(i)

#print encs

# list code page name
enclist = []
for enc in encs:
   enclist.append(enc.get_charset())

print enclist

current = 0
int1251 = 0
int866  = 0
intkoi8r= 0

if len(enclist) > 0:
 while current < len(enclist):
  print(current, ".", enclist[current])

  if enclist[current] ==  "WINDOWS-1251":
    int1251 = current
  if enclist[current] ==  "CP866":
    int866 = current
  if enclist[current] ==  "KOI8R":
    intkoi8r = current

  current = current + 1


UI_XML0 = """<ui>
<menubar name="MenuBar">
    <menu name="EditMenu" action="Edit">
      <placeholder name="EditOps_7">
        <menuitem name="CPAction" action="CPAction"/>
      </placeholder>
     </menu>
   </menubar>
</ui>"""

UI_XML1 = """<ui>
<menubar name="MenuBar">
    <menu name="EditMenu" action="Edit">
      <placeholder name="EditOps_8">
        <menuitem name="CPAction1" action="CPAction1"/>
      </placeholder>
     </menu>
   </menubar>
</ui>"""

UI_XML2 = """<ui>
<menubar name="MenuBar">
    <menu name="EditMenu" action="Edit">
      <placeholder name="EditOps_9">
        <menuitem name="CPAction2" action="CPAction2"/>
      </placeholder>
     </menu>
   </menubar>
</ui>"""


# Menu item
ui_str = """<ui>
 <menubar name="MenuBar">
   <menu name="ToolsMenu" action="Tools">
     <placeholder name="ToolsOps_9">
        <menuitem name="Codepage" action="Codepage"/>
      </placeholder>
%s
    </menu>
 </menubar>
</ui>
""" % "\n".join(["<menuitem name=\"Encoding%i\" action=\"Encoding%i\"/>" % (i, i) for i in range(len(enclist))])

class mencode(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "mencode"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
     GObject.Object.__init__(self)

    def do_activate(self):
        # Insert menu items
        self._insert_menu()

    def do_deactivate(self):
        # Remove any installed menu items
        self._remove_menu()
        self._action_group = None


    def _insert_menu(self):
        manager = self.window.get_ui_manager()
        self._actions = Gtk.ActionGroup("CP07Actions")
        self._actions.add_actions([
            ('CPAction', Gtk.STOCK_INFO, "WINDOWS-1251", 
                 None, "Document to codepage Windows-1251", 
                 self.to_cp1251),
        ])
        manager.insert_action_group(self._actions)
        self._ui_merge_id = manager.add_ui_from_string(UI_XML0)
        manager.ensure_update()
        
        self._actions = Gtk.ActionGroup("CP08Actions")
        self._actions.add_actions([
            ('CPAction1', Gtk.STOCK_INFO, "CP866", 
                 None, "Document to codepage CP866", 
                 self.to_cp866),
        ])
        manager.insert_action_group(self._actions)
        self._ui_merge_id = manager.add_ui_from_string(UI_XML1)
        manager.ensure_update()
    
        self._actions = Gtk.ActionGroup("CP09Actions")
        self._actions.add_actions([
            ('CPAction2', Gtk.STOCK_INFO, "KOI8R", 
                 None, "Document to codepage KOI8R", 
                 self.to_koi8r),
        ])
        manager.insert_action_group(self._actions)
        self._ui_merge_id = manager.add_ui_from_string(UI_XML2)
        manager.ensure_update()

        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()

# -------------------
        # Create a new action group
        self._action_group = Gtk.ActionGroup("Codepage")

        self._action_group.add_actions([("Codepage", None, _("CODEPAGE:"))] + \
           [("Encoding%i" % i, None, enclist[i], None, _("Document to codepage ")+" "+enclist[i],
           functools.partial(self.reopen_document, enc=enclist[i], ii=i )) \
           for i in range(len(enclist))])
        manager.insert_action_group(self._action_group, -1)

        # Merge the UI
        self._ui_id = manager.add_ui_from_string(ui_str)

    def reopen_document(self, action, enc,ii):
        doc = self.window.get_active_document()
        if not doc:
            return
        doc.load(Gio.file_new_for_commandline_arg(doc.get_uri_for_display()), Gedit.encoding_get_from_index(ii), 0, 0, False)


    def _remove_menu(self):
        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()
        # Remove the ui
        manager.remove_ui(self._ui_id)
        # Remove the action group
        manager.remove_action_group(self._action_group)
        # Make sure the manager updates

    # Menu activate handlers
    def to_cp1251(self, action):
        doc = self.window.get_active_document()
        if not doc:
            return
        print int1251
        doc.load(Gio.file_new_for_commandline_arg(doc.get_uri_for_display()), Gedit.encoding_get_from_index(int1251), 0, 0, False)

    def to_cp866(self, action):
        doc = self.window.get_active_document()
        if not doc:
            return
        print int866
        doc.load(Gio.file_new_for_commandline_arg(doc.get_uri_for_display()), Gedit.encoding_get_from_index(int866), 0, 0, False)

    def to_koi8r(self, action):
        doc = self.window.get_active_document()
        if not doc:
            return
        print int866
        doc.load(Gio.file_new_for_commandline_arg(doc.get_uri_for_display()), Gedit.encoding_get_from_index(intkoi8r), 0, 0, False)


