import numpy as np
from PIL import Image
from bokeh.plotting import figure, show
from bokeh.palettes import Oranges3, Inferno256
from bokeh.colors import RGB
from bokeh.models import (
    HoverTool,
    LinearColorMapper,
    BasicTicker,
    ColorBar,
    ColumnDataSource,
)
import bokeh.models as bkm


def plot_img_rgba(img: Image.Image, title: str = "", red_factor: int = 2) -> figure:
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # bokeh needs rgba images in which the 4 channels are combined in a single uint32
    img_arr = np.array(img).view(dtype=np.uint32).reshape(img.size)
    # bokeh by default uses origin bottom left (origin option leads to missmatch with tooltip)
    img_arr = img_arr[::-1]

    p = figure(
        width=img.width // red_factor, height=img.height // red_factor, title=title
    )
    p.x_range.range_padding = p.y_range.range_padding = 0
    p.axis.visible = False
    r = p.image_rgba(image=[img_arr], x=0, y=0, dw=img.width, dh=img.height)

    p.add_tools(
        HoverTool(
            renderers=[r],
            tooltips=[("(x,y)", "($x{int}, $y{int})"), ("value", "@image{%X}")],
            formatters={"@image": "printf"},
        )
    )

    p.toolbar.logo = None

    return p


def plot_img_scalar(
    img: np.ndarray, title: str = "", red_factor: int = 2, flip=True
) -> figure:
    h, w = img.shape

    cmap = "Inferno256"
    color_mapper = LinearColorMapper(palette=cmap, low=img.min(), high=img.max())

    # bokeh by default uses origin bottom left (origin option leads to missmatch with tooltip)
    if flip:
        img = img[::-1]

    p = figure(width=w // red_factor, height=h // red_factor, title=title)
    p.x_range.range_padding = p.y_range.range_padding = 0
    p.axis.visible = False
    r = p.image(
        image=[img], x=0, y=0, dw=w, dh=h, color_mapper=color_mapper, level="image"
    )
    color_bar = ColorBar(
        color_mapper=color_mapper, ticker=BasicTicker(), location=(0, 0)
    )

    p.add_tools(
        HoverTool(
            renderers=[r],
            tooltips=[
                ("(x,y)", "($x{int}, $y{int})"),
                ("value", "@image"),
            ],
        )
    )
    p.add_layout(color_bar, "right")

    p.grid.visible = False
    p.toolbar.logo = None

    return p


def add_bboxes_on_img(
    p: figure, bboxes: list, red_factor: int = 2, flip=True
) -> figure:
    for bbox in bboxes:
        y1, x1, y2, x2 = bbox

        if flip:
            y_origin = p.height * red_factor - y2
        else:
            y_origin = y1

        glyph = bkm.Block(
            x=x1,
            y=y_origin,
            width=x2 - x1,
            height=y2 - y1,
            line_color="red",
            line_width=2,
            fill_alpha=0.0,
        )

        p.add_glyph(glyph)

    return p


def add_seg_on_img(
    p: figure, seg: np.ndarray, red_factor: int = 2, flip=True
) -> figure:
    """Adds a binary segmentation mask on a bokeh figure"""
    h, w = seg.shape[:2]

    # bokeh by default uses origin bottom left (origin option leads to missmatch with tooltip)
    if flip:
        seg = seg[::-1]

    cmap = (RGB(0, 0, 0, 0),) + Oranges3[::-1]
    color_mapper = LinearColorMapper(palette=cmap, low=seg.min(), high=seg.max())

    cds = ColumnDataSource(dict(annot=[seg]))

    glyph = bkm.Image(
        image="annot", x=0, y=0, dw=w, dh=h, color_mapper=color_mapper, global_alpha=0.5
    )

    r = p.add_glyph(cds, glyph)

    # change original hover attachment to allow showing both simultaneously
    hover = p.select(dict(type=HoverTool))[0]
    hover.attachment = "above"

    p.add_tools(
        HoverTool(
            renderers=[r],
            tooltips=[("annotation", "@annot")],
            attachment="below",
        )
    )

    return p


def add_score_map_on_img(
    p: figure,
    score_map: np.ndarray,
    red_factor: int = 2,
    alpha: float = 0.25,
    flip: bool = True,
) -> figure:
    """Adds a score map on a bokeh figure"""
    h, w = score_map.shape[:2]

    # bokeh by default uses origin bottom left (origin option leads to missmatch with tooltip)
    if flip:
        score_map = score_map[::-1]

    color_mapper = LinearColorMapper(
        palette=Inferno256, low=score_map.min(), high=score_map.max()
    )

    cds = ColumnDataSource(dict(score=[score_map]))

    glyph = bkm.Image(
        image="score",
        x=0,
        y=0,
        dw=w,
        dh=h,
        color_mapper=color_mapper,
        global_alpha=alpha,
    )

    r = p.add_glyph(cds, glyph)

    # change original hover attachment to allow showing both simultaneously
    hover = p.select(dict(type=HoverTool))[0]
    hover.attachment = "above"

    p.add_tools(
        HoverTool(
            renderers=[r],
            tooltips=[("score", "@score")],
            attachment="below",
        )
    )

    return p
