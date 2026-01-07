from dotenv import load_dotenv
load_dotenv()

import json
from openai import OpenAI

# =========================
# Client OpenAI
# =========================
client = OpenAI()

# =========================
# TOOL REALI (Python)
# =========================
def somma(a: float, b: float) -> float:
    return a + b


def send_email(to: str, subject: str, body: str) -> str:
    # Mock: qui potresti chiamare una vera API email
    print(f"\n📧 Email inviata a {to}")
    print(f"Oggetto: {subject}")
    print(f"Contenuto: {body}\n")
    return "Email inviata con successo"


# =========================
# DEFINIZIONE TOOL PER IL MODELLO
# =========================
tools = [
    {
        "type": "function",
        "name": "somma",
        "description": "Somma due numeri con precisione matematica",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["a", "b"]
        }
    },
    {
        "type": "function",
        "name": "send_email",
        "description": "Invia un'email a una persona",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {"type": "string"},
                "subject": {"type": "string"},
                "body": {"type": "string"}
            },
            "required": ["to", "subject", "body"]
        }
    }
]

# =========================
# INPUT UTENTE
# =========================
user_input = "Quanto fa 12.5 + 7.3 e poi mandami il risultato per email a Marco"

# =========================
# STEP 1: IL MODELLO PIANIFICA
# =========================
response = client.responses.create(
    model="gpt-4.1-mini",
    input=user_input,
    tools=tools
)

# =========================
# STEP 2: ESECUZIONE TOOL
# =========================
context = {}   # stato condiviso tra i tool
email_status = None

for item in response.output:
    if item.type == "function_call":
        args = json.loads(item.arguments)

        if item.name == "somma":
            risultato = somma(**args)
            context["risultato"] = risultato

        elif item.name == "send_email":
            body = f"Il risultato della somma è {context['risultato']}."
            email_status = send_email(
                to=args["to"],
                subject=args["subject"],
                body=body
            )

# =========================
# STEP 3: RISPOSTA FINALE
# =========================
final_response = client.responses.create(
    model="gpt-4.1-mini",
    input=(
        f"La somma calcolata è {context['risultato']}. "
        f"Stato invio email: {email_status}. "
        f"Rispondi in modo chiaro e cortese all’utente."
    )
)

print("🤖 Risposta finale:")
print(final_response.output_text)
