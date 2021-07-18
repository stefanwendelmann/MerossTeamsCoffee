TODO

## Build

```shell
docker build -t itout/meross-teams-coffee:0.0.5 .
```

## Run

Test Local

```shell
docker run --rm -e MEROSS_EMAIL=example@gmail.com \
-e MEROSS_PASSWORD=StrongPw! \
-e TEAMS_WEBHOOK=https://webhook.site/c8966e4b-9072-4275-ab66-4c2bf12f60a2 \
-e MESSAGE_START=Test \
-e MESSAGE_END=Test2 itout/meross-teams-coffee:0.0.5
```

Server

```shell
docker run -it -e MEROSS_EMAIL=example@gmail.com \
-e MEROSS_PASSWORD=StrongPw! \
-e TEAMS_WEBHOOK=https://webhook.site/c8966e4b-9072-4275-ab66-4c2bf12f60a2 \
-e MESSAGE_START=Test \
-e MESSAGE_END=Test2 itout/meross-teams-coffee:0.0.5
```

## Environment Variables

| Variable  | Example |
|---|---|
|  MEROSS_EMAIL | example@gmail.com  |
| MEROSS_PASSWORD  | SuperStrong!  |
|  TEAMS_WEBHOOK | https://webhook.site/c8966e4b-9072-4275-ab66-4c2bf12f60a2  |
| MESSAGE_START | Der Kaffee läuft ! Fertig in ca. 15 min. |
| MESSAGE_END | Der Kaffee ist fertig ! Bitte neuen kochen, wenn er leer ist ! |
