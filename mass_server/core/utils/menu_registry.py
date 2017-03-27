from collections import OrderedDict

_menu_links = OrderedDict()


class MenuRegistry:
    def registerMenuLink(title, url):
        _menu_links[title] = url

    def getMenuLinks():
        return _menu_links
