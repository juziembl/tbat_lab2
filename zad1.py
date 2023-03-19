from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np

file1 = r'C:\Users\Julian\Desktop\A70E.txt'
file2 = r'C:\Users\Julian\Desktop\A70H.txt'
R = 36 * 10 ** 6
Z0 = 50


def angles(_list: list) -> np.ndarray:
    return np.linspace(-180, 180, len(_list))


def normalise(_list: list) -> list:
    _list = linearize(_list)
    return [e / max(_list) for e in _list]


def val_to_deg(val: int | float) -> float:
    return 180 * val / np.pi


def val_to_rad(val: int | float) -> float:
    return val * np.pi / 180


def to_deg(_list: list | np.ndarray) -> list:
    return [val_to_deg(e) for e in _list]


def to_rad(_list: list | np.ndarray) -> list:
    return [val_to_rad(e) for e in _list]


def linearize(_list: list | np.ndarray) -> list:
    return [10 ** (e / 10) for e in _list]


def to_E(_list: list | np.ndarray) -> list:
    global R
    global Z0
    return [np.sqrt(e / (4 * np.pi * R**2) * Z0) for e in _list]


def split_lr(_list) -> tuple[list, list]:
    left = [e for i, e in enumerate(_list) if i % 2 == 0]
    right = [e for i, e in enumerate(_list) if i % 2 != 0]
    return left, right


def read_file(file_path) -> list:
    with open(file_path, 'r') as fp:
        lines = fp.read().split(';')
        res = []
        for line in lines:
            try:
                res.append(float(line))
            except ValueError:
                continue
        return res


def square_plot(x: list | np.ndarray, y: list | np.ndarray, unit: str, axis='equal', title: str = 'Wykres prostokątny'):
    plt.plot(angles(x), y)
    plt.grid('on')
    plt.axis(axis)
    plt.title(title)
    plt.ylabel(unit)
    print(title)
    # plt.ylim(min(y), max(y))
    plt.show()


def polar_plot_decibel(x: list | np.ndarray, y: list | np.ndarray, unit: str, title: str = 'Wykres polarny'):
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    x = to_rad(x)
    print(y)
    print(min(y))
    print(max(y))
    ax.plot(x, y)
    ax.set_rticks(np.linspace(-95, -60, 5))  # Less radial ticks
    ax.set_rlabel_position(val_to_deg(-np.pi * 5 / 7))  # Move radial labels away from plotted line
    ax.grid(True)
    plt.ylabel(unit, loc='bottom', rotation=None)

    ax.set_title(title, va='top')
    plt.show()


def polar_plot_linear(x: list | np.ndarray, y: list | np.ndarray, unit: str, title: str = 'Wykres polarny'):
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    x = to_rad(x)
    y = linearize(y)
    print(y)
    print(min(y))
    print(max(y))
    ax.plot(x, y)
    ax.set_rticks(np.linspace(min(y), max(y), 5))  # Less radial ticks
    ax.set_rlabel_position(val_to_deg(-np.pi * 5 / 7))  # Move radial labels away from plotted line
    ax.grid(True)
    plt.ylabel(unit, loc='bottom', rotation=None)

    ax.set_title(title, va='top')
    plt.show()


def main():
    # od 8 do 64 s
    data = read_file(file1)
    x, y = split_lr(data)
    th = angles(x)
    square_plot(th, y, unit='Moc w dBm', title='')
    square_plot(th, linearize(y), unit='Moc w mW', axis='tight', title='')
    polar_plot_decibel(th, y, unit='Moc w dBm', title='')
    polar_plot_linear(th, y, unit='Moc w mW', title='')


if __name__ == '__main__':
    main()
