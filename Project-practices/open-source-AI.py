from openai import OpenAI

local_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

reply = local_client.chat.completions.create(model="llama3.2:3b", 
    messages=[
        {"role": "system", "content": "You are a helpful assistant that can answer questions about AWS."},
        {"role": "user", "content": "Explain what AWS is in one sentence."}
    ])
print(reply.choices[0].message.content)









