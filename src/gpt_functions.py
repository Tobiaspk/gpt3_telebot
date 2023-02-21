import openai

def run_gpt3(prompt, model_engine="text-davinci-003", text_function=lambda x: x):
    """
    Text_function can modify the response before it is sent to the user without modifying the database or gpt.
    """
    # Run the prompt
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=210,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Get the response
    response = completions.choices[0].text

    # Store the message in the database
    return text_function(response)