# race-box
Single Board Computer based data logger and track mapper for race ops and simulations, built in python for simple extensibility, future C++ upgrade path.

this will only work on rasberypi style computers without having to majorly change serial pinouts:

TODO: add pinout mapping

clone repo
cd into first layer where main is visible

## usage

activate local venv with ```python -m venv venv```

ensure venv is running by checking which python is running

install requirements with ```pip install -r requirements.txt```

test local with ```python -m main```

compile:
```python
python -m nuitka \
  --standalone \
  --follow-imports \
  --enable-plugin=multiprocessing \
  --output-dir=build \
  racebox.py
```


