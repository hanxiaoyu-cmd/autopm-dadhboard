"""Composited translucent surfaces and finite, event-driven desktop motion.

Tk does not support backdrop-filter. Every surface samples the same application
backdrop before alpha compositing, keeping text opaque and the desktop private.
"""
from __future__ import annotations

import itertools
import math
import sys
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageTk

from .design import C, FONT


def motion_allowed():
    if sys.platform == 'win32':
        import ctypes
        enabled = ctypes.c_int(1)
        if ctypes.windll.user32.SystemParametersInfoW(0x1042, 0, ctypes.byref(enabled), 0):
            return bool(enabled.value)
    return True


def backdrop(size):
    """White canvas with a barely visible cool halo at the outer edge."""
    w, h = size
    small = Image.new('RGB', (max(1, w//4), max(1, h//4)), '#FFFFFF')
    sw, sh = small.size
    small = small.convert('RGBA')
    for cx, cy, rx, ry, color in (
        (1.03, .10, .26, .32, (213, 230, 253, 35)),
        (.02, .95, .22, .30, (224, 236, 251, 23)),
    ):
        mask = Image.new('L', small.size)
        ImageDraw.Draw(mask).ellipse(((cx-rx)*sw, (cy-ry)*sh, (cx+rx)*sw, (cy+ry)*sh), fill=color[3])
        glow = Image.new('RGBA', small.size, color[:3])
        glow.putalpha(mask.filter(ImageFilter.GaussianBlur(max(14, sw*.11))))
        small = Image.alpha_composite(small, glow)
    return small.resize(size, Image.Resampling.BICUBIC)


def surface(background, *, hover=0., pressed=0., primary=False, disabled=False,
            cursor=None, ripple=None, panel=False):
    """Alpha glass over actual underlying pixels, with anti-aliased edges."""
    w, h = background.size
    if panel:
        # The atmosphere is already diffuse. Avoid blurring large panels again
        # during resize; supersample only the edge masks, not the RGBA surface.
        mask = Image.new('L', (w*2, h*2))
        ImageDraw.Draw(mask).rounded_rectangle((2, 2, w*2-3, h*2-3), radius=44, fill=255)
        mask = mask.resize((w, h), Image.Resampling.LANCZOS)
        inner = Image.new('L', (w*2, h*2))
        ImageDraw.Draw(inner).rounded_rectangle((4, 4, w*2-5, h*2-5), radius=42, fill=255)
        edge = ImageChops.subtract(mask, inner.resize((w, h), Image.Resampling.LANCZOS))
        transmitted = Image.blend(background.convert('RGBA'), Image.new('RGBA', (w, h), 'white'), .27)
        image = Image.composite(transmitted, background, mask)
        image.paste('#E8EDF4', (0, 0, w, h), edge)
        return image
    scale = 2
    image = background.convert('RGBA').resize((w*scale, h*scale), Image.Resampling.BICUBIC)
    W, H = image.size
    inset = (1 if panel else 4 + pressed*2) * scale
    lift = 0 if panel else hover*1.5*scale*(1-pressed)
    box = (inset, inset-lift, W-inset-1, H-inset-lift-1)
    radius = min((22 if panel else 16)*scale, (H-2*inset)/2)
    if radius < 1:
        return background.copy()
    mask = Image.new('L', image.size)
    ImageDraw.Draw(mask).rounded_rectangle(box, radius=radius, fill=255)
    shadow = Image.new('RGBA', image.size)
    ImageDraw.Draw(shadow).rounded_rectangle((box[0], box[1]+3*scale, box[2], box[3]+3*scale), radius=radius,
                                             fill=(50, 75, 124, 15+int(hover*12)))
    image = Image.alpha_composite(image, shadow.filter(ImageFilter.GaussianBlur(3*scale)))
    # Transmit most of the backdrop, with local diffusion through the glass.
    transmitted = image.filter(ImageFilter.GaussianBlur((5 if panel else 2)*scale))
    alpha = .27 if panel else (.12 + hover*.14 + pressed*.10)
    if disabled:
        alpha = .08
    transmitted = Image.blend(transmitted, Image.new('RGBA', image.size, 'white'), alpha)
    tint = Image.new('RGBA', image.size)
    td = ImageDraw.Draw(tint)
    for y in range(H):
        reflection = max(0, 1-y/max(1, H*.55))**2
        td.line((0, y, W, y), fill=(255, 255, 255, int(reflection*(34 if panel else 48))))
    transmitted = Image.alpha_composite(transmitted, tint)
    if cursor is not None and hover > .01 and not disabled:
        light = Image.new('RGBA', image.size)
        x, y = cursor[0]*scale, cursor[1]*scale
        ImageDraw.Draw(light).ellipse((x-36*scale, y-24*scale, x+36*scale, y+24*scale),
                                      fill=(255, 255, 255, int(90*hover)))
        transmitted = Image.alpha_composite(transmitted, light.filter(ImageFilter.GaussianBlur(15*scale)))
    if ripple is not None and not disabled:
        x, y, progress = ripple
        light = Image.new('RGBA', image.size)
        r = max(w, h)*progress*scale
        ImageDraw.Draw(light).ellipse((x*scale-r, y*scale-r, x*scale+r, y*scale+r),
                                      fill=(255, 255, 255, int(75*(1-progress))))
        transmitted = Image.alpha_composite(transmitted, light)
    image.paste(transmitted, (0, 0), mask)
    rim = Image.new('RGBA', image.size)
    rd = ImageDraw.Draw(rim)
    rd.rounded_rectangle(box, radius=radius, outline=(255, 255, 255, 180 if disabled else 240), width=scale)
    inner = (box[0]+scale, box[1]+scale, box[2]-scale, box[3]-scale)
    rd.rounded_rectangle(inner, radius=max(1, radius-scale), outline=(86, 124, 181, 20 if not primary else 62), width=scale)
    image = Image.alpha_composite(image, rim)
    return image.resize((w, h), Image.Resampling.LANCZOS)


class GlassLabel(tk.Label):
    """Keep native label sizing/text variables, paint text on a sampled backdrop."""
    def __init__(self, master, **kwargs):
        self._canvas = None
        self._variable = kwargs.get('textvariable')
        self._trace = None
        self._repaint_timer = None
        super().__init__(master, **kwargs)
        self._canvas = tk.Canvas(self, bd=0, highlightthickness=0, bg=self.cget('bg'))
        self._canvas._glass_backdrop = True
        self._canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self._image_item = self._canvas.create_image(0, 0, anchor='nw')
        self._text_item = self._canvas.create_text(0, 0, text='')
        self.bind('<Configure>', lambda _: self._paint(), add='+')
        self.bind('<Map>', lambda _: self._paint(), add='+')
        self.bind('<Destroy>', self._destroy, add='+')
        if isinstance(self._variable, tk.Variable):
            self._trace = self._variable.trace_add('write', self._changed)

    def _changed(self, *_):
        if self._repaint_timer is None:
            self._repaint_timer = self.after_idle(self._paint)

    def _destroy(self, event):
        if event.widget == self:
            if self._repaint_timer is not None:
                self.after_cancel(self._repaint_timer)
                self._repaint_timer = None
            if self._trace is not None:
                self._variable.trace_remove('write', self._trace)
                self._trace = None
            # Release Tk-backed objects on the UI thread, before cyclic GC can
            # encounter a destroyed view from a background worker.
            self._variable = None
            self._image = None

    def configure(self, cnf=None, **kwargs):
        result = super().configure(cnf, **kwargs)
        if self._canvas is not None and (kwargs or isinstance(cnf, dict)):
            self._paint()
        return result

    config = configure

    def _paint(self):
        self._repaint_timer = None
        if self._canvas is None or not self.winfo_ismapped():
            return
        w, h = self.winfo_width(), self.winfo_height()
        if min(w, h) < 2:
            return
        scene = getattr(self.winfo_toplevel(), '_glass_scene', None)
        bg = self.cget('bg')
        signature = (w, h, self.cget('text'), str(self.cget('font')), self.cget('fg'), bg,
                     str(self.cget('anchor')), str(self.cget('wraplength')), getattr(scene, 'revision', 0))
        if signature == getattr(self, '_paint_signature', None):
            return
        self._paint_signature = signature
        eligible = bg.lower() in ('white', '#ffffff', C['bg'].lower(), C['nav'].lower())
        background = scene.sample(self) if scene and eligible else Image.new('RGBA', (w, h), bg)
        self._image = ImageTk.PhotoImage(background, master=self)
        self._canvas.itemconfigure(self._image_item, image=self._image)
        anchor = str(self.cget('anchor'))
        px, py = self.winfo_pixels(self.cget('padx')), self.winfo_pixels(self.cget('pady'))
        x = px if anchor in ('w', 'nw', 'sw') else w-px if anchor in ('e', 'ne', 'se') else w/2
        y = py if anchor in ('n', 'nw', 'ne') else h-py if anchor in ('s', 'sw', 'se') else h/2
        self._canvas.coords(self._text_item, x, y)
        self._canvas.itemconfigure(self._text_item, text=self.cget('text'), font=self.cget('font'),
                                    fill=self.cget('fg'), anchor=anchor, justify=self.cget('justify'),
                                    width=self.winfo_pixels(self.cget('wraplength')))


class GlassButton(ttk.Button):
    """Native ttk activation and disabled semantics; only the surface animates."""
    ids = itertools.count()

    def __init__(self, master, **kwargs):
        self._base_style = kwargs.pop('style', 'TButton')
        self._uid = f'Liquid{next(self.ids)}'
        self._timer = None
        self._hover = self._press = self._target = 0.
        self._cursor = (30, 20)
        self._ripple_started = None
        self._ready = False
        super().__init__(master, **kwargs)
        self._photo = ImageTk.PhotoImage(Image.new('RGBA', (2, 2)), master=self)
        self._image_size = (2, 2)
        self._style = ttk.Style(self)
        self._element = self._uid + '.surface'
        self._style.element_create(self._element, 'image', str(self._photo), border=0,
                                   padding=0, width=1, height=1, sticky='nswe')
        self._ready = True
        self._set_style(self._base_style)
        for event, callback in (('<Enter>', self._enter), ('<Leave>', self._leave),
                                ('<Motion>', self._move), ('<ButtonPress-1>', self._down),
                                ('<ButtonRelease-1>', self._up), ('<FocusIn>', self._focus),
                                ('<FocusOut>', self._focus), ('<Configure>', self._size),
                                ('<Map>', self._size), ('<Unmap>', self._unmap), ('<Destroy>', self._destroy)):
            self.bind(event, callback, add='+')

    def _set_style(self, base):
        self._base_style = base
        name = self._uid + '.' + base
        self._style.layout(name, [(self._element, {'sticky': 'nswe', 'children': [
            ('Button.padding', {'sticky': 'nswe', 'children': [('Button.label', {'sticky': 'nswe'})]})]})])
        nav = base.startswith('Nav')
        self._style.configure(name, font=(FONT, -17), padding=(18, 12 if nav else 11),
                              anchor='w' if nav else 'center')
        self._style.map(name, foreground=[('disabled', '#8C9BAF'), ('!disabled', C['blue'] if self._primary else C['ink'])])
        super().configure(style=name)

    @property
    def _primary(self):
        return self._base_style in ('Primary.TButton', 'NavActive.TButton', 'Link.TButton')

    def configure(self, cnf=None, **kwargs):
        if not self._ready or (cnf is None and not kwargs) or isinstance(cnf, str):
            return super().configure(cnf, **kwargs)
        options = {**(cnf or {}), **kwargs}
        if 'style' in options:
            self._set_style(options.pop('style'))
        result = super().configure(**options) if options else None
        if self.instate(['disabled']):
            self._cancel()
            self._hover = self._press = self._target = 0.
            self._ripple_started = None
        self._paint()
        return result

    config = configure

    def _scene(self):
        return getattr(self.winfo_toplevel(), '_glass_scene', None)

    def _moving(self):
        scene = self._scene()
        return scene.enabled if scene else False

    def _cancel(self):
        if self._timer is not None:
            self.after_cancel(self._timer)
            self._timer = None

    def _destroy(self, event):
        if event.widget == self:
            self._cancel()
            self._photo = None

    def _unmap(self, _):
        self._cancel()
        self._hover = self._target = self._press = 0.
        self._ripple_started = None

    def _enter(self, _):
        if not self.instate(['disabled']):
            self._target = 1.
            self._start()

    def _leave(self, _):
        self._target = self._press = 0.
        self._start()

    def _move(self, event):
        self._cursor = (event.x, event.y)
        if self._timer is None and not self.instate(['disabled']):
            self._start()

    def _down(self, event):
        if not self.instate(['disabled']):
            self._cursor = (event.x, event.y)
            self._press = 1.
            self._paint()

    def _up(self, _):
        self._press = 0.
        if not self.instate(['disabled']) and self._moving():
            self._ripple_started = time.monotonic()
        self._start()

    def _focus(self, _):
        self._paint()

    def _size(self, _):
        self._paint()

    def _start(self):
        if not self.winfo_ismapped():
            return
        if not self._moving():
            self._cancel()
            self._hover = self._target
            self._ripple_started = None
            self._paint()
        elif self._timer is None:
            self._last_tick = time.monotonic()
            self._timer = self.after(16, self._tick)

    def _tick(self):
        self._timer = None
        now = time.monotonic()
        delta = min(.1, now-self._last_tick)
        self._last_tick = now
        self._hover += (self._target-self._hover)*(1-math.exp(-delta/0.045))
        if abs(self._target-self._hover) < .01:
            self._hover = self._target
        if self._ripple_started is not None and now-self._ripple_started >= .28:
            self._ripple_started = None
        self._paint()
        if self._hover != self._target or self._ripple_started is not None:
            self._timer = self.after(16, self._tick)

    def _paint(self):
        if not self._ready or not self.winfo_ismapped():
            return
        w, h = self.winfo_width(), self.winfo_height()
        if w < 8 or h < 8:
            return
        scene = self._scene()
        signature = (w, h, round(self._hover, 4), self._press, self._primary, self.instate(['disabled']),
                     self.instate(['focus']), self._cursor if self._hover else None,
                     getattr(scene, 'revision', 0), time.monotonic() if self._ripple_started is not None else None)
        if signature == getattr(self, '_paint_signature', None):
            return
        self._paint_signature = signature
        background = scene.sample(self) if scene else Image.new('RGBA', (w, h), C['bg'])
        ripple = None if self._ripple_started is None else (*self._cursor, min(1., (time.monotonic()-self._ripple_started)/.28))
        rendered = surface(background, hover=self._hover, pressed=self._press, primary=self._primary or self.instate(['focus']),
                           disabled=self.instate(['disabled']), cursor=self._cursor, ripple=ripple)
        if self._image_size != rendered.size:
            # Retain the Tcl image name referenced by the ttk element.
            self.tk.call(str(self._photo), 'configure', '-width', w, '-height', h)
            self._image_size = rendered.size
        self._photo.paste(rendered)


class GlassScene:
    def __init__(self, root):
        self.root = root
        root._glass_scene = self
        self.enabled = motion_allowed()
        self.image = None
        self.revision = 0
        self._pending = self._title_timer = None
        self._title_page = None
        self._painting = False
        root.bind('<Configure>', self._layout_changed, add='+')
        root.bind('<Map>', self._layout_changed, add='+')
        root.bind('<Destroy>', self._destroy, add='+')
        self.request()

    def _destroy(self, event):
        if event.widget == self.root:
            for timer in (self._pending, self._title_timer):
                if timer is not None:
                    self.root.after_cancel(timer)
            self._pending = self._title_timer = None
            self._title_page = None
            self.image = None

    def _layout_changed(self, event):
        if not self._painting and isinstance(event.widget, (tk.Tk, tk.Frame)):
            self.request()

    def request(self):
        if self._pending is not None:
            self.root.after_cancel(self._pending)
        self._pending = self.root.after(65, self.repaint)

    def _walk(self, parent, visible_pages=True):
        if getattr(parent, '_glass_exempt', False):
            return
        yield parent
        children = parent.winfo_children()
        if visible_pages and isinstance(parent, ttk.Notebook):
            children = [child for child in children if str(child) == str(parent.select())]
        for child in children:
            if not getattr(child, '_glass_backdrop', False) and not isinstance(child, tk.Toplevel):
                yield from self._walk(child, visible_pages)

    def sample(self, widget):
        w, h = max(1, widget.winfo_width()), max(1, widget.winfo_height())
        if self.image is None:
            return Image.new('RGBA', (w, h), C['bg'])
        x = widget.winfo_rootx()-self.root.winfo_rootx()
        y = widget.winfo_rooty()-self.root.winfo_rooty()
        return self.image.crop((x, y, x+w, y+h))

    def repaint(self):
        if self._pending is not None:
            self.root.after_cancel(self._pending)
            self._pending = None
        if not self.root.winfo_ismapped():
            return
        self._painting = True
        try:
            size = self.root.winfo_width(), self.root.winfo_height()
            if min(size) < 2:
                return
            if getattr(self, '_backdrop_size', None) != size:
                self._backdrop_size = size
                self._backdrop_image = backdrop(size)
            self.image = self._backdrop_image.copy()
            self.revision += 1
            widgets = [w for w in self._walk(self.root) if w.winfo_ismapped()]
            ox, oy = self.root.winfo_rootx(), self.root.winfo_rooty()
            for widget in widgets:
                if getattr(widget, '_glass_panel', False):
                    x, y = widget.winfo_rootx()-ox, widget.winfo_rooty()-oy
                    rendered = surface(self.sample(widget), panel=True)
                    self.image.paste(rendered, (x, y))
            for widget in widgets:
                if isinstance(widget, tk.Frame) and widget.winfo_height() > 5:
                    color = getattr(widget, '_glass_original_bg', widget.cget('bg'))
                    widget._glass_original_bg = color
                    if color.lower() not in ('white', '#ffffff', C['bg'].lower(), C['nav'].lower()):
                        continue
                    widget.configure(highlightthickness=0)
                    if not hasattr(widget, '_glass_layer'):
                        widget._glass_layer = tk.Label(widget, bd=0)
                        widget._glass_layer._glass_backdrop = True
                        widget._glass_layer.place(x=0, y=0, relwidth=1, relheight=1)
                        widget._glass_layer.lower()
                    widget._glass_image = ImageTk.PhotoImage(self.sample(widget), master=widget)
                    widget._glass_layer.configure(image=widget._glass_image)
                elif isinstance(widget, GlassLabel):
                    widget._paint()
                elif isinstance(widget, (tk.Label, tk.Canvas)):
                    color = getattr(widget, '_glass_original_bg', widget.cget('bg'))
                    widget._glass_original_bg = color
                    if color.lower() in ('white', '#ffffff', C['bg'].lower(), C['nav'].lower()):
                        crop = self.sample(widget)
                        rgb = crop.getpixel((crop.width//2, crop.height//2))[:3]
                        widget.configure(bg='#%02x%02x%02x' % rgb)
                elif isinstance(widget, GlassButton):
                    widget._paint()
                elif isinstance(widget, (ttk.Checkbutton, ttk.Radiobutton)):
                    rgb = self.sample(widget).getpixel((widget.winfo_width()//2, widget.winfo_height()//2))[:3]
                    color = '#%02x%02x%02x' % rgb
                    name = f'Glass{id(widget)}.' + ('TCheckbutton' if isinstance(widget, ttk.Checkbutton) else 'TRadiobutton')
                    style = ttk.Style(widget)
                    style.configure(name, background=color)
                    style.map(name, background=[('active', color), ('!active', color)])
                    widget.configure(style=name)
        finally:
            self._painting = False

    def set_motion(self, enabled):
        self.enabled = bool(enabled)
        self._finish_title()
        for widget in self._walk(self.root, visible_pages=False):
            if isinstance(widget, GlassButton):
                widget._cancel()
                widget._ripple_started = None
                widget._hover = widget._target
                widget._paint()

    def _finish_title(self):
        if self._title_timer is not None:
            self.root.after_cancel(self._title_timer)
            self._title_timer = None
        if self._title_page is not None:
            for widget, y, color in getattr(self._title_page, '_title_items', []):
                widget.place_configure(x=getattr(widget, '_title_x', 0), y=y)
                widget.configure(fg=color)
        self._title_page = None

    def enter_page(self, page):
        self._finish_title()
        self.request()
        if not self.enabled or not self.root.winfo_ismapped():
            return
        self._title_page = page
        started = time.monotonic()

        def step():
            self._title_timer = None
            t = min(1., (time.monotonic()-started)/.22)
            ease = 1-(1-t)**3
            for widget, y, color in getattr(page, '_title_items', []):
                widget.place_configure(x=getattr(widget, '_title_x', 0)+round(16*(1-ease)), y=y)
                rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
                widget.configure(fg='#%02x%02x%02x' % tuple(round(150+(v-150)*ease) for v in rgb))
            if t < 1:
                self._title_timer = self.root.after(16, step)
            else:
                self._finish_title()
        step()
