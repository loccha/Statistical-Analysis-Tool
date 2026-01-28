import tkinter as tk

# ToolTip class that displays a tooltip when hovering over a widget
# Implementation adapted from: https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter

class ToolTip:
    """
    Displays a tooltip popup on widget hover with configurable delay.

    Args:
            widget: tkinter widget to attach tooltip to
            text (str): tooltip text to display
            delay (int): milliseconds before tooltip appears (default 500)
    """
       
        
    def __init__(self, widget, text, delay=500):
        
        # Initialize tooltip with widget, text content, and hover delay
        self.delay = delay #ms
        self.widget = widget
        self.text = text
        
        self.id = None
        self.tw = None

        # Bind mouse events to show/hide tooltip
        self.widget.bind("<Enter>", self._enter)
        self.widget.bind("<Leave>", self._leave)
        self.widget.bind("<ButtonPress>", self._leave)
    

    def _enter(self, event=None):
        # Schedule tooltip display when mouse enters widget
        self._schedule()
    

    def _leave(self, event=None):
        # Cancel scheduled display and hide tooltip when mouse leaves or clicks
        self._unschedule()
        self._hidetip()


    def _schedule(self):
        # Schedule tooltip to appear after delay period
        self._unschedule()
        self.id=self.widget.after(self.delay, self._show)


    def _unschedule(self):
        # Cancel any pending tooltip display
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)


    def _show(self, event=None):
        # Create and display tooltip window under the widget
        x = self.widget.winfo_rootx()
        y = self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(
            self.tw, text=self.text, 
            justify='left', 
            background='#ffffff', 
            relief='solid', 
            borderwidth=1, 
            )
        label.pack(ipadx=1)
    

    def _hidetip(self):
        # Destroy tooltip window if it exists
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()