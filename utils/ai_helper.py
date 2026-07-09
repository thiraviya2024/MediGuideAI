from utils.llm import client

def ask_ai(vectorstore, question):

    # Retrieve the 3 most relevant chunks
    docs = vectorstore.similarity_search(question, k=3)

    # Combine retrieved text
    context = "\n\n".join([doc.page_content for doc in docs])

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI Hospital Document Assistant. "
                    "Answer ONLY using the provided document. "
                    "If the answer is not in the document, say "
                    "'I couldn't find that information in the uploaded document.'"
                )
            },
            {
                "role": "user",
                "content": f"Document:\n{context}\n\nQuestion: {question}"
            }
        ]
    )

    return response.choices[0].message.content
