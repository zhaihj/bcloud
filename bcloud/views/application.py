# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

from gi.repository import Gio
from gi.repository import GLib
from gi.repository import Gtk

from ..base import const
from ..base.i18n import _
from .about_dialog import AboutDialog
from .main_window import MainWindow
from .preferences_dialog import PreferencesDialog

_kDbusName = "org.liulang.bcloud"

class Application(Gtk.Application):

    def __init__(self):
        super().__init__()
        self.set_application_id(_kDbusName)

    def do_startup(self):
        GLib.set_application_name(const.kAppName)
        Gtk.Application.do_startup(self)
        self.main_window = MainWindow(self)

        app_menu = Gio.Menu.new()
        app_menu.append(_("Preferences"), "app.preferences")
        app_menu.append(_("Sign out"), "app.signout")
        app_menu.append(_("About"), "app.about")
        app_menu.append(_("Quit"), "app.quit")
        self.set_app_menu(app_menu)

        preferences_action = Gio.SimpleAction.new("preferences", None)
        preferences_action.connect("activate",
                                   self.on_preferences_action_activated)
        self.add_action(preferences_action)
        signout_action = Gio.SimpleAction.new("signout", None)
        signout_action.connect("activate", self.on_signout_action_activated)
        self.add_action(signout_action)
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about_action_activated)
        self.add_action(about_action)
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", lambda *args: self.quit())
        self.add_action(quit_action)

    def do_activate(self):
        self.main_window.show_all()

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)
        print("application do_shutdown()")

    def on_preferences_action_activated(self, action, params):
        dialog = PreferencesDialog(self.main_window)
        dialog.run()
        dialog.destroy()

    def on_signout_action_activated(self, action, params):
        pass

    def on_about_action_activated(self, action, params):
        dialog = AboutDialog(self.main_window)
        dialog.run()
        dialog.destroy()
