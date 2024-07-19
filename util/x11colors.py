from PyQt6.QtGui import QColor


class X11Colors:
    # Dictionary of the X11 colors, filled as requested.
    x11colors = {}

    @staticmethod
    def get_color(name, alpha=255):
        color = X11Colors.get_color_by_name(name)
        if color is not None:
            color.setAlpha(alpha)
        return color

    @staticmethod
    def get_color_by_name(name):
        if name is None:
            return None
        name = name.lower()

        color = X11Colors.x11colors.get(name)
        if color is None:
            if name == "alice blue":
                color = QColor(240, 248, 255)
            elif name == "antique white":
                color = QColor(250, 235, 215)
            elif name == "aqua":
                color = QColor(0, 255, 255)
            elif name == "aquamarine":
                color = QColor(127, 255, 212)
            elif name == "azure":
                color = QColor(240, 255, 255)
            elif name == "beige":
                color = QColor(245, 245, 220)
            elif name == "bisque":
                color = QColor(255, 228, 196)
            elif name == "black":
                color = QColor(0, 0, 0)
            elif name == "blanched almond":
                color = QColor(255, 235, 205)
            elif name == "blue":
                color = QColor(0, 0, 255)
            elif name == "blue violet":
                color = QColor(138, 43, 226)
            elif name == "brown":
                color = QColor(165, 42, 42)
            elif name == "burlywood":
                color = QColor(222, 184, 135)
            elif name == "cadet blue":
                color = QColor(95, 158, 160)
            elif name == "chartreuse":
                color = QColor(127, 255, 0)
            elif name == "chocolate":
                color = QColor(210, 105, 30)
            elif name == "coral":
                color = QColor(255, 127, 80)
            elif name == "cornflower blue":
                color = QColor(100, 149, 237)
            elif name == "cornsilk":
                color = QColor(255, 248, 220)
            elif name == "crimson":
                color = QColor(220, 20, 60)
            elif name == "cyan":
                color = QColor(0, 255, 255)
            elif name == "dark blue":
                color = QColor(0, 0, 139)
            elif name == "dark cyan":
                color = QColor(0, 139, 139)
            elif name == "dark goldenrod":
                color = QColor(184, 134, 11)
            elif name == "dark gray":
                color = QColor(169, 169, 169)
            elif name == "dark green":
                color = QColor(0, 100, 0)
            elif name == "dark khaki":
                color = QColor(189, 183, 107)
            elif name == "dark magenta":
                color = QColor(139, 0, 139)
            elif name == "dark olive green":
                color = QColor(85, 107, 47)
            elif name == "dark orange":
                color = QColor(255, 140, 0)
            elif name == "dark orchid":
                color = QColor(153, 50, 204)
            elif name == "dark red":
                color = QColor(139, 0, 0)
            elif name == "dark salmon":
                color = QColor(233, 150, 122)
            elif name == "dark sea green":
                color = QColor(143, 188, 143)
            elif name == "dark slate blue":
                color = QColor(72, 61, 139)
            elif name == "dark slate gray":
                color = QColor(47, 79, 79)
            elif name == "dark turquoise":
                color = QColor(0, 206, 209)
            elif name == "dark violet":
                color = QColor(148, 0, 211)
            elif name == "deep pink":
                color = QColor(255, 20, 147)
            elif name == "deep sky blue":
                color = QColor(0, 191, 255)
            elif name == "dim gray":
                color = QColor(105, 105, 105)
            elif name == "dodger blue":
                color = QColor(30, 144, 255)
            elif name == "firebrick":
                color = QColor(178, 34, 34)
            elif name == "floral white":
                color = QColor(255, 250, 240)
            elif name == "forest green":
                color = QColor(34, 139, 34)
            elif name == "fuchsia":
                color = QColor(255, 0, 255)
            elif name == "gainsboro":
                color = QColor(220, 220, 220)
            elif name == "ghost white":
                color = QColor(248, 248, 255)
            elif name == "gold":
                color = QColor(255, 215, 0)
            elif name == "goldenrod":
                color = QColor(218, 165, 32)
            elif name == "gray":
                color = QColor(128, 128, 128)
            elif name == "green":
                color = QColor(0, 128, 0)
            elif name == "green yellow":
                color = QColor(173, 255, 47)
            elif name == "honeydew":
                color = QColor(240, 255, 240)
            elif name == "hot pink":
                color = QColor(255, 105, 180)
            elif name == "indian red":
                color = QColor(205, 92, 92)
            elif name == "indigo":
                color = QColor(75, 0, 130)
            elif name == "ivory":
                color = QColor(255, 255, 240)
            elif name == "khaki":
                color = QColor(240, 230, 140)
            elif name == "lavender":
                color = QColor(230, 230, 250)
            elif name == "lavender blush":
                color = QColor(255, 240, 245)
            elif name == "lawn green":
                color = QColor(124, 252, 0)
            elif name == "lemon chiffon":
                color = QColor(255, 250, 205)
            elif name == "light blue":
                color = QColor(173, 216, 230)
            elif name == "light coral":
                color = QColor(240, 128, 128)
            elif name == "light cyan":
                color = QColor(224, 255, 255)
            elif name == "light goldenrod yellow":
                color = QColor(250, 250, 210)
            elif name == "light green":
                color = QColor(144, 238, 144)
            elif name == "light grey":
                color = QColor(211, 211, 211)
            elif name == "light pink":
                color = QColor(255, 182, 193)
            elif name == "light salmon":
                color = QColor(255, 160, 122)
            elif name == "light sea green":
                color = QColor(32, 178, 170)
            elif name == "light sky blue":
                color = QColor(135, 206, 250)
            elif name == "light slate gray":
                color = QColor(119, 136, 153)
            elif name == "light steel blue":
                color = QColor(176, 196, 222)
            elif name == "light yellow":
                color = QColor(255, 255, 224)
            elif name == "lime":
                color = QColor(0, 255, 0)
            elif name == "lime green":
                color = QColor(50, 205, 50)
            elif name == "linen":
                color = QColor(250, 240, 230)
            elif name == "magenta":
                color = QColor(255, 0, 255)
            elif name == "maroon":
                color = QColor(128, 0, 0)
            elif name == "medium aquamarine":
                color = QColor(102, 205, 170)
            elif name == "medium blue":
                color = QColor(0, 0, 205)
            elif name == "medium orchid":
                color = QColor(186, 85, 211)
            elif name == "medium purple":
                color = QColor(147, 112, 219)
            elif name == "medium sea green":
                color = QColor(60, 179, 113)
            elif name == "medium slate blue":
                color = QColor(123, 104, 238)
            elif name == "medium spring green":
                color = QColor(0, 250, 154)
            elif name == "medium turquoise":
                color = QColor(72, 209, 204)
            elif name == "medium violet red":
                color = QColor(199, 21, 133)
            elif name == "midnight blue":
                color = QColor(25, 25, 112)
            elif name == "mint cream":
                color = QColor(245, 255, 250)
            elif name == "misty rose":
                color = QColor(255, 228, 225)
            elif name == "moccasin":
                color = QColor(255, 228, 181)
            elif name == "navajo white":
                color = QColor(255, 222, 173)
            elif name == "navy":
                color = QColor(0, 0, 128)
            elif name == "old lace":
                color = QColor(253, 245, 230)
            elif name == "olive":
                color = QColor(128, 128, 0)
            elif name == "olive drab":
                color = QColor(107, 142, 35)
            elif name == "orange":
                color = QColor(255, 165, 0)
            elif name == "orange red":
                color = QColor(255, 69, 0)
            elif name == "orchid":
                color = QColor(218, 112, 214)
            elif name == "pale goldenrod":
                color = QColor(238, 232, 170)
            elif name == "pale green":
                color = QColor(152, 251, 152)
            elif name == "pale turquoise":
                color = QColor(175, 238, 238)
            elif name == "pale violet red":
                color = QColor(219, 112, 147)
            elif name == "papaya whip":
                color = QColor(255, 239, 213)
            elif name == "peach puff":
                color = QColor(255, 218, 185)
            elif name == "peru":
                color = QColor(205, 133, 63)
            elif name == "pink":
                color = QColor(255, 192, 203)
            elif name == "plum":
                color = QColor(221, 160, 221)
            elif name == "powder blue":
                color = QColor(176, 224, 230)
            elif name == "purple":
                color = QColor(128, 0, 128)
            elif name == "red":
                color = QColor(255, 0, 0)
            elif name == "rosy brown":
                color = QColor(188, 143, 143)
            elif name == "royal blue":
                color = QColor(65, 105, 225)
            elif name == "saddle brown":
                color = QColor(139, 69, 19)
            elif name == "salmon":
                color = QColor(250, 128, 114)
            elif name == "sandy brown":
                color = QColor(244, 164, 96)
            elif name == "sea green":
                color = QColor(46, 139, 87)
            elif name == "seashell":
                color = QColor(255, 245, 238)
            elif name == "sienna":
                color = QColor(160, 82, 45)
            elif name == "silver":
                color = QColor(192, 192, 192)
            elif name == "sky blue":
                color = QColor(135, 206, 235)
            elif name == "slate blue":
                color = QColor(106, 90, 205)
            elif name == "slate gray":
                color = QColor(112, 128, 144)
            elif name == "snow":
                color = QColor(255, 250, 250)
            elif name == "spring green":
                color = QColor(0, 255, 127)
            elif name == "steel blue":
                color = QColor(70, 130, 180)
            elif name == "tan":
                color = QColor(210, 180, 140)
            elif name == "teal":
                color = QColor(0, 128, 128)
            elif name == "thistle":
                color = QColor(216, 191, 216)
            elif name == "tomato":
                color = QColor(255, 99, 71)
            elif name == "turquoise":
                color = QColor(64, 224, 208)
            elif name == "violet":
                color = QColor(238, 130, 238)
            elif name == "wheat":
                color = QColor(245, 222, 179)
            elif name == "white":
                color = QColor(255, 255, 255)
            elif name == "white smoke":
                color = QColor(245, 245, 245)
            elif name == "yellow":
                color = QColor(255, 255, 0)
            elif name == "yellow green":
                color = QColor(154, 205, 50)

            if color is not None:
                X11Colors.x11colors[name] = color

        return color
