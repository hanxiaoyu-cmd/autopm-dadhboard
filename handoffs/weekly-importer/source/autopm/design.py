"""Desktop design tokens and privately bundled upright Noto Sans SC font."""
from pathlib import Path
import sys
import tkinter as tk

C = dict(bg="#FFFFFF", card="#FFFFFF", ink="#182B49", muted="#697B8D", line="#E8EDF3",
         nav="#FFFFFF", nav_hover="#F3F7FF", nav_text="#526273", blue="#246BFE",
         blue_light="#E8F0FF", cyan="#246BFE", green="#0F8F65", amber="#B7791F", red="#C2414B")
FONT_PATH = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent)) / "assets/fonts/NotoSansSC-VF.ttf"


def load_private_font():
    if sys.platform == "win32" and FONT_PATH.is_file():
        import ctypes
        return bool(ctypes.windll.gdi32.AddFontResourceExW(str(FONT_PATH), 0x10, None))
    return False


# Register before Tk creates its font cache; no installation or network needed.
FONT_LOADED = load_private_font()
FONT = "Noto Sans SC" if FONT_LOADED else "Microsoft YaHei UI"


def rounded_image(master, fill, border, size=24, radius=7):
    """Small transparent nine-slice image; native ttk keeps focus/state behavior."""
    image = tk.PhotoImage(master=master, width=size, height=size)
    for y in range(size):
        for x in range(size):
            dx = max(radius - x - .5, x + .5 - (size-radius), 0)
            dy = max(radius - y - .5, y + .5 - (size-radius), 0)
            if dx*dx + dy*dy <= radius*radius:
                edge = x == 0 or y == 0 or x == size-1 or y == size-1 or dx*dx + dy*dy > (radius-1)**2
                image.put(border if edge else fill, (x, y))
    return image


def rounded_buttons(style, root):
    images = []
    for name, border, text in (
        ("TButton", "#CDDAE7", C["ink"]),
        ("Primary.TButton", "#A7C4EC", C["blue"]),
        ("Nav.TButton", "#E1E8EF", C["nav_text"]),
        ("NavActive.TButton", "#ABC7EF", C["blue"]),
    ):
        normal = glass_image(root, border)
        active = glass_image(root, "#8FB5E7", bottom="#EAF2FC")
        pressed = glass_image(root, "#7BA6DF", bottom="#E1EBF8", pressed=True)
        disabled = glass_image(root, "#E1E7EF", bottom="#F1F4F7")
        focus = glass_image(root, C["blue"])
        images.extend((normal, active, pressed, disabled, focus))
        element = name + ".round"
        style.element_create(element, "image", normal, ("disabled", disabled),
                             ("pressed", pressed), ("focus", focus), ("active", active),
                             border=(13, 18, 13, 18), padding=0, sticky="nswe")
        style.layout(name, [(element, {"sticky": "nswe", "children": [
            ("Button.padding", {"sticky": "nswe", "children": [("Button.label", {"sticky": "nswe"})]})]})])
        backing = C["nav"] if name.startswith("Nav") else "white"
        style.configure(name, background=backing, foreground=text, padding=(17, 11), font=(FONT, -16), anchor="center")
        style.map(name, background=[("!disabled", backing), ("disabled", backing)])
        style.map(name, foreground=[("disabled", "#8A9AAD"), ("!disabled", text)])
    style.configure("Nav.TButton", anchor="w", padding=(17, 14))
    style.configure("NavActive.TButton", anchor="w", padding=(17, 14))
    return images


def glass_image(master, border, bottom="#F0F5FA", pressed=False):
    """White glass surface: rounded rim, reflected upper light, soft lower shadow."""
    size, radius = 40, 12
    image = tk.PhotoImage(master=master, width=size, height=size)
    rgb = tuple(int(bottom[i:i+2], 16) for i in (1, 3, 5))
    for y in range(size):
        for x in range(size):
            dx = max(radius-x-.5, x+.5-(size-radius), 0)
            dy = max(radius-y-.5, y+.5-(size-2-radius), 0)
            distance = dx*dx + dy*dy
            if distance <= radius*radius and y < size-2:
                edge = x in (0, size-1) or y in (0, size-3) or distance > (radius-1)**2
                t = (y/(size-3))**1.7
                color = '#%02x%02x%02x' % tuple(round(255+(v-255)*t) for v in rgb)
                if pressed and y < 3:
                    color = "#E9F0F8"
                image.put(border if edge else color, (x, y))
            elif y >= size-3 and radius <= x < size-radius:
                image.put("#E7EDF4" if y == size-2 else "#F5F7FA", (x, y))
    return image
