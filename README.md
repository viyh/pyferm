# pyferm

Simple Python homebrew/fermentation controller

The intent is to be a fermentation control, defined by a simple
YAML configuration file and easily expandible with plugins.

![Pyferm Components](pyferm_components.png?raw=true "Pyferm Components")

The high level components include:

* **sensors** - A device that is able to provide one or more metrics.
* **metrics** - A specific value provided by a sensor such as temperature,
humidity, pH, or gravity. Metrics can be used to make decisions for steps or controls.
* **outputs** - sensor data can be sent to an output destination, such as a CSV file,
database, or an HTTP request to be able to integrate with third parties such
as Brewfather or Brewer's Friend.
* **steps** - The ordered logic of the brewing process. Each step has conditions
that must be met before the step is completed. Additionally, a step may have
actions that take place in order to control the environment of the fermentation process.
* **conditions** - Conditions must be met in order for a brew step to be completed.
Any sensor metric data can be used for the condition such as waiting for a duration
of time, getting below a certain gravity, or reaching a temperature.
* **actions** - Actions are used during a brew step as a method to control the
environment of the fermentation process while the step is waiting to meet conditions.
Actions have a metric that is used to trigger high or low controls, such as holding
at a specific temperature or ramping the temperature up or down in steps by using
a heater and cooler configured as controls.
* **controls** - Devices that can be used to get sensor metrics into a range, such as
a heater and cooler to maintain a specific temperature, or a device that can add
sugar or acid in order to change gravity or pH.
