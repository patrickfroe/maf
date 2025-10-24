# maf-basic

Eine minimalistische Agenten-Demo, die zeigt, wie sich Speicher und Skills zu einem einfachen Chatbot kombinieren lassen. Die Anwendung registriert eine Echo-Fähigkeit, speichert den Gesprächsverlauf und eignet sich als Ausgangspunkt für eigene Experimente.

## Voraussetzungen

- Python 3.10 oder neuer
- Ein virtuelles Environment wird empfohlen (`python -m venv .venv`)

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Alternativ lässt sich die Installation auch über `make install` anstoßen (siehe unten).

## Anwendung starten

Für eine kurze Demo steht ein kleines Skript zur Verfügung, das eine Konversation mit einer registrierten Fähigkeit ermöglicht:

```bash
make run
```

Der Befehl startet `python -m maf_basic.cli`, begrüßt dich, nimmt deine Eingabe entgegen und ruft standardmäßig die `EchoSkill` auf. Der Gesprächsverlauf wird im In-Memory-Speicher abgelegt und nach dem Beenden (mit `exit`, `quit` oder `Strg+C`) nochmals ausgegeben.

### Beispiel-Dialog (EchoSkill)

```
$ make run
maf-basic demo – type a message and the agent will echo it back.
Press Ctrl+C or type 'exit' to quit.

You: Hallo Agent!
Agent: Hallo Agent!
You: Was machst du?
Agent: Was machst du?
You: exit

Conversation history saved in storage:
 1. Hallo Agent!
 2. Was machst du?
 3. exit
```

Über CLI-Argumente lässt sich das Verhalten anpassen:

- `--skill`: Wählt die auszuführende Fähigkeit (`EchoSkill`, `WebSearchSkill`, `ManagementSummarySkill`).
- `--exit-commands`: Legt eigene Befehle zum Beenden fest, z. B. `--exit-commands stop ende`.

```bash
python -m maf_basic.cli --skill EchoSkill --exit-commands stoppen tschüss
```

## Erweiterte Nutzungsbeispiele

### Websuche über die Kommandozeile

Die `WebSearchSkill` nutzt wahlweise das Paket `duckduckgo_search`. Installiere es bei Bedarf zusätzlich:

```bash
pip install duckduckgo_search
```

Starte die CLI anschließend mit der gewünschten Fähigkeit:

```
$ python -m maf_basic.cli --skill WebSearchSkill
Demo Agent CLI. Type your message and press enter. Type 'exit' to quit.
>> Aktuelle KI Trends
Suchergebnisse für 'Aktuelle KI Trends':
- KI Trend Report 2024 (https://beispiel.de/report): Überblick über die wichtigsten Entwicklungen.
- State of AI (https://beispiel.de/state-of-ai): Analyse zu Investitionen und Forschung.
```

Die angezeigten Ergebnisse werden intern gespeichert und stehen dadurch für weitere Verarbeitung zur Verfügung.

### Kombination mehrerer Fähigkeiten im eigenen Skript

In eigenen Python-Skripten lassen sich mehrere Fähigkeiten hintereinander nutzen, um zum Beispiel zunächst zu suchen und anschließend eine Management Summary zu erzeugen:

```python
from maf_basic.app import AgentApp
from maf_basic.skills import EchoSkill, ManagementSummarySkill, WebSearchSkill

app = AgentApp()
app.register_skill(EchoSkill())
app.register_skill(WebSearchSkill())
app.register_skill(ManagementSummarySkill(max_items=2))

query = "Aktuelle KI Trends"
print(app.invoke("WebSearchSkill", query))

print()
print(app.invoke("ManagementSummarySkill", query))
```

Innerhalb derselben `AgentApp` greifen alle Fähigkeiten auf denselben Speicher zu. Die Summary-Fähigkeit fasst daher direkt die zuvor abgelegten Suchergebnisse zusammen. Das Muster eignet sich auch, um eigene Fähigkeiten zu registrieren oder alternative Storage-Implementierungen zu testen.

## Tests ausführen

Die vorhandenen Unit-Tests verwenden `pytest` und lassen sich über folgenden Befehl starten:

```bash
make test
```

## Nützliche Makefile-Kommandos

| Befehl        | Beschreibung                                      |
| ------------- | -------------------------------------------------- |
| `make install`| Installiert die Abhängigkeiten via `pip`.          |
| `make run`    | Startet die interaktive Echo-Demo.                 |
| `make test`   | Führt die Tests mit `pytest` aus.                  |

Die Variablen des Makefiles sind so definiert, dass standardmäßig `python3` verwendet wird. Bei Bedarf lässt sich `PYTHON=/pfad/zum/python make run` verwenden.
