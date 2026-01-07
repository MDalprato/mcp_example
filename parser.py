from dotenv import load_dotenv
load_dotenv()

import json
from openai import OpenAI

# =========================
# CLIENT
# =========================
client = OpenAI()


def extract_json(text: str) -> str:
    """
    Rimuove eventuali code fence ```json ... ```
    e restituisce solo il JSON puro
    """
    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        # rimuove prima e ultima riga ``` / ```json
        return "\n".join(lines[1:-1])

    return text


# =========================
# PROMPT DI SISTEMA
# =========================
SYSTEM_PROMPT = """
Sei un assistente che estrae informazioni strutturate da richieste in linguaggio naturale.

Dato l'input dell'utente, estrai i seguenti campi se presenti:
- azione (es. cerca, mostra, trova)
- oggetto (es. auto, persona, camion)
- colore
- ora_inizio (formato HH:MM)
- ora_fine (formato HH:MM)
- telecamera (identificatore o colore)
- targa (formato SSSSSSS)

Se un campo non è presente o non è chiaramente deducibile, restituisci null.
Non inventare mai valori.
Rispondi ESCLUSIVAMENTE in formato JSON valido.
"""


# =========================
# FUNZIONE DI PARSING
# =========================
def parse_query(user_input: str) -> dict:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    raw_output = response.output_text
    cleaned = extract_json(raw_output)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            "Output non valido JSON:\n"
            + cleaned
        ) from e

# VALIDAZIONE BASE (OPZIONALE)
# =========================
def validate_parsed_data(data: dict) -> bool:
    """
    Esempio di validazione minima:
    richiede almeno oggetto + telecamera
    """
    return (
        data.get("oggetto") is not None and
        data.get("telecamera") is not None
    )


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    print("🔎 Parser semantico attivo (CTRL+C per uscire)")

    while True:
        try:
            user_input = input("\n👤 Descrivi il misfatto: ")
            parsed = parse_query(user_input)

            print("\n📦 Dati estratti:")
            print(json.dumps(parsed, indent=2, ensure_ascii=False))

            if validate_parsed_data(parsed):
                print("\n✅ Query valida e pronta per l’esecuzione")
            else:
                print("\n⚠️ Dati incompleti: servono più informazioni")

        except KeyboardInterrupt:
            print("\n👋 Uscita")
            break

        except Exception as e:
            print("\n❌ Errore:", e)


#input example

#mi hanno rubato l'auto, era una fiat panda rossa targata fk455kk. il furto sospetto sia successo tra le 10 e le 11 del 10 dicembre. la telecamera è "atrio"