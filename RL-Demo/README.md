# RL-Demo

Reinforcement learning notebooks using [Stable Baselines 3](https://stable-baselines3.readthedocs.io/), Gymnasium, and PyTorch.

## Prerequisites

- Python 3.10+
- `make`

## Setup

```bash
make setup
source venv/bin/activate
```

This creates a virtual environment in `venv/` and installs dependencies from `requirements.txt`.

To reinstall or update packages after changing requirements:

```bash
make install
```

To remove the virtual environment and cache files:

```bash
make clean
```

Run `make help` to see all available commands.

## Notebooks

| Notebook | Description |
|----------|-------------|
| `Main Course.ipynb` | Core RL course material |
| `Project 1-Breakout.ipynb` | Breakout game with Atari |
| `Project 2 - Self Driving.ipynb` | Self-driving environment |
| `Project 3 - Custom Environment.ipynb` | Custom Gymnasium environment |

Open a notebook in Jupyter or VS Code and select the `venv` Python kernel.

## Links Mentioned
Stable Baselines 3: https://stable-baselines3.readthedocs...
OpenAI Gym: https://gym.openai.com/
PyTorch: https://pytorch.org/
Atarimania ROMs: http://www.atarimania.com/roms/Roms.rar
Swig: http://www.swig.org/Doc1.3/Windows.html
