import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(prompt, model="gpt-4o-mini", max_tokens=2000):
    response = client.chat.completions.create(
        model=model,
        # O parâmetro messages é uma lista com o histórico da conversa
        # Como queremos recomeçar sempre da saída anterior gerada pela LLM, não mantemos o histórico
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.1 # Controla o grau de criatividade. Devemos deixar rígido assim?
    )
    # O modelo retorna a(s) resposta(s) em uma lista
    # O parâmetro n, que controla o número de respostas, é configurado com 1 por padrão
    return response.choices[0].message.content
