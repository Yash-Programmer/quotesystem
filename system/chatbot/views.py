from django.shortcuts import render
import openai
# Create your views here.
def chatbot(request):
    openai.api_key = "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"
    context = {}
    if request.method == "POST":
        question = request.POST.get("question", "None")
        print(question)
        question_ = [
            {"role": "user", "content": question},
        ]
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=question_)
        reply = chat.choices[0].message.content
        print("reply" + reply)
        context = {
            "question": question,
            "answer": reply,
        }
    return render(request, 'chatbot.html', context)