# differential-privacy-practice
Differential Privacy in Practice using Python

This project implements **Differential Privacy (DP)** using the **Laplace Mechanism** to protect user data in histogram-style queries. It is inspired by applied privacy engineering labs in DS 593 (Privacy-Conscious Computer Systems).

The goal: enable data analytics while ensuring that **no single user’s data can be inferred** from the output, even by a strong adversary.

## Differential Privacy Mechanism

This project implements the **Laplace Mechanism** for a histogram query:

noised_value = true_count + Laplace( mean = 0, scale = Δf / ε )

- Global sensitivity: **Δf = 1**
- Laplace noise sampling:

```python
np.random.laplace(mu, b)
```

Core logic excerpt from dp.py:

noise = np.random.laplace(mu, b)
noise_rounded = round(noise)
noised_value = max(0, int(value + noise_rounded))

## Repository Structure

.
├── dp.py                # DP histogram generation and plotting
├── client.py            # Data counting utilities
├── composition.py       # (optional) privacy budget composition helpers
├── budget.py            # (optional) epsilon accounting
├── dp-plot.png          # Sample output visualization
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation

### Install dependencies
```python
pip install -r requirements.txt
```
### Run a DP histogram
```python
python dp.py 0.5
```
Example output:

Using epsilon = 0.5
Plotting, this may take a minute ...
Plot saved at 'dp-plot.png'

### Author
Yuki Li (Data Science | Privacy & Trust & Safety)
If you use this project or want to collaborate on privacy engineering, feel free to reach out!
