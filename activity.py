#!/usr/bin/env python

# Copyright (C) 2009, Simon Schampijer
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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import sys, os, platform

from gi.repository import Gtk
from gi.repository import Vte
from gi.repository import GLib

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import StopButton

print("RUUUUN")

class RiverHexActivity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.max_participants = 1

        print("RUNNED")
        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        title_entry = TitleEntry(self)
        toolbar_box.toolbar.insert(title_entry, -1)
        title_entry.show()
        
        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()
        
        vt = Vte.Terminal()
        vt.connect("child-exited", self.exit)
        vt.spawn_sync(Vte.PtyFlags.DEFAULT, os.environ["HOME"],
            ["/bin/bash"], [], GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None, None)
        self.set_canvas(vt)
        vt.show()

        if platform.machine().startswith('arm'):
            vt.feed_child("echo \"RiverHex, this activity won't run on this computer\"; sleep 10; exit\n", -1)
        else:
            vt.feed_child("cd $SUGAR_BUNDLE_PATH/bin; ./bin/riverhexactivity-activity; exit\n", -1)

    def exit(self, vt, data):
        self.close()

