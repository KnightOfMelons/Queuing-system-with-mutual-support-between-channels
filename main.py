# Домашнее задание № 7

# Имеется трехканальная СМО с очередью: интенсивность потока заявок λ = 4 заявки в 1 мин, среднее время обслуживания
# одной заявки одним каналом tоб = [10, 250] секунд, максимальное число заявок в очереди m = [2, 100]. Функция φ(k)
# = kφ. Найти Q и A проп. способности. Построить графики. Сравнить параметры для случая без взаимопомощи и с
# равномерной взаимопомощью.

import numpy as np
import math
import matplotlib.pyplot as plt

arrival_rate = 4
num_channels = 3

service_time = np.arange(10, 251, 1)
service_rate = 1 / service_time * 60
max_queue = np.arange(2, 101, 1)

service_rate, max_queue = np.meshgrid(service_rate, max_queue)

load_factor = arrival_rate / service_rate
normalized_load = load_factor / num_channels

p0 = (
    sum(load_factor ** i / math.factorial(i) for i in range(num_channels + 1)) +
    (load_factor ** (num_channels + 1) / math.factorial(num_channels + 1)) *
    (1 - (load_factor / num_channels) ** max_queue) / (1 - load_factor / num_channels)
) ** -1

block_probability_no_help = (
    p0 * load_factor ** (num_channels + max_queue) /
    (num_channels ** max_queue * math.factorial(num_channels))
)
throughput_no_help = 1 - block_probability_no_help
absolute_throughput_no_help = arrival_rate * throughput_no_help

throughput_with_help = (
    1 - normalized_load ** (num_channels + max_queue)
) / (
    1 - normalized_load ** (num_channels + max_queue + 1)
)
absolute_throughput_with_help = arrival_rate * throughput_with_help

# Графики опять же такие себе, но сделал всё, что мог
parameters = {
    'Относительная пропускная способность без взаимопомощи': throughput_no_help,
    'Абсолютная пропускная способность без взаимопомощи': absolute_throughput_no_help,
    'Относительная пропускная способность с равномерной взаимопомощью': throughput_with_help,
    'Абсолютная пропускная способность с равномерной взаимопомощью': absolute_throughput_with_help
}

for title, value in parameters.items():
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(service_time, max_queue, value, alpha=0.8, cmap='viridis')
    ax.set_title(title)
    ax.set_xlabel('Среднее время обслуживания (мин)')
    ax.set_ylabel('Максимальная длина очереди')
    ax.set_zlabel('Значение')
    ax.set_zlim(0, np.nanmax(value))
    plt.show()
