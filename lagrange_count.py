import numpy as np
from utils import MathFunction
from logging import Logger


def get_lagrange_coefficients(table: dict, logger: Logger):
    """
    Составляем СЛАУ, решаем СЛАУ
    f(x1) = L(x1) = a0 + a1 x1^1 + a2 x1^2 + ... + an x1^n
    f(x2) = L(x2) = a0 + a1 x2^1 + a2 x2^2 + ... + an x2^n
    ....
    f(xn) = L(xn) = a0 + a1 xn^1 + a2 xn^2 + ... + an xn^n

    Решить СЛАУ = Получить {a_n}.
    """
    vector_b = list()
    matrix_a = list()

    logger.info(f"--= GETTING LAGRANGE COEFFICIENTS =--")
    logger.info(f"A-matrix | b-vector")
    for x, y in table.items():
        vector_b.append(y)
        line = list()
        for i in range(len(table.items())):
            line.append(x ** i)
        matrix_a.append(line)
        logger.info(f"{' '.join(map(str, line))} | {y}")
    
    matrix_a = np.array(matrix_a).astype(np.float64)
    vector_b = np.array(vector_b).astype(np.float64)
    
    a_vector = np.linalg.solve(matrix_a, vector_b)
    logger.info("Result of solving Ax = b:")
    for i, a_i in enumerate(a_vector):
        logger.info(f"a{i} = {a_i}")
    logger.info("--= END LAGRANGE COEFFICIENTS =--")
    return a_vector



def build_lagrange(coefficients, logger: Logger) -> MathFunction:
    """
    Строит функцию Лагранжа на основе набора коэффициентов
    """
    res = ""
    for i, coefficient in enumerate(coefficients):
        res += f"{coefficient} * x ** {i} + "

    logger.info("Result function: " + str(MathFunction(res[:-2])))
    return MathFunction(res[:-2])
