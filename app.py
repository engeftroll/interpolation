from utils import MathFunction, create_discrete_table
import graphics
import lagrange_count
import linear_count

import logging

logger = logging.getLogger("INTERPOLATION LOGS")
logging.basicConfig(
    filename="interpolation.log", 
    format="%(levelname)s\t\t %(message)s", 
    filemode="w",
    level=logging.INFO
)


math_function: MathFunction = MathFunction("log(3)/log(x) + log(x)/log(5)")
from_x, to_x = 3, 10
# Подбор коэффициентов (шага для таблицы и отображения)
step_for_discrete_table_lagrange = 1
step_for_graphics_lagrange = 0.1
# Подбор коэффициентов для кусочно-линейных функций
step_for_discrete_table_linear = 0.1
step_for_graphics_linear = 0.01


# Метод Лагранжа
result_table = create_discrete_table(logger, math_function, from_x, to_x + 1, step_for_discrete_table_lagrange)
lagrange_coefficients = lagrange_count.get_lagrange_coefficients(result_table, logger)
lagrange_function = lagrange_count.build_lagrange(lagrange_coefficients, logger)
# Вывод первого графика
graphics.build_graphics(math_function, lagrange_function, logger, from_x, to_x + 1, step_for_graphics_lagrange)

# Кусочно-линейными функциями
result_table = create_discrete_table(logger, math_function, from_x, to_x + 2, step_for_discrete_table_linear)
functions = linear_count.count_via_linear_interpolation(result_table, logger)
# Вывод второго графика
linear_count.build_graphics(functions, math_function, from_x, to_x + 1, step_for_graphics_linear)
