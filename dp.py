from client import count, _pretty_print
from matplotlib import pyplot
import sys
import numpy as np

# Return a random sample from laplace with mean/loc = mu and scale/spread b.
def laplace(mu, b):
  # 使用 NumPy 的拉普拉斯采样
  return np.random.laplace(mu, b)

# Return a noised histogram that is epsilon-dp.
def dp_histogram(epsilon):
  # 1) 噪声分布参数
  sensitivity = 1.0      # 直方图 L1 敏感度
  mu = 0.0               # 拉普拉斯机制的均值
  b = sensitivity / float(epsilon)  # 拉普拉斯尺度参数

  # 2) 获取未加噪的直方图
  #   headers: ("age", "music", "count") 这样的列名
  #   rows:    列表，每行形如 (age, music, value)
  headers, rows = count(["age", "music"], False)

  # 3) 对每个计数加噪
  noised_rows = []
  for (age, music, value) in rows:
    noise = laplace(mu, b)        # 连续噪声
    noise_rounded = round(noise)  # 计数希望保持整数
    noised_value = value + noise_rounded

    # 可选：为了输出好看，不让负数出现（DP 不会变差，后处理是免费的）
    noised_value = max(0, int(noised_value))

    noised_rows.append((age, music, noised_value))

  return headers, noised_rows

# Plot the frequency of counts for the first group (age 0 and Hip Hop).
def plot(epsilon):
  ITERATIONS = 150
  d = {}
  for i in range(ITERATIONS):
    headers, rows = dp_histogram(epsilon)
    # 取第一行（示例里是 age 0 & Hip Hop；按你们数据顺序为准）
    value = round(rows[0][-1])
    d[value] = d.get(value, 0) + 1

  vmin, vmax = min(d.keys()) - 3, max(d.keys()) + 3
  xs = list(range(vmin, vmax + 1))
  ys = [d.get(x, 0) / ITERATIONS for x in xs]

  pyplot.plot(xs, ys, 'o-', ds='steps-mid')
  pyplot.xlabel("Count value")
  pyplot.ylabel("Frequency")
  pyplot.savefig('dp-plot.png')

if __name__ == "__main__":
  epsilon = 0.5
  if len(sys.argv) > 1:
    epsilon = float(sys.argv[1])

  print("Using epsilon =", epsilon)
  headers, rows = dp_histogram(epsilon)
  _pretty_print(headers, rows)

  # 如需画图，取消下面注释

  print("Plotting, this may take a minute ...")
  plot(epsilon)
  print("Plot saved at 'dp-plot.png'")

