import ollama 

msg = 'generate an innovative prompt.'


refew = ollama.chat(model='llama2', messages=[{'role': 'user', 'content': msg}])


print(refew)                    
