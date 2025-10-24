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

> **Hinweis:** Die Demo kommt ohne externe PyPI-Abhängigkeiten aus. Die Datei
> `requirements.txt` ist bewusst leer gehalten, damit der Installationsbefehl
> problemlos durchläuft und bei Bedarf künftig ergänzt werden kann.

Alternativ lässt sich die Installation auch über `make install` anstoßen (siehe unten).

## Anwendung starten

Für eine kurze Demo steht ein kleines Skript zur Verfügung, das eine Konversation mit der Echo-Fähigkeit ermöglicht:

```bash
make run
```

Das Skript begrüßt dich, nimmt deine Eingabe entgegen und antwortet mit derselben Nachricht. Der Gesprächsverlauf wird im In-Memory-Speicher abgelegt und nach dem Beenden (mit `exit`, `quit` oder `Strg+C`) nochmals ausgegeben.

### Beispiel-Dialog

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
