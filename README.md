# For Temp.py

Create a virtual env on the RPi.

```
$ python3 -m venv venv
```

Install dependencies.

```
(venv) $ pip install Adafruit-CharLCD
```

```
(venv) $ pip install RPi.GPIO
```

Run the program.

```
(venv) $ sudo python3 temp.py
```

## Run GPIO as non root

https://raspberrypi.stackexchange.com/questions/40105/access-gpio-pins-without-root-no-access-to-dev-mem-try-running-as-root