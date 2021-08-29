# pyferm

Simple Python homebrew/fermentation controller

The intent is to be a fermentation control, defined by a simple
YAML configuration file and easily expandible with plugins.

The high level components include:

* sensors - provide metrics in order to make decisions for steps or controls
* steps - ordered logic of the brewing process, such as holding at a specific,
    temperature for a duration or waiting until a sensor condition is met
* outputs - sensor data can be sent to an output destination, such as a CSV file,
    database, or an HTTP request to be able to integrate with third parties such
    as Brewfather or Brewer's Friend
* controls - devices that can be used to get sensor metrics into a range, such as
    a heater and cooler to maintain a specific temperature.
