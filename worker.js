export default {
  async fetch(request, env) {
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    const body = await request.json();
    const question = body.question;
    const context = body.context;

    const prompt = "Sen Firat Universitesi yonetmeliklerinde uzman bir asistanisin. Asagidaki baglamı kullanarak soruyu yanıtla. Eger cevabi bulamazsan bilmedigini soyle. Kullanici hangi dilde sorarsa o dilde cevap ver.\n\nBaglam:\n" + context + "\n\nSoru: " + question + "\n\nCevap:";

    const groqRes = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "llama-3.1-8b-instant",
        messages: [{ role: "user", content: prompt }],
        temperature: 0.1,
        max_tokens: 1024
      })
    });

    const data = await groqRes.json();
    const answer = data.choices[0].message.content;

    return new Response(JSON.stringify({ answer: answer }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" }
    });
  }
};
