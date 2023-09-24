import numpy as np
from PIL import Image
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, LinearColorMapper, BasicTicker, ColorBar, Block


def plot_img_rgba(img: Image.Image, title: str = "") -> figure:
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # bokeh needs rgba images in which the 4 channels are combined in a single uint32
    img_arr = np.array(img).view(dtype=np.uint32).reshape(img.size)

    p = figure(width=img.width // 2, height=img.height // 2, title=title)
    p.x_range.range_padding = p.y_range.range_padding = 0
    p.axis.visible = False
    p.add_tools(
        HoverTool(
            tooltips=[
                ("(x,y)", "($x{int}, $y{int})"),
                ("value", "@image{%X}"),
            ],
            formatters={"@image": "printf"},
        )
    )
    p.image_rgba(image=[img_arr], x=0, y=0, dw=img.width, dh=img.height)
    p.toolbar.logo = None

    return p


def plot_img_scalar(img: np.ndarray, title: str = "") -> figure:
    h, w = img.shape

    cmap = "Inferno256"
    color_mapper = LinearColorMapper(palette=cmap, low=img.min(), high=img.max())

    p = figure(width=w // 2, height=h // 2, title=title)
    p.x_range.range_padding = p.y_range.range_padding = 0
    p.axis.visible = False
    p.add_tools(
        HoverTool(
            tooltips=[
                ("(x,y)", "($x{int}, $y{int})"),
                ("value", "@image"),
            ],
        )
    )
    p.image(image=[img], x=0, y=0, dw=w, dh=h, color_mapper=color_mapper, level="image")
    color_bar = ColorBar(
        color_mapper=color_mapper, ticker=BasicTicker(), location=(0, 0)
    )

    p.grid.visible = False
    p.toolbar.logo = None
    p.add_layout(color_bar, "right")

    return p


def add_bboxes_on_plot(p: figure, bboxes: list) -> figure:
    for bbox in bboxes:
        y1, x1, y2, x2 = bbox

        glyph = Block(
            x=x1,
            y=y1,
            width=x2 - x1,
            height=y2 - y1,
            line_color="red",
            line_width=2,
            fill_alpha=0.0,
        )

        p.add_glyph(glyph)

    return p
