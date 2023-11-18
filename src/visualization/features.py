from typing import Optional
import numpy as np
import matplotlib.pyplot as plt
from bokeh.plotting import figure


def plot_feature_samples(
    feats: np.ndarray,
    anns: Optional[np.ndarray] = None,
    title: str = "",
    width=400,
    height=400,
) -> figure:
    if anns is not None:
        x_ann = feats[anns > 0.0]
        x = feats[~(anns > 0.0)]
        default_label = "Normal Samples"
    else:
        x = feats
        default_label = "Feature Samples"

    p = figure(width=width, height=height, title=title)

    p.circle(
        x[:, 0],
        x[:, 1],
        legend_label=default_label,
        fill_color="blue",
        fill_alpha=0.3,
        line_color="white",
        size=12,
    )
    if anns is not None:
        p.circle(
            x_ann[:, 0],
            x_ann[:, 1],
            legend_label="Anomalous Samples",
            fill_color="red",
            fill_alpha=0.3,
            line_color="white",
            size=12,
        )

    p.toolbar.logo = None

    return p


def plot_feature_3d_samples(
    feats: np.ndarray,
    anns: Optional[np.ndarray] = None,
    title: str = "",
    figsize=(10, 8),
) -> figure:
    if anns is not None:
        x_ann = feats[anns > 0.0]
        x = feats[~(anns > 0.0)]
        default_label = "Normal Samples"
    else:
        x = feats
        default_label = "Feature Samples"

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(projection="3d")
    ax.set_title(title)

    ax.scatter(
        x[:, 0],
        x[:, 1],
        x[:, 2],
        marker="o",
        color="blue",
        alpha=0.3,
        label=default_label,
    )

    if anns is not None:
        ax.scatter(
            x_ann[:, 0],
            x_ann[:, 1],
            x_ann[:, 2],
            marker="o",
            color="red",
            alpha=0.3,
            label="Anomalous Samples",
        )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend(loc="best")

    return ax
