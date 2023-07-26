import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from statements.td_statement import TDStatement
from statements.tv_statement import TVStatement
from statements.vd_statement import VDStatement


def _extract_kind(hypothesis: tuple):
    if hypothesis is None:
        return ""

    if len(hypothesis) == 5:
        return "VD"
    elif len(hypothesis) == 4:
        return "TV"
    return "TD"


def plot_statements(tv_container, td_container, vd_container, tv_influences, td_influences, vd_influences, hypothesis=None):
    kind: str = _extract_kind(hypothesis)

    _setup_plot(tv_container, tv_influences, hypothesis if kind == "TV" else None)
    _setup_plot(td_container, td_influences, hypothesis if kind == "TD" else None, derivative=True)
    _setup_plot(vd_container, vd_influences, hypothesis if kind == "VD" else None, derivative=True)


def _setup_plot(container: dict, influenced, hypothesis: tuple, derivative=False):
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
        if influence not in container:
            continue

        _plot_axis(axis, index, hypothesis, container, influence, derivative)


def _plot_axis(axis, index: int, hypothesis: tuple, statements_mapping: dict, influenced, derivative):
    statements = sorted(statements_mapping[influenced].get_statements())
    if len(statements) == 0:
        return

    # get min/max values
    min_x, max_x = min(st.start for st in statements), max(st.end for st in statements)
    if statements and isinstance(statements[0], TVStatement):
        min_y, max_y = min(min(st.lower, st.lower_r) for st in statements), max(max(st.upper_r, st.upper) for st in statements)
    else:
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
    x_label = "t" if isinstance(influenced, str) else influenced[0]
    y_label = influenced if isinstance(influenced, str) else influenced[1]
    if derivative:
        y_label += "'"
    axis[index].set(xlabel=x_label, ylabel=y_label)

    # plot the statements
    for st in statements:
        if isinstance(st, TVStatement):
            _plot_t_statement(axis[index], st)
            continue
        _plot_r_statement(axis[index], st)

    # plot highlighted hypothesis
    kind: str = _extract_kind(hypothesis)
    if hypothesis is not None:
        if kind == "TV" and hypothesis[0] == influenced:
            statement_interval: TVStatement = TVStatement.create(hypothesis)
            _plot_t_statement(axis[index], statement_interval, "red")
        elif kind == "TD" and hypothesis[0] == influenced:
            statement_interval: TDStatement = TDStatement.create(hypothesis)
            _plot_r_statement(axis[index], statement_interval, "red")
        elif kind == "VD" and (hypothesis[0], hypothesis[-1]) == influenced:
            statement_interval: VDStatement = VDStatement.create(hypothesis)
            _plot_r_statement(axis[index], statement_interval, "red")


def _plot_t_statement(ax, st: TVStatement, color="black"):
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


def _plot_r_statement(ax, st: TDStatement, color="black"):
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

    if isinstance(st, VDStatement):
        st.__class__ = VDStatement
        rx, ry = rect.get_xy()
        cx = rx + rect.get_width() / 2.0
        cy = ry + rect.get_height() / 2.0
        ax.annotate(f"[{st.min_slope}, {st.max_slope}]", (cx, cy), color=color, weight='bold',
                    fontsize=4, ha='center', va='center')


def show_plot():
    """
    Show all previously created plots
    """

    plt.show()
