import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

from zenmapGUI.higwidgets.higboxes import HIGHBox
from zenmapGUI.higwidgets.higlabels import HintWindow


class FilterBar(HIGHBox):
    """This is the bar that appears while the host filter is active. It allows
    entering a string that restricts the set of visible hosts."""

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, ())
    }

    def __init__(self):
        HIGHBox.__init__(self)
        self.information_label = Gtk.Label()
        self.entry = Gtk.Entry()

        self.pack_start(self.information_label, False, True, 0)
        self.information_label.show()

        label = Gtk.Label.new(_("主机过滤："))
        self.pack_start(label, False, True, 0)
        label.show()

        self.pack_start(self.entry, True, True, 0)
        self.entry.show()

        help_button = Gtk.Button()
        icon = Gtk.Image()
        icon.set_from_stock(Gtk.STOCK_INFO, Gtk.IconSize.BUTTON)
        help_button.add(icon)
        help_button.connect("clicked", self._help_button_clicked)
        self.pack_start(help_button, False, True, 0)
        help_button.show_all()

        self.entry.connect("changed", lambda x: self.emit("changed"))

    def grab_focus(self):
        self.entry.grab_focus()

    def get_filter_string(self):
        return self.entry.get_text()

    def set_filter_string(self, filter_string):
        return self.entry.set_text(filter_string)

    def set_information_text(self, text):
        self.information_label.set_text(text)

    def _help_button_clicked(self, button):
        hint_window = HintWindow(HELP_TEXT)
        hint_window.show_all()

HELP_TEXT = _("""\
在搜索框中输入文本将执行一次 <b>关键字搜索</b> - \
搜索字符串会与主机的所有相关信息进行匹配。

为了细化搜索，你可以使用 <b>运算符</b> 仅搜索主机中的 \
特定字段。大多数运算符都有对应的简写形式，已列出如下。 \

<b>target: (t:)</b> - 用户提供的目标，或反向 DNS（rDNS）解析结果。
<b>os:</b> - 所有与操作系统相关的字段。
<b>open: (op:)</b> - 扫描中发现的开放端口。
<b>closed: (cp:)</b> - 扫描中发现的关闭端口。
<b>filtered: (fp:)</b> - 扫描中发现的被过滤端口。
<b>unfiltered: (ufp:)</b> - 扫描中发现的未过滤端口（例如使用 ACK 扫描）。
<b>open|filtered: (ofp:)</b> - 处于 \"open|filtered\" 状态的端口。
<b>closed|filtered: (cfp:)</b> - 处于 \"closed|filtered\" 状态的端口。
<b>service: (s:)</b> - 所有与服务相关的字段。
<b>inroute: (ir:)</b> - 匹配扫描结果中 traceroute 输出里的路由器。

""")
