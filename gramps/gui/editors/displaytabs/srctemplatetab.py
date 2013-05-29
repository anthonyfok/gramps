#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2013       Benny Malengier
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

# $Id$

#-------------------------------------------------------------------------
#
# Python modules
#
#-------------------------------------------------------------------------
from gramps.gen.const import GRAMPS_LOCALE as glocale
_ = glocale.translation.gettext

#-------------------------------------------------------------------------
#
# GTK libraries
#
#-------------------------------------------------------------------------
from gi.repository import Gdk
from gi.repository import Gtk

#-------------------------------------------------------------------------
#
# Gramps libraries
#
#-------------------------------------------------------------------------
from gramps.gen.lib.srcattrtype import SrcAttributeType
from ...autocomp import StandardCustomSelector
from ...widgets.srctemplatetreeview import SrcTemplateTreeView
from .grampstab import GrampsTab

#-------------------------------------------------------------------------
#
# Classes
#
#-------------------------------------------------------------------------
class SrcTemplateTab(GrampsTab):
    """
    This class provides the tabpage for template generation of attributes.
    """
    def __init__(self, dbstate, uistate, track, src, widget, scrolled,
                 callback_src_changed):
        """
        @param dbstate: The database state. Contains a reference to
        the database, along with other state information. The GrampsTab
        uses this to access the database and to pass to and created
        child windows (such as edit dialogs).
        @type dbstate: DbState
        @param uistate: The UI state. Used primarily to pass to any created
        subwindows.
        @type uistate: DisplayState
        @param track: The window tracking mechanism used to manage windows.
        This is only used to pass to generted child windows.
        @type track: list
        @param src: source which we manage in this tab
        @type src: gen.lib.Source
        @param widget: widget with all the elements
        @type widget: GTK dialog
        """
        self.src = src
        self.callback_src_changed = callback_src_changed
        self.readonly = dbstate.db.readonly
        GrampsTab.__init__(self, dbstate, uistate, track, _("Source Template"))
        eventbox = Gtk.EventBox()
        eventbox.add(widget)
        self.pack_start(eventbox, True, True, 0)
        self._set_label(show_image=False)
        widget.connect('key_press_event', self.key_pressed)
        self.setup_interface(scrolled)
        self.show_all()

    def is_empty(self):
        """
        Override base class
        """
        return False

    def setup_interface(self, scrolled):
        """
        Set all information on the widgets
        * template selection
        * setting attribute fields
        
        :param scrolled: GtkScrolledWindow to which to add treeview with templates
        """
        srcattr = SrcAttributeType()
        templ = self.src.get_source_template()
        self.temp_tv = SrcTemplateTreeView(templ[2],
                                sel_callback=self.on_template_selected)
        scrolled.add(self.temp_tv)

    def on_template_selected(self, index, key):
        """
        Selected template changed, we save this and update interface
        """
        self.src.set_source_template(index, key)
        self.callback_src_changed()

##    def setup_autocomp_combobox(self):
##        """
##        Experimental code to set up a combobox with all templates.
##        This is too slow, we use treeview in second attempt
##        """
##        self.srctempcmb = Gtk.ComboBox(has_entry=True)
##        ignore_values = []
##        custom_values = []
##        srcattr = SrcAttributeType()
##        default = srcattr.get_templatevalue_default()
##        maptempval = srcattr.get_templatevalue_map().copy()
##        if ignore_values :
##            for key in list(maptempval.keys()):
##                if key in ignore_values and key not in (None, default):
##                    del map[key]
##
##        self.sel = StandardCustomSelector(
##            maptempval, 
##            self.srctempcmb, 
##            srcattr.get_custom(), 
##            default, 
##            additional=custom_values)
##
##        templ = self.src.get_source_template()
##        self.sel.set_values((templ[0], templ[1]))
##        self.srctempcmb.set_sensitive(not self.readonly)
##        self.srctempcmb.connect('changed', self.on_change_template)
##        srctemphbox.pack_start(self.srctempcmb, False, True, 0)
##        
##        return topvbox

##    def fix_value(self, value):
##        if value[0] == SrcAttributeType.CUSTOM:
##            return value
##        else:
##            return (value[0], '')
##
##    def on_change_template(self, obj):
##        #value = self.fix_value(self.srctempcmb.get_values())
##        value = self.sel.get_values()
##        self.src.set_source_template(value[0], value[1])