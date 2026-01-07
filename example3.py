from dotenv import load_dotenv
load_dotenv()

import json
import requests
from openai import OpenAI

import time
from openai import RateLimitError

def call_with_retry(fn, retries=5):
    for attempt in range(retries):
        try:
            return fn()
        except RateLimitError as e:
            wait = 5 * (attempt + 1)
            print(f"⏳ Rate limit, riprovo tra {wait}s...")
            time.sleep(wait)
    raise Exception("Troppi tentativi, riprova più tardi")



client = OpenAI()

# =========================
# TOOL: INVIO PRESTITO
# =========================
def submit_loan_request(
    name: str,
    age: int,
    monthly_income: float,
    amount: float,
    duration_months: int
) -> dict:
    """
    Mock POST verso API prestiti (Mokkala)
    """
    payload = {
        "name": name,
        "age": age,
        "monthly_income": monthly_income,
        "amount": amount,
        "duration_months": duration_months
    }

    print("\n📡 POST verso API prestiti:")
    print(json.dumps(payload, indent=2))

    # MOCK RESPONSE
    return {
        "status": "approved",
        "rate": 4.2,
        "message": "Prestito approvato"
    }


# =========================
# TOOL DEFINITIONS
# =========================
tools = [
    {
        "type": "function",
        "name": "submit_loan_request",
        "description": "Invia una richiesta di prestito al sistema centrale",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "monthly_income": {"type": "number"},
                "amount": {"type": "number"},
                "duration_months": {"type": "integer"}
            },
            "required": [
                "name",
                "age",
                "monthly_income",
                "amount",
                "duration_months"
            ]
        }
    }
]

# =========================
# STATO CONVERSAZIONE
# =========================
state = {
    "name": None,
    "age": None,
    "monthly_income": None,
    "amount": None,
    "duration_months": None
}

# =========================
# PROMPT DI SISTEMA
# =========================
system_prompt = """
Sei un assistente che aiuta l’utente a richiedere un prestito.

L’utente può fornire le informazioni in qualsiasi ordine e forma.
Devi estrarre, se presenti:
- nome
- età
- reddito mensile
- importo richiesto
- durata in mesi

Se alcune informazioni mancano o non sono valide,
chiedi SOLO quelle mancanti, in modo conciso.
Nel caso in cui l'utente ti chieda se il prestito è possibile, rispondi di si in tono amichevole.

Quando tutte le informazioni sono presenti e valide,
richiedi l’invio della richiesta tramite il tool submit_loan_request.
Non inventare mai dati.

"""

messages = [
    {"role": "system", "content": system_prompt}
]

# =========================
# LOOP CHAT
# =========================
while True:
    user_input = input("\n👤 Utente: ")
    messages.append({"role": "user", "content": user_input})

    response = call_with_retry(
        lambda: client.responses.create(
            model="gpt-4.1-mini",
            input=messages,
            tools=tools
        )
    )
    tool_called = False

    for item in response.output:
        if item.type == "message":
            print("\n🤖 Assistente:", item.content[0].text)
            messages.append({"role": "assistant", "content": item.content[0].text})

        elif item.type == "function_call":
            tool_called = True
            args = json.loads(item.arguments)

            result = submit_loan_request(**args)

            messages.append({
                "role": "tool",
                "tool_name": item.name,
                "content": json.dumps(result)
            })

    if tool_called:
        break
