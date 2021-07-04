# Configuration file options

Configuration files contain the following options:

## `network`

`ip`

The ip address of the robot (e.g. 10.0.0.3). The WebSocket server and client will attempt to bind to this address.

It can be set to '*' to bind to any available address.

## `control`

`default_speed`

Default speed between 1 and 8.

## `motors`

`type`

Type of motor connection to use. Available options:

- `dynamixel` for Dynamixel AX-series servos
- `sabertooth` for Sabertooth motor controllers
- `virtual` for a virtual motor connection (for testing)

Additional motor connection handlers can be added by following the instructions in [extending.md](/extending.md?id=adding-new-motors)

`port`

Serial port to connect over (e.g. `/dev/ttyACM0`).

_Not required for virtual connection._

`baudrate`

Baud rate to connect to the specified serial port with.

_Not required for virtual connection._

`ids`

Configure Dynamixel ID assignment for each motor group. Currently only `left` and `right` groups are supported which define which servos are on the left and right side. Each group is a list, allowing for multiple motors.

_Only required for Dynamixel connection._

`channels`

Configure the serial channel/s in use for each side of the robot. Currently only `left` and `right` groups are supported which define which motor channels are on the left and right side. Each group is a list, allowing for multiple motor channels.

_Only required for Sabertooth connection._

## `interface`

### `notifications`

Configures the toast notifications in the interface.

`enabled`

Enable or disable toast notifications outright.

`timeout`

The duration toasts are displayed for (or timeout).

As with all configuration settings, they take effect after a configuration file has been loaded, so some toasts may still display after a restart before the new configuration file has been received.

### `cameras`

For each camera, if the `enabled` option is set, it will be shown on the interface. The URL that the interface will attempt to load the camera stream from is defined in the `id` option. Note that these settings don't modify the Motion settings, and are meant to be set to whatever has been set in the relevant Motion config files.

Example for the front camera:

```yaml
front:
  enabled: true
  id: 1
```

### `graphs`

An array of graph definitions.

`uid`

Used by the interface to determine whether to show a sensor's data on any one graph. This should be set to a unique value.

`type`

The type of graph to use. This is determined by the graph selected from the dropdown list.

`enabled`

A graph can be enabled or disabled without having to delete its definition.

`location`

Where on the interface the graph should display. Common values are listed, including  `#btm_view_sensors`, `#left_view_sensors` or `#right_view_sensors`

`title`

The pretty title to display on the graph.

#### Other

Some graphs may require additional fields specific to the type of graph. Refer to individual documentation provided in the config schema.

### Theme

Allows the customisation of how the SIGHTS interface appears.

#### Accent Colour

Change the accent colour of the interface to a different colour using a hexadecimal colour code.

## `sensors`

Array of sensors. Each sensor can have a number of different configuration options but for every sensor, the required fields are:

`type`

The type of sensor (i.e. the model name). This is determined by the sensor selected from the dropdown list.

`enabled`

Whether or not the sensor is enabled.

`name`

The pretty display name. Some graphs, such as the line graph, may use this to label individual lines.

`period`

How often the sensor is polled (in seconds).

`display_on`

An array of graph `unique id`s to display the sensor's data on.

Some sensors will have an additional options such as an `address` option to set the I²C address.

## `debug`

`log_level`

Takes one of the following string values, to specify the log types that are shown in the log file and log window. Anything lower than the specified level is not logged.

- `critical`
- `error`
- `warning`
- `info` (_default_)
- `debug`

`print_messages`

Log any messages received from the interface, and any data received from the sensors to be sent to the interface.
