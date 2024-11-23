import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns

# Задання матриці переходів для поглинаючого ланцюга Маркова
# Кількість станів - 7, з яких 2 - поглинаючі (стани 6 і 7)
n_states = 7
P = np.array([
    [0.1, 0.3, 0.2, 0.2, 0.1, 0.05, 0.05],  # Стан 1
    [0.2, 0.1, 0.3, 0.2, 0.1, 0.05, 0.05],  # Стан 2
    [0.3, 0.2, 0.1, 0.3, 0.05, 0.05, 0],  # Стан 3
    [0.2, 0.3, 0.2, 0.1, 0.1, 0.05, 0.05],  # Стан 4
    [0.1, 0.2, 0.1, 0.2, 0.2, 0.1, 0.1],  # Стан 5
    [0, 0, 0, 0, 0, 1.0, 0],  # Стан 6 - поглинаючий
    [0, 0, 0, 0, 0, 0, 1.0]  # Стан 7 - поглинаючий
])

# Початковий розподіл вектора стану
initial_distribution = [0.2, 0.2, 0.2, 0.2, 0.2, 0.0, 0.0]


# Функція для моделювання поглинаючого ланцюга Маркова
def simulate_absorbing_chain(P, initial_distribution, n_realizations):
    realizations = []
    absorbing_times = []

    for _ in range(n_realizations):
        current_state = np.random.choice(len(initial_distribution), p=initial_distribution)
        trajectory = [current_state]
        steps = 0

        while current_state not in [5, 6]:
            current_state = np.random.choice(len(P), p=P[current_state])
            trajectory.append(current_state)
            steps += 1

        realizations.append(trajectory)
        absorbing_times.append(steps)

    return realizations, absorbing_times


# Змоделювати 100 реалізацій ланцюга Маркова до моменту поглинання
n_realizations = 100
realizations, absorbing_times = simulate_absorbing_chain(P, initial_distribution, n_realizations)

# Оцінка матриці переходів на основі реалізацій
transition_counts = np.zeros((n_states, n_states))
time_in_state = np.zeros(n_states)

for trajectory in realizations:
    for i in range(len(trajectory) - 1):
        transition_counts[trajectory[i], trajectory[i + 1]] += 1
        time_in_state[trajectory[i]] += 1
    time_in_state[trajectory[-1]] += 1  # Останній стан також враховується

# Врахування поглинаючих станів у матриці переходів
estimated_P = np.zeros_like(P)
for i in range(n_states):
    if transition_counts[i].sum() == 0:
        estimated_P[i, i] = 1.0  # Поглинаючий стан
    else:
        estimated_P[i] = transition_counts[i] / transition_counts[i].sum()

# Обчислення теоретичних характеристик ймовірностей поглинання
Q = P[:5, :5]  # Матриця переходів між непоглинаючими станами
R = P[:5, 5:]  # Матриця переходів з непоглинаючих станів до поглинаючих
I = np.eye(Q.shape[0])
N = np.linalg.inv(I - Q)  # Фундаментальна матриця
B = N @ R  # Ймовірності поглинання для кожного непоглинаючого стану до поглинаючих

# Теоретичні ймовірності поглинання для кожного поглинаючого стану
absorbing_probabilities_theoretical = B.mean(axis=0)  # Середнє значення ймовірностей поглинання

# Теоретичний середній час поглинання для кожного початкового стану
mean_absorbing_times_theoretical = N.sum(axis=1)
mean_absorbing_time_theoretical = mean_absorbing_times_theoretical.mean()  # Середній час поглинання для всіх початкових станів

# Обчислення експериментальних характеристик
absorbing_probabilities_experimental = time_in_state[[5, 6]] / np.sum(
    time_in_state[[5, 6]])  # Ймовірність поглинання (експериментальна)
mean_absorbing_time_experimental = np.mean(absorbing_times)  # Середній час поглинання (експериментальний)

# Візуалізація перших 5 реалізацій ланцюга Маркова
plt.figure(figsize=(12, 8))
for i, realization in enumerate(realizations[:5]):
    plt.plot(range(len(realization)), realization, marker='o', label=f'Realization {i + 1}')
plt.xlabel('Кроки')
plt.ylabel('Стан')
plt.title('Перші 5 реалізацій поглинаючого ланцюга Маркова')
plt.legend()
plt.grid()
plt.show()

# Візуалізація 100 реалізацій ланцюга Маркова
plt.figure(figsize=(12, 8))
for i, realization in enumerate(realizations):
    plt.plot(range(len(realization)), realization, alpha=0.1, color='blue')
plt.xlabel('Кроки')
plt.ylabel('Стан')
plt.title('100 реалізацій поглинаючого ланцюга Маркова')
plt.grid()
plt.show()

# Візуалізація матриці переходів
plt.figure(figsize=(10, 6))
sns.heatmap(P, annot=True, cmap='viridis', cbar=True)
plt.xlabel('Наступний стан')
plt.ylabel('Поточний стан')
plt.title('Матриця переходів поглинаючого ланцюга Маркова')
plt.show()

# Візуалізація початкового розподілу
plt.figure(figsize=(10, 6))
plt.bar(range(len(initial_distribution)), initial_distribution, color='b', alpha=0.7)
plt.xlabel('Стан')
plt.ylabel('Ймовірність')
plt.title('Початковий розподіл станів')
plt.grid(axis='y')
plt.show()

# Візуалізація оціненої матриці переходів
plt.figure(figsize=(10, 6))
sns.heatmap(estimated_P, annot=True, cmap='viridis', cbar=True)
plt.xlabel('Наступний стан')
plt.ylabel('Поточний стан')
plt.title('Оцінена матриця переходів на основі реалізацій')
plt.show()

# Візуалізація часу перебування у кожному стані
plt.figure(figsize=(10, 6))
plt.bar(range(n_states), time_in_state, color='g', alpha=0.7)
plt.xlabel('Стан')
plt.ylabel('Час перебування')
plt.title('Час перебування у кожному стані (експериментальний)')
plt.grid(axis='y')
plt.show()

# Візуалізація часу до поглинання
plt.figure(figsize=(10, 6))
plt.hist(absorbing_times, bins=15, color='r', alpha=0.7, edgecolor='black')
plt.xlabel('Час до поглинання')
plt.ylabel('Частота')
plt.title('Розподіл часу до поглинання')
plt.grid()
plt.show()

# Виведення результатів
for i, realization in enumerate(realizations[:5]):  # Виводимо перші 5 реалізацій для прикладу
    print(f'Realization {i + 1}: {realization}')

print("\nТеоретична матриця переходів:")
print(P)
print("\nОцінена матриця переходів на основі реалізацій:")
print(estimated_P)
print("\nСередній час до поглинання (експериментальний):", mean_absorbing_time_experimental)
print("\nСередній час до поглинання (теоретичний):", mean_absorbing_time_theoretical)
print("\nЙмовірності поглинання (теоретичні):", absorbing_probabilities_theoretical)
print("\nЙмовірності поглинання (експериментальні):", absorbing_probabilities_experimental)
