import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np


def draw_boxplot(df, col_perc=('25_perc', '50_perc', '75_perc'),
                 col_whisker=('whisker_min', 'whisker_max'),
                 col_outliers=('outliers_min', 'outliers_max'),
                 box_colors=('orchid', 'darkkhaki'),
                 figsize=(20, 5), fontsize_x=14, fontsize_y=14,
                 fontsize_title=16, y_lim=None, x_tick_labels=None,
                 rotation_x=90, title='', x_label_txt='', y_label_txt='',
                 **boxplot_kwargs):
    """
    Draw custom boxplot.

    Parameters
    ----------
    df : Pandas DataFrame
        Values to draw the boxplots
        - Must contain the columns listed in `col_perc`, `col_whisker`,
          `col_outliers`
        - Each row will be a boxplot in the order that they appear
    col_perc : list, tuple, optional
        Column names of the 25th, 50th and 75th percentiles respectively. Each 
        row in these columns of the DataFrame must contain a number.
    col_whisker : list, tuple, optional
        Column names of the minimum and maximum position of the whiskers,
        respectively. Each row in these columns of the DataFrame must contain a 
        number.
    col_outliers : list, tuple, optional
        Column names of the lowest and highest values of the outliers. Each row
        in these columns of the DataFrame must contain a number or a collection
        of values.
    box_colors : list, tuple, optional
        Color names.
    figsize : tuple of integers, optional
        Width, height in inches
    fontsize_x, fontsize_y, fontsize_title : numeric, optional
        Font size of the x-axis or y-axis labels (titles and ticks) or of the
        title
    y_lim : tuple, list, optional
        y-axis limits
    x_tick_labels : tuple, list, optional
        x-axis labels. The default is the DataFrame index values.
    rotation_x : numeric, optional
        Rotation angle in degrees of the x-axis
    title : str, optional
        Title
    x_label_txt, y_label_txt : str, optional
        Text for the x- and y-axes. The default value is the index and column
        names, respectively.
    boxplot_kwargs
        additional arguments to be passed to matplotlib's boxplot

    Returns
    -------
    Side-by-side boxplots

    Examples
    --------
    >>> import pandas as pd
    >>> %matplotlib inline

    >>> df = pd.DataFrame({'25_perc': 10, '50_perc': 20, '75_perc': 30,
                           'whisker_min': 5, 'whisker_max': 50,
                           'outliers_min': [[-10, 0]], 'outliers_max': 80},
                          index=pd.Index(['A'], name='My index'),
                          columns=pd.Index(['outliers_min', 'whisker_min',
                                            '25_perc', '50_perc', '75_perc',
                                            'whisker_max', 'outliers_max'],
                                           name='My columns'))
    >>> draw_boxplot(df)

    >>> df = pd.DataFrame(data=pd.np.sort((pd.np.random
                                           .RandomState(seed=44)
                                           .randint(low=1, high=100,
                                                    size=(3, 7))),
                                          axis=1),
                          index=['index_A', 'index_B', 'index_C'],
                          columns=['outliers_min', 'whisker_min', '25_perc',
                                   '50_perc', '75_perc', 'whisker_max',
                                   'outliers_max'])
    >>> df['outliers_min'] = [[1,5,10], [10,15], 0]
    >>> draw_boxplot(df)

    >>> draw_boxplot(df=df,
                     sym='k.',
                     figsize=(10, 4),
                     fontsize_x=10, fontsize_y=12, fontsize_title=18,
                     title='My Boxplot',
                     y_lim=(-50, 150),
                     x_tick_labels=tuple('ABC'),
                     rotation_x=60,
                     x_label_txt='My x-axis', y_label_txt='My y-axis')

    Notes
    -----
    Inspired by:
    - http://stackoverflow.com/questions/29230766/matplotlib-boxplot-using-summary-stats-and-patch-artist-true
    - http://stackoverflow.com/questions/27214537/is-it-possible-to-draw-a-matplotlib-boxplot-given-the-percentile-values-instead
    """

    n_box = len(df)  # number of boxplots
    _, ax = plt.subplots(figsize=figsize)

    # initialize boxplot with dummy data
    box_plot = ax.boxplot([[-9, -4, 2, 4, 9],]*n_box, **boxplot_kwargs)
    min_y, max_y = float('inf'), -float('inf')

    for bb in xrange(n_box):

        # Interquantile range
        IQR = (df.iloc[bb][col_perc[0]], df.iloc[bb][col_perc[2]])

        # Confidence limit
        CL = (df.iloc[bb][col_whisker[0]], df.iloc[bb][col_whisker[1]])
        outliers = np.hstack([df.iloc[bb][col_outliers[0]],
                              df.iloc[bb][col_outliers[1]]])

        # Draw boxplot
        box_plot['medians'][bb].set_ydata([df.iloc[bb][col_perc[1]],
                                           df.iloc[bb][col_perc[1]]])

        # box_plot['boxes'][bb]._xy[[0,1,4], 1] = IQR[0]
        # box_plot['boxes'][bb]._xy[[2,3], 1] = IQR[1]
        box_plot['boxes'][bb].set_ydata([IQR[0], IQR[0], IQR[1], IQR[1],
                                         IQR[0]])

        # Whiskers
        box_plot['whiskers'][2*bb].set_ydata([CL[0], IQR[0]])    # lower
        box_plot['whiskers'][2*bb+1].set_ydata([IQR[1], CL[1]])  # higher

        # Caps
        box_plot['caps'][2*bb].set_ydata([CL[0], CL[0]])    # lower
        box_plot['caps'][2*bb+1].set_ydata([CL[1], CL[1]])  # higher

        # Fliers
        box_plot['fliers'][bb].set(xdata=[bb+1]*len(outliers), ydata=outliers)

        # Colors
        plt.setp(box_plot['boxes'], color='black')
        plt.setp(box_plot['whiskers'], color='black')
        # plt.setp(box_plot['fliers'], marker='None')

        # Fill the boxes (alternate between the colors)
        box_polygon = Polygon(list(zip(box_plot['boxes'][bb].get_xdata(),
                                       box_plot['boxes'][bb].get_ydata())),
                              facecolor=box_colors[bb % len(box_colors)],
                              alpha=.5)
        ax.add_patch(box_polygon)

        # y-axis limits
        if y_lim is None:
            min_y = min(np.r_[min_y, df.iloc[bb][col_outliers[0]], CL[0]])
            max_y = max(np.r_[max_y, df.iloc[bb][col_outliers[1]], CL[1]])

    # y-axis limits
    if y_lim is None:
        ylims = (min_y, max_y)
        ylims = np.array(ylims) + [-0.1*np.ptp(ylims), 0.1*np.ptp(ylims)]
        # set the limits to 10% above and below the extreme values
    else:
        ylims = y_lim
    ax.set_ylim(ylims)

    # Ticks
    ax.tick_params(axis='y', labelsize=fontsize_y)
    if x_tick_labels is None:
        x_tick_labels = df.index.tolist()
    ax.set_xticks(range(1, n_box+1))
    ax.set_xticklabels(labels=x_tick_labels, rotation=rotation_x,
                       fontsize=fontsize_x)

    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                  alpha=0.8)

    # Hide these grid lines behind plot objects
    ax.set_axisbelow(True)

    # Texts
    ax.set_title(title, fontsize=fontsize_title)
    ax.set_xlabel(df.index.name or x_label_txt, fontsize=fontsize_x)
    ax.set_ylabel(df.columns.name or y_label_txt, fontsize=fontsize_y)
