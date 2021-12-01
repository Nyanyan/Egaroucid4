# Egaroucid 4 - Othello AI



## Abstract

Egaroucid 4 is an Othello AI.

**You can [play this AI on the Web](https://www.egaroucid.nyanyan.dev/).**

There are former versions:

https://github.com/Nyanyan/Reversi

https://github.com/Nyanyan/Egaroucid

https://github.com/Nyanyan/Egaroucid3

![img0](https://github.com/Nyanyan/Egaroucid4/blob/main/img/img.png)



## Requirements

### Languages

* Python3
* C++

### Additional Python libraries

* subprocess
* tkinter

### Additional C++ libraries

None



## How to use

First, you have to clone this repository. For example,

```
$ git clone git@github.com:Nyanyan/Egaroucid4.git
```

Then move to the ```src``` directory

```
$ cd Egaroucid4/src
```

Compile ```egaroucid4.cpp```

```
$ g++ egaroucid4.cpp -O3 -march=native -fexcess-precision=fast -funroll-loops -flto -mtune=native -lpthread -Wall -o egaroucid4.out
```

Execute ```main.py```

```
$ python3 main.py
```

Then choose which color AI play. 0 for black, 1 for white

```
AI moves (0: black 1: white): 
```

Press ```Start``` button to play!