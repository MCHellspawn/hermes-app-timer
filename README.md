# Rhasspy Timer Skill (Rhasspy_App_Timer)

A skill for [Rhasspy](https://github.com/rhasspy) that provides various timer related intents including creating new timers, getting the remaining time on existing timers, and stopping a timer. This skill is implemented as a Hermes app and uses the [Rhasspy-hermes-app](https://github.com/rhasspy/rhasspy-hermes-app) library. The script can be run as a service, or as a docker container (recommended). 

## Installing

Requires:
* rhasspy-hermes-app 1.1.2

### In Docker:
To install, clone the repository and execute docker build to build the image.

Basic Timer:
```bash
git clone https://github.com/MCHellspawn/hermes-app-timer.git
mv hermes-app-timer/dockerfile-basic hermes-app-timer/dockerfile
sudo docker build hermes-app-timer -t <image_name>
```

Advanced Timer:
```bash
git clone https://github.com/MCHellspawn/hermes-app-timer.git
mv hermes-app-timer/dockerfile-advanced hermes-app-timer/dockerfile
sudo docker build hermes-app-timer -t <image_name>
```

### In Rhasspy:
This skill requires no additional setup in Rhasspy except addding sentences. See senetence.ini for sample english senteces.

## Using

Build a docker container using the image created above.

Bind the config volume <path/on/host>:/app/config

```bash
sudo docker run -it -d \
        --restart always \
        --name <container_name> \
        -e "MQTT_HOST=<MQTT Host/IP>" \
        -e "MQTT_PORT=<MQTT Port (Typically:1883)" \
        -e "MQTT_USER=<MQTT User>" \
        -e "MQTT_PASSWORD=<MQTT Password>" \
        <image_name>
```

The following intents are implemented on the hermes MQTT topic:

```ini
[AdvTimerStart]

[AdvTimerStop]

[AdvTimerTimeRemaining]
```

## To-Do

* Clean up install process
* More intents
  * Timer stuff <any ideas?>