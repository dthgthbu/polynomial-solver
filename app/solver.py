import numpy as np


def find_roots(coefficients: list[float]) -> list[list[float]]:
    """
    Возвращает корни многочлена.
    coefficients — от старшей степени к младшей, например [1, -3, 2] = x^2 - 3x + 2.
    Возвращает список пар [real, imag].
    """
    if not coefficients:
        raise ValueError("Список коэффициентов пуст")
    if all(c == 0 for c in coefficients):
        raise ValueError("Все коэффициенты нулевые — это не многочлен")

    roots = np.roots(coefficients)
    return [[float(r.real), float(r.imag)] for r in roots]
