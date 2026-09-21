"""Verify transparency, native button safety and finite animation lifetimes."""
import time
import tkinter as tk
from tkinter import ttk
import unittest
from unittest.mock import Mock

from PIL import Image
from autopm.design import C
from autopm.glass import GlassButton, GlassLabel, GlassScene, surface


class MaterialTests(unittest.TestCase):
    def test_surface_transmits_underlying_color_instead_of_painting_white(self):
        blue = surface(Image.new('RGBA', (180, 48), '#80B8E8'))
        pink = surface(Image.new('RGBA', (180, 48), '#DDAACB'))
        b, p = blue.getpixel((90, 24)), pink.getpixel((90, 24))
        self.assertGreater(p[0]-b[0], 60)
        self.assertGreater(b[2]-p[2], 15)
        self.assertEqual(blue.getpixel((0, 0))[:3], (128, 184, 232))


class MotionTests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.geometry('520x330+4000+4000')
        self.errors = []
        self.root.report_callback_exception = lambda *args: self.errors.append(args)
        self.frame = tk.Frame(self.root, bg=C['bg'])
        self.frame.pack(fill='both', expand=True)
        self.called = Mock()
        self.button = GlassButton(self.frame, text='同步预览', command=self.called)
        self.button.pack(pady=20)
        self.scene = GlassScene(self.root)
        self.scene.enabled = True
        self.pump(.1)

    def tearDown(self):
        self.root.destroy()
        self.assertEqual(self.errors, [])

    def pump(self, seconds):
        until = time.monotonic()+seconds
        while time.monotonic() < until:
            self.root.update()
            time.sleep(.004)

    def test_hover_reaches_target_and_stops_scheduling(self):
        self.button._enter(None)
        self.pump(.05)
        self.assertGreater(self.button._hover, 0)
        self.assertLess(self.button._hover, 1)
        self.pump(.35)
        self.assertEqual(self.button._hover, 1)
        self.assertIsNone(self.button._timer)
        self.button._leave(None)
        self.pump(.4)
        self.assertEqual(self.button._hover, 0)
        self.assertIsNone(self.button._timer)

    def test_disable_during_animation_stops_motion_and_blocks_command(self):
        self.button._enter(None)
        self.pump(.04)
        self.button.configure(state='disabled')
        self.button.invoke()
        self.called.assert_not_called()
        self.assertIsNone(self.button._timer)
        self.assertEqual(self.button._hover, 0)
        self.button.configure(state='normal')
        self.button.invoke()
        self.called.assert_called_once()

    def test_reduced_motion_is_immediate_and_creates_no_animation_timer(self):
        self.scene.set_motion(False)
        self.button._enter(None)
        self.assertEqual(self.button._hover, 1)
        self.assertIsNone(self.button._timer)
        self.button._up(None)
        self.assertIsNone(self.button._ripple_started)

    def test_only_selected_notebook_page_contributes_to_glass(self):
        notebook = ttk.Notebook(self.frame)
        notebook.pack()
        first, second = tk.Frame(notebook), tk.Frame(notebook)
        notebook.add(first)
        notebook.add(second)
        notebook.select(first)
        self.pump(.03)
        widgets = list(self.scene._walk(self.root))
        self.assertIn(first, widgets)
        self.assertNotIn(second, widgets)

    def test_rapid_page_changes_finish_titles_and_clear_timer(self):
        pages = []
        for text in ('周报', '设置'):
            frame = tk.Frame(self.frame, height=45)
            frame.pack(fill='x')
            title = GlassLabel(frame, text=text, bg=C['bg'], fg=C['ink'])
            title.place(x=0, y=0)
            frame._title_items = [(title, 0, C['ink'])]
            pages.append(frame)
        self.scene.enter_page(pages[0])
        self.pump(.025)
        self.scene.enter_page(pages[1])
        self.pump(.35)
        self.assertIsNone(self.scene._title_timer)
        for page in pages:
            title = page._title_items[0][0]
            self.assertEqual(int(title.place_info()['x']), 0)
            self.assertEqual(title.cget('fg'), C['ink'])

    def test_label_variable_changes_repaint_displayed_text(self):
        value = tk.StringVar(value='就绪')
        label = GlassLabel(self.frame, textvariable=value, bg=C['bg'])
        label.pack()
        self.pump(.02)
        value.set('已生成 10 条预览')
        self.pump(.03)
        self.assertEqual(label._canvas.itemcget(label._text_item, 'text'), value.get())
        x, y = label._canvas.coords(label._text_item)
        self.assertAlmostEqual(x, label.winfo_width()/2)
        self.assertAlmostEqual(y, label.winfo_height()/2)


if __name__ == '__main__':
    unittest.main()
