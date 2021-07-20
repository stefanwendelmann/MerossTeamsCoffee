## TODO's / Ideas

- Wann wurde Kaffee gekocht, in DB schreiben
- Aktueller Status der Kaffeemaschnine in DB schreiben
- Grafana Dashboard über die DB

## Build

```shell
docker build -t docker.itout.de/iot/meross-teams-coffee:1.0.0 .
docker push docker.itout.de/iot/meross-teams-coffee:1.0.0
```

## Update DB
````shell
alembic upgrade head
````
## Run

Test Local

```shell
docker run --rm -e MEROSS_EMAIL=example@gmail.com \
-e MEROSS_PASSWORD=StrongPw! \
-e TEAMS_WEBHOOK=https://webhook.site/c8966e4b-9072-4275-ab66-4c2bf12f60a2 \
-e MESSAGE_START=Test \
-e MESSAGE_END=Test2 itout/meross-teams-coffee:1.0.0
```

Server

```shell
docker run -it -e MEROSS_EMAIL=example@gmail.com \
-e MEROSS_PASSWORD=StrongPw! \
-e TEAMS_WEBHOOK=https://webhook.site/c8966e4b-9072-4275-ab66-4c2bf12f60a2 \
-e MESSAGE_START=Test \
-e MESSAGE_END=Test2 itout/meross-teams-coffee:1.0.0
```

## Environment Variables

| Variable  | Example |
|---|---|
|  MEROSS_EMAIL | example@gmail.com  |
| MEROSS_PASSWORD  | SuperStrong!  |
| MEROSS_DEVICE_NAME | Name of the Device set inside the Meross App, if there are multiple devices with the same, this app will use the first found  |
| TEAMS_WEBHOOK | https://webhook.site/c8966e4b-9072-4275-ab66-4c2bf12f60a2  |
| MESSAGE_START | Der Kaffee läuft ! Fertig in ca. 15 min. |
| MESSAGE_END | Der Kaffee ist fertig ! Bitte neuen kochen, wenn er leer ist ! |
