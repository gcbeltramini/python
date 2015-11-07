class ProgressBar(object):
    """
    Display progress bar

    Parameters
    ----------
    - message (str): message to display in front of the progress bar
    - char (str): character of the progress bar
    - nchars (int): number of characters of the progress bar
    - value (int): current value of the progress bar (0, 1, ..., `n_steps`)
        - Only used when `fraction` = None
    - n_steps (int): number of steps of the progress bar
        - Only used when `fraction` = None
    - fraction (float): fraction of the progress bar (0 <= `fraction` <= 1)
        - If `fraction` = None, `fraction` will be set equal to float(`value`) / `n_steps`

    Returns
    -------
    `show_bar` displays the progress bar

    Examples
    --------
    >>> from time import sleep
    >>>
    >>> n_steps = 30
    >>>
    >>> from IPython.display import display
    >>> from ipywidgets import FloatProgress
    >>> progress_bar_alt = FloatProgress(min=0, max=n_steps, description='Running...')
    >>> display(progress_bar_alt)
    >>>
    >>> progress_bar = ProgressBar(n_steps=n_steps, message='Running')
    >>> for ii in range(n_steps):
    >>>     progress_bar.update_bar()  # or progress_bar.value += 1
    >>>     progress_bar.show_bar()
    >>>     progress_bar_alt.value += 1
    >>>     sleep(.2)
    >>> progress_bar_alt.description = 'Done!'
    >>> progress_bar.message = 'Done!'
    >>> progress_bar.show_bar()
    """

    def __init__(self, message='', char='=', nchars=40, value=0, n_steps=100, fraction=None):
        self._message = message
        self.char = char
        self.nchars = nchars
        self._value = value
        self.n_steps = n_steps
        if fraction is None:
            fraction = float(self.value) / self.n_steps
        self._fraction = fraction
        self.create_bar(fraction=self.fraction)

    @property
    def message(self):
        return self._message

    @property
    def value(self):
        return self._value

    @property
    def fraction(self):
        return self._fraction

    @message.setter
    def message(self, message):
        self._message = max(len(self.message) - len(message), 0)*' ' + message  # try to keep the size of the previous message
        self.create_bar(message=self.message)

    @value.setter
    def value(self, value):
        self._value = value
        self.fraction = float(self.value) / self.n_steps
        self.create_bar(fraction=self.fraction)

    @fraction.setter
    def fraction(self, fraction):
        self._fraction = fraction
        self.create_bar(fraction=self.fraction)

    def create_bar(self, fraction=None, message=None):
        fraction = fraction or self.fraction
        message = message or self.message
        self.bar_str = "\r{msg:s} [{bar:s}] {fraction:6.1%}".format(msg=message,
                                                                    bar=self.char*int(round(self.nchars*fraction)) + \
                                                                        ' '*(self.nchars-int(round(self.nchars*fraction))),
                                                                    fraction=fraction)

    def update_bar(self, fraction=None):
        if fraction is None:
            self.value += 1
        else:
            self.fraction = fraction

    def show_bar(self):
        sys.stdout.write(self.bar_str)
        sys.stdout.flush()
