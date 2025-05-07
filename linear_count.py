from logging import Logger

import numpy as np
from typing import Tuple, Dict, Optional
from utils import MathFunction
import matplotlib.pyplot as plt


class PiecewiseLinearFunction(MathFunction):
    """Кастомный класс кусочно-линейной функции на интервале [from_x, to_x]"""
    def __init__(self, raw_function: str, from_x: float, to_x: float):
        super().__init__(raw_function)
        self.from_x = from_x
        self.to_x = to_x

    def __repr__(self):
        return f"<PiecewiseLinearFunction y={self.equation}; [{self.from_x}, {self.to_x}]>"


class SystemOfLinearFunctions:
    """Система линейных функций"""
    def __init__(self, from_x: float, to_x: float):
        self.from_x = from_x
        self.to_x = to_x
        self.functions: Dict[Tuple[float, float], PiecewiseLinearFunction] = dict()

    def add_function(self, function: PiecewiseLinearFunction):
        if self.from_x > function.from_x:
            raise ValueError(f"Function not in the system, right border ({self.from_x} > {function.from_x})")
        if self.to_x < function.from_x:
            raise ValueError(f"Function not in the system, left border ({self.to_x} < {function.from_x})")

        self.functions[(function.from_x, function.to_x)] = function

    def __call__(self, *args, **kwargs) -> Optional[float]:
        """Поиск нужной функции и подстановка её в подходящую"""
        if kwargs.get("x") is None:
            raise TypeError(f"You forgot to add 'x=' when you call <{self}>")

        x = kwargs.get("x")
        result_function = None
        if not (self.from_x <= x <= self.to_x):
            raise ValueError(f"Impossible value for x={x} (should be in [{self.from_x}, {self.to_x}]")

        for (from_x, to_x), function in self.functions.items():
            if not (from_x <= x <= to_x):
                continue
            result_function = function(x=x)
        return result_function


def get_linear_function(x_prev: float, y_prev: float, x_next: float, y_next: float) -> PiecewiseLinearFunction:
    """
    Получение самой кусочно-линейно функции на основе (x_prev, y_prev) и (x_next, y_next).
    """
    k = (y_next - y_prev) / (x_next - x_prev)
    b = y_prev - k * x_prev
    linear_function = PiecewiseLinearFunction(f"{k} * x + {b}", x_prev, x_next)
    return linear_function


def count_via_linear_interpolation(table: dict, logger: Logger) -> SystemOfLinearFunctions:
    """
    Опираясь на таблицу дискретных значений, построить системы кусочно-линейных функций.
    """
    x_prev, y_prev = sorted(list(table.items()))[0]
    result_function_system = SystemOfLinearFunctions(
        from_x=min(table),
        to_x=max(table)
    )
    i = 0
    for x, y in sorted(list(table.items()))[1:]:
        x_next, y_next = x, y
        function_i: PiecewiseLinearFunction = get_linear_function(x_prev, y_prev, x_next, y_next)
        logger.info(f"F_{i}(x) = {function_i}")
        result_function_system.add_function(function_i)
        x_prev, y_prev = x, y
        i += 1
    return result_function_system


def build_graphics(
        system_of_functions: SystemOfLinearFunctions,
        orig_function: callable,
        from_x: float, to_x: float, step: float
):
    x_linear_list = list()
    y_linear_list = list()

    x_original_list = list()
    y_original_list = list()

    x = from_x
    while x <= to_x:
        y_original = orig_function(x=x)
        y_linear = system_of_functions(x=x)

        x_original_list.append(x)
        y_original_list.append(y_original)

        x_linear_list.append(x)
        y_linear_list.append(y_linear)
        x += step

    x_linear_list = np.array(x_linear_list).astype(np.float64)
    y_linear_list = np.array(y_linear_list).astype(np.float64)

    x_original_list = np.array(x_original_list).astype(np.float64)
    y_original_list = np.array(y_original_list).astype(np.float64)

    plt.plot(x_linear_list, y_linear_list, color="red", label="Linear function")
    plt.plot(x_original_list, y_original_list, color="blue", label="Original")
    plt.legend()
    plt.show()
