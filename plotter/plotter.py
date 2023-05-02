from ctypes import Union

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from statements.influence_statement import IStatement
from statements.rectangle_statement import RStatement
from statements.trapezoid_statement import TStatement


def plot_statements(mapping: dict, variables: set[str | tuple[str, str]], hypothesis=None):
    """
    Plots model using matplotlib. This only builds the plots, they are shown using the show_plot method

    Parameters:
        intervals (dict): contains statements accesseble via its pair of variables
        influences (list): list of variable pairs, whose statements should be plotted
    """

    time_variable_influences = [elem for elem in variables if type(elem) == str and not elem.endswith("'")]
    time_derivation_influences = [elem for elem in variables if type(elem) == str and elem.endswith("'")]
    variable_derivation_influence = [elem for elem in variables if type(elem) == tuple]

    _setup_plot(mapping, time_variable_influences, hypothesis)
    _setup_plot(mapping, time_derivation_influences, hypothesis)
    _setup_plot(mapping, variable_derivation_influence, hypothesis)


def _setup_plot(statements_mapping: dict, influenced, hypothesis: tuple):
    # setup amount of plots
    _, axis = plt.subplots(max(len(influenced), 2))  # when using subplots, at least 2 are needed

    # setup distance of the plots
    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.95,
                        wspace=0.4,
                        hspace=1)

    for index, influence in enumerate(influenced):
        if influence not in statements_mapping:
            continue

        _plot_axis(axis, index, hypothesis, statements_mapping, influence)


def _plot_axis(axis, index: int, hypothesis: tuple, statements_mapping: dict, influenced):
    """
    Sets up the axis range as needed and plots the statements onto them

    Parameters:
        index (int): index of the axis
        hypothesis (tuple): hypothesis that should be highlighted
        intervals (dict): contains statements accesseble via its pair of variables
        influences (list): list of variable pairs, whose statements should be plotted
    """

    statements = sorted(statements_mapping[influenced].get_statements())
    if len(statements) == 0:
        return

    # get min/max values
    min_x, max_x = min(st.start for st in statements), max(st.end for st in statements)
    min_y, max_y = min(st.lower for st in statements), max(st.upper for st in statements)
    if hypothesis is not None and hypothesis[0] == influenced:
        min_x = min(min_x, hypothesis[1][0])
        max_x = max(max_x, hypothesis[1][1])
        min_y = min(min_y, hypothesis[2][0])
        max_y = max(max_y, hypothesis[2][1])

    # build axis and add offset to prevent statements from overlapping it
    offset_x: float = abs(max_x - min_x) if abs(max_x - min_x) != 0 else 10
    offset_y: float = abs(max_y - min_y) if abs(max_y - min_y) != 0 else 10
    margin_x: float = offset_x / 30
    margin_y: float = offset_y / 6
    axis[index].axis([min_x - margin_x, max_x + margin_x, min_y - margin_y, max_y + margin_y])
    axis[index].set(xlabel="t", ylabel=influenced)

    # plot the statements
    for st in statements:
        if isinstance(st, TStatement):
            _plot_t_statement(axis[index], st)
            continue
        _plot_r_statement(axis[index], st)

    # plot highlighted hypothesis
    if hypothesis is not None and hypothesis[0] == influenced:
        statement_interval: RStatement = RStatement.create(hypothesis)
        _plot_r_statement(axis[index], statement_interval, "red")


def _plot_t_statement(ax, st: TStatement, color="black"):
    """
    Plots a given statement by drawing its borders and inserting the quality in the center

    Parameters:
        ax: current axis
        st (Statement): statement to draw
        color (str): color of the statement
    """
    rect = mpatches.Polygon(st.get_coordinates(),
                            fill=False,
                            alpha=1,
                            color=color,
                            linewidth=0.5)
    ax.add_patch(rect)


def _plot_r_statement(ax, st: RStatement, color="black"):
    """
    Plots a given statement by drawing its borders and inserting the quality in the center

    Parameters:
        ax: current axis
        st (Statement): statement to draw
        color (str): color of the statement
    """

    bottom: float = st.start
    left: float = st.lower
    width: float = st.end - st.start
    height: float = st.upper - st.lower

    # create window
    rect = mpatches.Rectangle((bottom, left), width, height,
                              fill=False,
                              alpha=1,
                              color=color,
                              linewidth=0.5)
    ax.add_patch(rect)

    if isinstance(st, IStatement):
        st.__class__ = IStatement
        rx, ry = rect.get_xy()
        cx = rx + rect.get_width() / 2.0
        cy = ry + rect.get_height() / 2.0
        ax.annotate(f"[{st.min_slope}, {st.max_slope}]", (cx, cy), color='black', weight='bold',
                    fontsize=10, ha='center', va='center')


def show_plot():
    """
    Show all previously created plots
    """

    plt.show()
