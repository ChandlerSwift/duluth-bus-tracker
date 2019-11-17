# Duluth Bus Tracker 
### (For Keeping Track of Buses in Duluth)

Backend for the sign that is going to display where the buses are in Duluth!

Raspberry pi display uses ui.html to display information on bus times

[DTA bus API info](https://www.duluthtransit.com/home/doing-business/developer-resources/)

### Installation Notes
When installing, the lights are driven over PWM on GPIO12. This normally
requires root access to read/write `/dev/mem`. Instead, since it's difficult
to run some of the other components as root, we allow the user (`pi` in this
case) to write to `/dev/mem` by `chmod g+w /dev/mem; usermod -aG kmem pi`.

We also need `python3`, `pip(3)`, and `pipenv`:
```
sudo apt install python3 python3-pip
pip3 install pipenv
export PATH=$PATH:$HOME/.local/bin
sudo pipenv install # since we're running the pipenv as root, we need to install it as root
```
