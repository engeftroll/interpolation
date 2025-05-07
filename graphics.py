import matplotlib.pyplot as plt
from logging import Logger


def build_graphics(function: callable, lagrange_function: callable, logger: Logger, from_range: int = -10, to_range: int = 10, step: float = 0.01):
    """
    Здесь происходит построение графика и соответствующая оценка погрешностей
    """
    x_original_function = list()
    y_original_function = list()

    x_lagrange_function = list()
    y_lagrange_function = list()

    x = from_range
    while x <= to_range:
        x_original_function.append(x)
        y_original_function.append(function(x=x))

        x_lagrange_function.append(x)
        y_lagrange_function.append(lagrange_function(x=x))

        logger.info(f"|f({x}) - L({x})| = {abs(function(x=x) - lagrange_function(x=x))}")
        x += step

    plt.plot(x_original_function, y_original_function, color="red", label="Original")
    plt.plot(x_lagrange_function, y_lagrange_function, color="blue", label="Lagrange function")
    plt.legend()
    plt.show()
