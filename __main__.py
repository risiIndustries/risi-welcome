#!/usr/bin/env python3
import gi
import subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio

icons = Gtk.IconTheme.get_default().list_icons(None)
settings = Gio.Settings.new("io.risi.welcome")

packagesproc = subprocess.run(["rpm", "-qa", "--qf", "%{NAME}\n"], stdout=subprocess.PIPE)

class Welcome:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("/usr/share/risiWelcome/risiWelcome.ui")
        startup_check = self.builder.get_object("startup_check")
        startup_check.set_active(settings.get_boolean("startup-show"))
        startup_check.connect("toggled", lambda btn: settings.set_boolean("startup-show", btn.get_active()))

        firststeps = [
            Step(
                "nvidia",
                "Install Proprietary NVIDIA Drivers (Highly Recommended)",
                "Installs proprietary NVIDIA drivers that significantly increase performence.",
                ["/usr/bin/risi-script-gtk", "/usr/share/risiWelcome/scripts/nvidia.risisc", "--trusted"],
                not nouveau_running() and not check_package("akmod-nvidia"), True
            ),
            Step(
                "applications-multimedia-symbolic",
                "Setup RPMFusion &amp; Proprietary Codecs (Highly Recommended)",
                "Installs RPMFusion which allows contains some extra software that risiOS/Fedora cannot ship, and\nproprietary codecs that may be needed to use some media files and render some websites.",
                ["/usr/bin/risi-script-gtk", "/usr/share/risiWelcome/scripts/multimedia.risisc", "--trusted"],
                not check_package("rpmfusion-free-release") and
                not check_package("rpmfusion-nonfree-release") and
                not check_package("gstreamer1-plugins-ugly"), True
            ),
            Step(
                "applications-multimedia-symbolic",
                "Setup Flathub (Highly Recommended)",
                "Install Flatpak and sets up Flathub. This gives you a bigger selection of apps including some proprietary apps. ",
                ["/usr/bin/risi-script-gtk", "/usr/share/risiWelcome/scripts/flatpaks.risisc", "--trusted"],
                not check_package("flatpak"), True
            ),
            Step(
                "timeshift",
                "Setup System Snapshots with Timeshift",
                "We recommend setting up system snapshots so that you have a place to restore your computer to if "
                "something breaks.\n\nNOTE: THIS DOES NOT REPLACE A FULL BACKUP!",
                ["/usr/bin/timeshift-launcher"],
                check_package("timeshift"), False
            ),
            Step(
                "org.gnome.Software",
                "Install Apps with GNOME Software",
                "GNOME Software is used to install and update applications on your computer.",
                ["/usr/bin/gnome-software"],
                check_package("gnome-software"), False
            ),
            Step(
                "webapp-manager",
                "Install Webapps",
                "We use webapps to bridge the gap that Linux has with app compatibility. Turn your favorite webapps "
                "into desktop class apps, and discover new web apps from the store.",
                ["/usr/bin/webapp-manager"],
                check_package("webapp-manager"), False
            ),
            Step(
                "io.risi.Tweaks",
                "Customize risiOS with risiTweaks",
                "risiTweaks is used to enable experimental features such as extensions.",
                ["/usr/bin/risi-tweaks"],
                check_package("risi-tweaks"), False
            )
        ]
        communitysteps = [
            Step(
                "discord",
                "Discord",
                "A chat application used by the risiOS team for development, support, and just hanging out."
                "\n\nNOTE: Please do not direct message admins and moderators for tech support help.",
                ["xdg-open", "https://discord.com/invite/hE2MXgJjK4"],
                True, False
            ),
            Step(
                "twitter",
                "Twitter",
                "Our main social media platform, used for news, announcements.",
                ["xdg-open", "https://twitter.com/risi_os"],
                True, False
            ),
            Step(
                "instagram",
                "Instagram",
                "We put photos here... sometimes.",
                ["xdg-open", "https://instagram.com/risi.io"],
                True, False
            )
        ]
        contributesteps = [
            Step(
                "money",
                "Contribute Financially",
                "While we do not accept full donations yet, check out our shop for some epic t-shirts and more.",
                ["xdg-open", "https://risi.io"],
                True, False
            ),
            Step(
                "image-x-generic",
                "Contribute Wallpapers",
                "Are you a photographer or graphic designer?"
                "\nSubmit your best 4k wallpapers for a chance for them to be in the next risiOS release.",
                ["xdg-open", "https://github.com/risiOS/risios-35-backgrounds"],
                True, False
            ),
            Step(
                "applications-development",
                "Contribute Code",
                "Audit and contribute to our codebase on GitHub.",
                ["xdg-open", "https://github.com/risiOS"],
                True, False
            )
        ]

        steps = self.builder.get_object("stepsBox")
        for item in firststeps:
            steps.add(item)
        steps = self.builder.get_object("communityBox")
        for item in communitysteps:
            steps.add(item)
        steps = self.builder.get_object("contributeBox")
        for item in contributesteps:
            steps.add(item)

        self.window = self.builder.get_object("window")
        self.window.show_all()


class Step(Gtk.Box):
    def __init__(self, icon, name, description, subproc, show, hide_on_click):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        self.set_no_show_all(not show)

        if icon in icons:
            self.icon = Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.DIALOG)
        else:
            self.icon = Gtk.Image.new_from_file(f"/usr/share/risiWelcome/icons/{icon}.png")
        self.icon.set_margin_end(15)
        start_alignment(self.icon)

        self.textbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.name = Gtk.Label()
        self.name.set_markup(f"<b>{name}</b>")
        start_alignment(self.name)
        self.description = Gtk.Label(label=description)
        self.description.set_line_wrap(True)
        self.description.set_xalign(0)
        self.textbox.set_hexpand(True)
        self.textbox.set_margin_end(15)
        start_alignment(self.description)

        self.textbox.add(self.name)
        self.textbox.add(self.description)
        self.textbox.set_vexpand(True)
        start_alignment(self.textbox)

        self.button = Gtk.Button(label="Launch")
        self.button.get_style_context().add_class("suggested-action")
        self.button.connect("clicked", self.btn_clicked, subproc, hide_on_click)
        self.button.set_valign(Gtk.Align.CENTER)

        self.add(self.icon)
        self.add(self.textbox)
        self.add(self.button)

        self.set_margin_start(15)
        self.set_margin_end(15)
        self.set_margin_top(15)
        self.set_margin_bottom(15)

    def btn_clicked(self, button, subproc, hide):
        subprocess.run(subproc)
        self.set_visible(not hide)

def start_alignment(obj):
    obj.set_valign(Gtk.Align.START)
    obj.set_halign(Gtk.Align.START)

def check_package(package):
    return package in packagesproc.stdout.decode('utf-8').split("\n")

def nouveau_running():
    sp = subprocess.run("lsmod | grep nouveau", shell=True)
    return not sp.returncode == 0

window = Welcome()
Gtk.main()
