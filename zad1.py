from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np

fileH = r'C:\Users\Julian\Desktop\A70H.txt'
fileE = r'C:\Users\Julian\Desktop\A70E.txt'
R = 7
Z0 = 50


def angles(_list: list) -> np.ndarray:
    return np.linspace(-180, 180, len(_list))


def linearize(_list: list | np.ndarray) -> list:
    return [10 ** (e / 10) for e in _list]


def normalize(_list: list) -> list:
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


def to_E(_list: list | np.ndarray) -> list:
    global R
    global Z0
    return [np.sqrt(e / (4 * np.pi * R ** 2) * Z0) for e in _list]


def convert_to_dB(_list: list | np.ndarray) -> list:
    return [10 * np.log10(e / max(_list)) for e in _list]


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


def square_plot(x: list | np.ndarray, y: list | np.ndarray, unit: str, scale: tuple[int, int] = (0, 1.1),
                title: str = 'Wykres prostokątny'):
    plt.plot(angles(x), y)
    plt.grid('on')
    # plt.axis(axis)
    plt.title(title)
    plt.ylabel(unit)
    plt.ylim(scale)
    # plt.ylim([min(y), max(y)])
    # print(title)
    plt.show()


def polar_plot(x: list | np.ndarray, y: list | np.ndarray, unit: str, scale: tuple[float, float] = (0, 1.0),
               title: str = 'Wykres polarny'):
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    x = to_rad(x)
    ax.plot(x, y)
    ax.set_rticks(np.linspace(min(y), max(y), 7))  # Less radial ticks
    ax.set_rlabel_position(val_to_deg(-np.pi * 5 / 7))  # Move radial labels away from plotted line
    ax.grid(True)
    plt.ylabel(unit, loc='bottom')

    ax.set_title(title, va='top')
    plt.show()


def plot(x: list | np.ndarray, y: list | np.ndarray, plane: str):
    x_angles = angles(x)
    y_normalized = normalize(y)
    y_linear = linearize(y)
    y_dB = convert_to_dB(y_linear)
    # Wykres mocy w funkcji kąta obrotu anteny we współrzędnych prostokątnych w skali liniowej
    power_linear_title = f'Wykres zależności mocy odbieranej ' \
                         f'od\nkąta obrotu anteny w płaszczyźnie {plane} (skala liniowa).\n'
    polar_plot(x_angles, y_normalized, unit='Moc [mW]', title=power_linear_title)
    square_plot(x_angles, y_normalized, unit='Moc [mW]', title=power_linear_title)

    # Wykres mocy w funkcji kąta obrotu anteny we współrzędnych prostokątnych w skali logarytmicznej
    power_dB_title = f'Wykres zależności mocy odbieranej ' \
                     f'od\nkąta obrotu anteny w płaszczyźnie {plane} (skala logarytmiczna).\n'
    print("y_db: ", y_dB)
    print("y: ", y)
    polar_plot(x_angles, y_dB, unit='Moc [dB]', title=power_dB_title)
    square_plot(x_angles, y_dB, unit='Moc [dB]', scale=(-30, 0.5), title=power_dB_title)


def main():
    # płaszczyzna H
    dataH = read_file(fileH)
    xH, yH = split_lr(dataH)
    plot(xH, yH, plane='H')

    # płaszczyzna E
    dataE = read_file(fileE)
    xE, yE = split_lr(dataE)
    plot(xE, yE, plane='E')


if __name__ == '__main__':
    main()
