import json
import os
import gradio as gr
from groq import Groq

with open("firat_data.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

client = Groq(api_key="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")

def find_relevant_chunks(question, top_k=4):
    q = question.lower()
    words = [w for w in q.split() if len(w) > 2]
    scored = []
    for chunk in chunks:
        text = chunk["text"].lower()
        score = sum(1 for w in words if w in text)
        if score > 0:
            scored.append((score, chunk["page"], chunk["text"]))
    scored.sort(reverse=True)
    return scored[:top_k]

def ask(question, history):
    relevant = find_relevant_chunks(question)
    if relevant:
        context = "\n\n".join([f"[Sayfa {r[1]}]: {r[2]}" for r in relevant])
    else:
        context = "Ilgili bilgi bulunamadi."

    prompt = f"""Sen Firat Universitesi yonetmeliklerinde uzman bir asistanisin.
Asagidaki baglamı kullanarak soruyu yanıtla.
Eger cevabi bulamazsan bilmedigini soyle.
Kullanici hangi dilde sorarsa o dilde cevap ver.

Baglam:
{context}

Soru: {question}

Cevap:"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=1024
    )
    return response.choices[0].message.content

demo = gr.ChatInterface(
    fn=ask,
    title="🎓 Fırat-GPT",
    description="Fırat Üniversitesi yönetmelikleri hakkında soru sorun.",
    examples=[
        "Form-30 nedir?",
        "Yüksek lisans jüri sayısı?",
        "ما هو نموذج Form-30؟"
    ]
)

demo.launch()