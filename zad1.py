from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np

fileH = r'C:\Users\Julian\Desktop\A70H.txt'
fileE = r'C:\Users\Julian\Desktop\A70E.txt'
R = 8
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


def calculate_E(_list: list | np.ndarray) -> list:
    global R
    global Z0
    return [np.sqrt(((0.001 * e) / (4 * np.pi * (R ** 2))) * Z0) for e in _list]


def convert_to_dB(_list: list | np.ndarray) -> list:
    return [10 * np.log10(e / max(_list)) for e in _list]


def get_scale(_list: list | np.ndarray) -> tuple[float, float]:
    return min(_list) - 0.0000001 * min(_list), max(_list) + 0.0000001 * max(_list)


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


def square_plot(x: list | np.ndarray, y: list | np.ndarray, unit: str, scale: tuple[float, float] = (0, 1.1),
                title: str = 'Wykres prostokątny'):
    plt.plot(angles(x), y)
    plt.grid('on')
    # plt.axis(axis)
    plt.title(title)
    plt.ylabel(unit)
    plt.ylim(scale)
    # plt.axis('equal')
    # plt.ylim([min(y), max(y)])
    # print(title)
    plt.show()


def polar_plot(x: list | np.ndarray, y: list | np.ndarray, unit: str, scale: tuple[float, float] = (0, 1.0),
               title: str = 'Wykres polarny'):
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    x = to_rad(x)
    ax.plot(x, y)
    ax.set_rticks(np.linspace(*scale, 7))  # Less radial ticks
    ax.set_rlabel_position(val_to_deg(-np.pi * 5 / 7))  # Move radial labels away from plotted line
    ax.grid(True)
    plt.ylabel(unit, loc='bottom')
    plt.ylim(scale)

    ax.set_theta_zero_location("N")
    ax.set_title(title, va='top')
    # plt.axis('equal')
    plt.show()


def plot(x: list | np.ndarray, y: list | np.ndarray, plane: str):
    x_angles = angles(x)
    y_linear = linearize(y)
    y_normalized = normalize(y)
    # y_dB = convert_to_dB(y_linear)
    y_E = calculate_E(y_linear)
    y_E_linear = normalize(calculate_E(y_linear))
    y_E_dB = convert_to_dB(y_E)
    linear = (-0.1, 1.1)
    logarithmic = (-30.5, 0.5)

    # Wykres mocy w funkcji kąta obrotu anteny we współrzędnych prostokątnych w skali liniowej
    power_linear_title = f'Unormowany wykres zależności mocy odbieranej ' \
                         f'od\nkąta obrotu anteny w płaszczyźnie {plane} (skala liniowa).\n'
    polar_plot(x_angles, y_normalized, unit='Moc [mW]', scale=linear, title=power_linear_title)
    square_plot(x_angles, y_normalized, unit='Moc [mW]', scale=linear, title=power_linear_title)

    # # Wykres mocy w funkcji kąta obrotu anteny we współrzędnych prostokątnych w skali logarytmicznej
    # power_dB_title = f'Wykres zależności mocy odbieranej ' \
    #                  f'od\nkąta obrotu anteny w płaszczyźnie {plane} (skala logarytmiczna).\n'
    # polar_plot(x_angles, y_dB, unit='Moc [dB]', scale=(-30.5, 0.5), title=power_dB_title)
    # square_plot(x_angles, y_dB, unit='Moc [dB]', scale=(-30.5, 0.5), title=power_dB_title)

    # Wykres pola elektrycznego w funkcji kąta obrotu anteny we współrzędnych prostokątnych w skali liniowej
    E_linear_title = f'Unormowany wykres natężenia pola elektrycznego w zależnośći' \
                     f'od\nkąta obrotu anteny w płaszczyźnie {plane} (skala liniowa).\n'
    polar_plot(x_angles, y_E_linear, unit='Natężenie pola elektrycznego [mV/m]',
               scale=linear, title=E_linear_title)
    square_plot(x_angles, y_E_linear, unit='Natężenie pola elektrycznego [mV/m]',
                scale=linear, title=E_linear_title)
    # print(y_E_linear)

    # Wykres pola elektrycznego w funkcji kąta obrotu anteny we współrzędnych prostokątnych w skali logarytmicznej
    E_dB_title = f'Wykres natężenia pola elektrycznego w zależności' \
                     f'od\nkąta obrotu anteny w płaszczyźnie {plane} (skala logarytmiczna).\n'
    polar_plot(x_angles, y_E_dB, unit='Natężenie pola elektrycznego [mV/m]',
               scale=logarithmic, title=E_dB_title)
    square_plot(x_angles, y_E_dB, unit='Natężenie pola elektrycznego [mV/m]',
                scale=logarithmic, title=E_dB_title)


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
