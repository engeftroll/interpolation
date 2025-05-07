from math import e as math_e

from sympy import Expr, parse_expr
from logging import Logger


class MathFunction:
    """Кастомный класс, чтобы упростить себе жизнь в решениях ниже"""

    def __init__(self, entered_function: str):
        self.equation: Expr = parse_expr(entered_function)
    
    def __call__(self, *args, **kwds) -> float:
        """На вход подаются аргументы, которые надо заменить на числа"""
        kwds["e"] = math_e
        return self.equation.evalf(subs=kwds)  # noqa: Подразумевается, что все переменные подставляются

    def get_derivative(self, *args) -> "MathFunction":
        return MathFunction(str(self.equation.diff(*args)))
    
    def __repr__(self):
        return f"<MathFunction expr=[{self.equation}]>"


def create_discrete_table(
        logger: Logger,
        function: callable,
        from_range: int = -10, to_range: int = 10,
        step: float = 0.01,
):
    """Составление таблицы с конкретными дискретными значениями"""
    logger.info("--= CREATING DISCRETE TABLE =--")
    result_table = dict()
    x = from_range
    while x <= to_range:
        result_table[x] = function(x=x)
        logger.info(f"f({x}) = {result_table[x]}")
        x += step
    logger.info("--= END DISCRETE TABLE =--")
    return result_table
