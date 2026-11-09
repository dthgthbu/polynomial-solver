import pytest

from app.solver import find_roots


def _normalize_roots(roots):
    """Сортирует корни, чтобы сравнивать без привязки к порядку."""
    return sorted(roots, key=lambda r: (r[0], r[1]))


def test_quadratic_two_roots():
    # x^2 - 3x + 2 = 0 → корни 1 и 2
    roots = _normalize_roots(find_roots([1, -3, 2]))
    assert roots == [[1.0, 0.0], [2.0, 0.0]]


def test_quadratic_no_real_roots():
    # x^2 + 1 = 0 → корни ±i
    roots = _normalize_roots(find_roots([1, 0, 1]))
    assert len(roots) == 2
    assert roots[0][1] == pytest.approx(-1.0)
    assert roots[1][1] == pytest.approx(1.0)
    assert roots[0][0] == pytest.approx(0.0)
    assert roots[1][0] == pytest.approx(0.0)


def test_linear():
    # 2x - 4 = 0 → корень 2
    roots = find_roots([2, -4])
    assert len(roots) == 1
    assert roots[0][0] == pytest.approx(2.0)
    assert roots[0][1] == pytest.approx(0.0)


def test_empty_coefficients():
    with pytest.raises(ValueError):
        find_roots([])


def test_all_zero():
    with pytest.raises(ValueError):
        find_roots([0, 0, 0])
