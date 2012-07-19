# -*- coding: utf-8 -*-
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
# version 1.2

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

#print enclist

current = 0
int1251 = 0
int866  = 0
intkoi8r= 0

if len(enclist) > 0:
 while current < len(enclist):
#  print(current, ".", enclist[current])

  if enclist[current] ==  "WINDOWS-1251":
    int1251 = current
  if enclist[current] ==  "CP866":
    int866 = current
  if enclist[current] ==  "KOI8R":
    intkoi8r = current

  current = current + 1


UI_XML = """<ui>
<menubar name="MenuBar">
    <menu name="rootMenu" action="rootMenuAction">
        <placeholder>
        <menuitem name="Action1" action="action1251"/>
        <menuitem name="Action2" action="action866"/>
        <menuitem name="Action3" action="actionkoi8r"/>
        <menuitem name="Action4" action="actionutf8"/>
        <separator/>
        <menu action="SubMenuAction">
%s
        </menu>
        </placeholder>
    </menu>
</menubar>
</ui>""" % "\n".join(["<menuitem name=\"Encoding%i\" action=\"Encoding%i\"/>" % (i, i) for i in range(len(enclist))])


class ExamplePlugin04(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "ExamplePlugin04"
    window = GObject.property(type=Gedit.Window)
   
    def __init__(self):
        GObject.Object.__init__(self)
    
    def _add_ui(self):
        manager = self.window.get_ui_manager()
        
        #action_filemenu = Gtk.ActionGroup("test", "File", None, None)
        #self._actions.add_actions(action_filemenu)

        self._actions = Gtk.ActionGroup("rootMenuGroup")
        self._actions.add_actions([
            ('rootMenuAction', Gtk.STOCK_UNDERLINE, "Кодировка", 
                None, "Открыть текущий документ в другой кодировке", 
                self.on_example_action_activate2),
        ])
        manager.insert_action_group(self._actions)

                
        self._actions = Gtk.ActionGroup("SubMenu")
        self._actions.add_actions([
            ('SubMenuAction', Gtk.STOCK_PASTE, "Другие кодировки", 
                None, "Список кодировок", 
                self.on_example_action_activate2),
        ])
        manager.insert_action_group(self._actions)

#        self._actions = Gtk.ActionGroup("Example04Actions")
#        self._actions.add_actions([
#            ('ExampleAction', Gtk.STOCK_INFO, "Say _Hello", 
#                None, "Say hello to the current document", 
#                self.on_example_action_activate),
#        ])
#        manager.insert_action_group(self._actions)


        self._actions = Gtk.ActionGroup("group1251")
        self._actions.add_actions([
            ('action1251', Gtk.STOCK_DND_MULTIPLE, "WINDOWS-1251",    None, "Документ в кодировку Windows-1251", 
                 self.to_cp1251), ])
        manager.insert_action_group(self._actions)
        
        self._actions = Gtk.ActionGroup("group866")
        self._actions.add_actions([
            ('action866', Gtk.STOCK_DND_MULTIPLE, "CP866",  None, "Документ в кодировку CP866", 
                 self.to_cp866), ])
        manager.insert_action_group(self._actions)
    
        self._actions = Gtk.ActionGroup("groupkoi8r")
        self._actions.add_actions([
            ('actionkoi8r', Gtk.STOCK_DND_MULTIPLE, "KOI8R",  None, "Документ в кодировку KOI8R", 
                 self.to_koi8r), ])
        manager.insert_action_group(self._actions)
        

        self._actions = Gtk.ActionGroup("grouputf8")
        self._actions.add_actions([
            ('actionutf8', Gtk.STOCK_DND_MULTIPLE, "UTF-8",  None, "Документ в кодировку UTF-8", 
                 self.to_utf8), ])
        manager.insert_action_group(self._actions)


        self._action_group = Gtk.ActionGroup("Codepage")

        self._action_group.add_actions([("Codepage", None, _("CODEPAGE:"))] + \
           [("Encoding%i" % i, Gtk.STOCK_DND_MULTIPLE, enclist[i], None, _("Документ в кодировку ")+" "+enclist[i],
           functools.partial(self.reopen_document, enc=enclist[i], ii=i )) \
           for i in range(len(enclist))])
        manager.insert_action_group(self._action_group, -1)

        
        self._ui_merge_id = manager.add_ui_from_string(UI_XML)
        manager.ensure_update()
        
        
    def do_activate(self):
        self._add_ui()

    def do_deactivate(self):
        self._remove_ui()

    def do_update_state(self):
        pass
    
    def on_example_action_activate(self, action, data=None):
        view = self.window.get_active_view()
        if view:
            view.get_buffer().insert_at_cursor("Hello World! %D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%")
            
    def on_example_action_activate2(self, action, data=None):
        view = self.window.get_active_view()
               
    def _remove_ui(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_merge_id)
        manager.remove_action_group(self._actions)
        manager.ensure_update()

    def reopen_document(self, action, enc,ii):
        doc = self.window.get_active_document()
        if not doc:
            return
        doc.load(Gio.file_new_for_commandline_arg(doc.get_uri_for_display()), Gedit.encoding_get_from_index(ii), 0, 0, False)

    # Menu activate handlers
    def to_cp1251(self, action):
        doc = self.window.get_active_document()
        if not doc:
            return
        doc.load(Gio.file_new_for_commandline_arg(doc.get_uri_for_display()), Gedit.encoding_get_from_index(int1251), 0, 0, False)

    def to_cp866(self, action):
        doc = self.window.get_active_document()
        if not doc:
            return
        doc.load(Gio.file_new_for_commandline_arg(doc.get_uri_for_display()), Gedit.encoding_get_from_index(int866), 0, 0, False)

    def to_koi8r(self, action):
        doc = self.window.get_active_document()
        if not doc:
            return
        doc.load(Gio.file_new_for_commandline_arg(doc.get_uri_for_display()), Gedit.encoding_get_from_index(intkoi8r), 0, 0, False)

    def to_utf8(self, action):
        doc = self.window.get_active_document()
        if not doc:
            return
        doc.load(Gio.file_new_for_commandline_arg(doc.get_uri_for_display()), Gedit.encoding_get_current(), 0, 0, False)

