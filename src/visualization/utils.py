from pathlib import Path
import bs4
from html.parser import HTMLParser
from bokeh.plotting import curdoc, figure, show, output_file, save, reset_output
from bokeh.io import output_notebook


def save_plot_from_notbook_for_jekyll(
    p: figure, output_path: Path, title: str = None
) -> None:
    """Saves a plot from a notebook such that it can be directly used within the jekyll framework"""

    save_plot_from_notebook_to_html(p, output_path, title)
    bokeh_html_to_jekyll(output_path)


def save_plot_from_notebook_to_html(
    p: figure, output_path: Path, title: str = None
) -> None:
    """To save a bokeh plot from notebook to a file we temporarily need to change the output target"""

    # switch to file output so save the plots
    bokeh_file_setup(output_path, title)
    save(p)


def bokeh_notebook_setup():
    output_notebook()
    bokeh_common_setup()


def bokeh_file_setup(output_path: Path, title: str = None):
    output_file(filename=output_path, title=title)
    bokeh_common_setup()


def bokeh_common_setup():
    curdoc().theme = "dark_minimal"


def bokeh_html_to_jekyll(html_path: Path) -> None:
    """Only a part of the bokeh html is needed to embed a plot within jekyll

    - keeps only 1st-level script and div tags
    - wraps the 'application/json' script in {% raw %} and {% endraw %} lines
        - this is due to an incompatibility between bokeh 3.2.2 and jekyll liquid processing
        - see: https://talk.jekyllrb.com/t/code-block-is-improperly-handled-and-generates-liquid-syntax-error/7599/2
    """

    with open(html_path) as f:
        soup = bs4.BeautifulSoup(f, "html.parser")

    plot_code = soup.find_all("script")
    plot_code.extend(soup.find_all("div"))

    # fix of bokeh liquid processing issue
    for el in plot_code:
        if el.has_attr("type") and el["type"] == "application/json":
            code_block = el.string
            el.string = "{% raw %}" + code_block + "{% endraw %}"

    with open(html_path, "w", encoding="utf-8") as out:
        for el in plot_code:
            out.write(f"{str(el)}\n")
