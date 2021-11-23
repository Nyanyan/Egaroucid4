# Build Dockerfile

## Quick Installation

```barh
docker pull ray255ar/egaroucid4_example
```

## Build

```bash
docker build --no-cache -t ray255ar/egaroucid4_example .
```

## Install
```bash
docker run --rm -it -p 5000:5000 ray255ar/egaroucid4_example python3 app.py
```