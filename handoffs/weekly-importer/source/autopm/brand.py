"""AutoPM identity: original AP monogram and a shared workflow icon family."""
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageTk

ASSET_ROOT = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent.parent))/'assets'/'brand'
TITLE = 'AutoPM · 项目同步工作台'
NAVY = '#182B49'
BLUE = '#246BFE'


def monogram(size=256):
    scale = 4
    image = Image.new('RGBA', (256*scale, 256*scale))
    d = ImageDraw.Draw(image)
    def points(values):
        return [(x*scale, y*scale) for x, y in values]
    d.rounded_rectangle((4*scale, 4*scale, 252*scale, 252*scale), radius=58*scale, fill=NAVY)
    # A joins the upright of P: one continuous project-to-progress signature.
    d.line(points([(45, 178), (83, 75), (99, 75), (137, 178)]), fill='white', width=14*scale, joint='curve')
    d.line(points([(62, 140), (113, 140)]), fill='white', width=14*scale)
    d.line(points([(143, 178), (143, 75), (179, 75)]), fill='white', width=14*scale, joint='curve')
    d.arc((145*scale, 75*scale, 213*scale, 139*scale), -90, 90, fill='white', width=14*scale)
    d.line(points([(143, 139), (179, 139)]), fill='white', width=14*scale)
    d.ellipse((185*scale, 163*scale, 208*scale, 186*scale), fill='#79A9FF')
    return image.resize((size, size), Image.Resampling.LANCZOS)


def glyph(name, size=28, color=BLUE):
    """24-unit hand-drawn vector geometry; all icons share stroke and spacing."""
    scale = 4
    image = Image.new('RGBA', (size*scale, size*scale))
    d = ImageDraw.Draw(image)
    unit = size*scale/24
    def line(points, fill=color, width=1.55):
        pts = [(round(x*unit), round(y*unit)) for x, y in points]
        d.line(pts, fill=fill, width=max(1, round(width*unit)), joint='curve')
        r = width*unit/2
        for x, y in (pts[0], pts[-1]):
            d.ellipse((x-r, y-r, x+r, y+r), fill=fill)
    def dot(x, y, r=1.7, fill=color):
        d.ellipse(((x-r)*unit, (y-r)*unit, (x+r)*unit, (y+r)*unit), fill=fill)
    if name == 'report':
        line([(14, 3), (5, 3), (5, 21), (19, 21), (19, 8), (14, 3), (14, 8), (19, 8)])
        line([(8, 12), (15, 12)])
        line([(8, 16), (11, 16)])
        dot(15.5, 16.5, 1.2)
    elif name == 'folder':
        line([(3, 8), (3, 5), (9, 5), (12, 8), (21, 8), (19, 20), (3, 20), (3, 8), (21, 8)])
        line([(7, 12), (16, 12)])
    elif name == 'connection':
        line([(6, 6), (12, 12), (18, 6)])
        line([(12, 12), (12, 19)])
        for x, y in ((6, 5), (18, 5), (12, 19)):
            dot(x, y, 2.5)
        dot(12, 12, 2, NAVY)
    elif name == 'tracker':
        line([(4, 3), (20, 3), (20, 21), (4, 21), (4, 3)])
        line([(4, 9), (20, 9)])
        line([(10, 9), (10, 21)])
        line([(4, 15), (20, 15)])
        line([(8, 6), (16, 6)])
    elif name == 'sync':
        line([(3, 5), (9, 5), (9, 19), (3, 19), (3, 5)])
        line([(5, 9), (7, 9)])
        line([(5, 12), (7, 12)])
        line([(11, 12), (17, 12), (17, 6), (21, 6)])
        line([(17, 12), (21, 12)])
        line([(17, 12), (17, 18), (21, 18)])
        for y in (6, 12, 18):
            dot(21, y, 1.5)
    else:
        raise ValueError(f'Unknown AutoPM icon: {name}')
    return image.resize((size, size), Image.Resampling.LANCZOS)


def window_identity(root):
    root.title(TITLE)
    root._brand_icons = [ImageTk.PhotoImage(monogram(size), master=root) for size in (16, 32, 48, 64)]
    root.iconphoto(True, *root._brand_icons)
    root._caption_attributes = {}

    def style_caption(event=None):
        if event is not None and event.widget != root:
            return
        if sys.platform != 'win32':
            return
        import ctypes
        from ctypes import wintypes
        user32, dwm = ctypes.windll.user32, ctypes.windll.dwmapi
        user32.GetParent.argtypes = [wintypes.HWND]
        user32.GetParent.restype = wintypes.HWND
        dwm.DwmSetWindowAttribute.argtypes = [wintypes.HWND, wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD]
        hwnd = user32.GetParent(root.winfo_id()) or root.winfo_id()
        # Per-window appearance only; preserve native resize, snap and caption buttons.
        for attr, color in ((20, 0), (33, 2), (34, 0xE9E5E0), (35, 0xFFFFFF), (36, 0x492B18)):
            value = wintypes.DWORD(color)
            result = dwm.DwmSetWindowAttribute(hwnd, attr, ctypes.byref(value), ctypes.sizeof(value))
            root._caption_attributes[str(attr)] = int(result)
    root.bind('<Map>', style_caption, add='+')
    root.after_idle(style_caption)


def export_assets():
    ASSET_ROOT.mkdir(parents=True, exist_ok=True)
    mark = monogram(256)
    mark.save(ASSET_ROOT/'autopm.png')
    mark.save(ASSET_ROOT/'autopm.ico', sizes=[(s, s) for s in (16, 24, 32, 48, 64, 128, 256)])
    for name in ('report', 'folder', 'connection', 'tracker', 'sync'):
        glyph(name, 96).save(ASSET_ROOT/f'{name}.png')
    (ASSET_ROOT/'autopm.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
<title>AutoPM — AP project-to-progress monogram</title>
<rect x="4" y="4" width="248" height="248" rx="58" fill="#182B49"/>
<g fill="none" stroke="white" stroke-width="14" stroke-linejoin="round">
<path d="M45 178L83 75H99L137 178M62 140H113"/>
<path d="M143 178V75H179A32 32 0 0 1 179 139H143"/>
</g><circle cx="196.5" cy="174.5" r="11.5" fill="#79A9FF"/></svg>''', encoding='utf-8')


if __name__ == '__main__':
    export_assets()
