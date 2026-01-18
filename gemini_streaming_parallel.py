import asyncio
import os
from typing import List, AsyncIterator

import google.genai as genai


class GeminiProcessor:
    """
    This class is your gateway to Gemini's AI magic. Think of it as the trusty
    (and slightly sassy) assistant that handles all API calls, from conjuring up
    the client to making the AI spit out text. Handle with care, it has feelings... 
    probably.
    """

    def __init__(self, model_name: str = "gemini-1.5-flash"):
        """
        This is the constructor – Python's way of saying 'Let's make a new object!'
        when you do `GeminiProcessor()`. It sets up your AI assistant with a
        specific model (`model_name`). Defaulting to `gemini-1.5-flash` because
        it's the cool kid on the block. If you change `model_name` to something
        obscure, don't blame us when it throws a tantrum.

        The `__init__` method is a special method in Python classes that is
        automatically called when a new instance of the class is created. It is used to
        initialize the attributes of the object.

        Args:
            model_name (str, optional): The name of the Gemini model to use.
                                        Defaults to "gemini-1.5-flash".
        """
        self.model_name = model_name
        # The Gemini client is initialized here. It plays nice with the
        # `GEMINI_API_KEY` environment variable for authentication.
        # If you forget to set it... well, let's just say `genai.Client()` is
        # very particular and will throw a fit. Don't say we didn't warn you.
        try:
            self.client = genai.Client()
        except Exception as e:
            print("Failed to initialize Gemini Client. Please make sure the `GEMINI_API_KEY` environment variable is set.")
            print("It's like forgetting your keys before going on a road trip. Expect consequences.")
            raise e

    async def stream_generate(self, prompt: str) -> AsyncIterator[str]:
        """
        This method generates text from a given prompt and streams the response.
        Streaming allows the response to be received in chunks as it is being
        generated, which is useful for real-time applications. It's like getting
        an essay sentence by sentence instead of waiting for the whole novel.

        An `AsyncIterator` is an iterator that can be used in an `async for` loop.
        It's designed to work with asynchronous code, meaning it doesn't block
        the program while waiting for data.
        """
        try:
            # We call `generate_content` with `stream=True`. This tells the AI:
            # 'Don't just blab it all out at once, give me dribbles of wisdom as
            # you think of them!' It returns an iterator that blesses us with
            # response chunks as they're ready. Sneaky, right?
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                stream=True
            )
            # We loop through the AI's stream of consciousness, yielding each
            # precious chunk of text. `yield`? That's Python's way of saying
            # 'I'm a generator, not a function that returns one thing and then quits.'
            # It's like a magical conveyor belt for data, one piece at a time.
            for chunk in response:
                yield chunk.text
        except Exception as e:
            # If the AI gets confused, throws a tantrum, or just decides to ghost you,
            # this `except` block is here to catch the falling pieces. It'll print an
            # error so you know who to blame (hint: probably your prompt) and yield
            # a friendly 'Error: {e}' message. Because blaming the AI is so last year.
            print(f"An error occurred while generating text: {e}")
            yield f"Error: {e}"


async def parallel_generate(processor: GeminiProcessor, prompts: List[str]):
    """
    This function orchestrates the generation of text for multiple prompts
    concurrently using `asyncio`. Parallel processing allows multiple requests
    to be sent to the API simultaneously, potentially speeding up the overall
    process significantly. Why wait for one thing at a time when you can have
    multiple AI brains working at once?

    `asyncio` is Python's library for writing concurrent code using the `async/await`
    syntax, enabling non-blocking operations.
    """
    # We're creating a list of `asyncio.Task` objects here. A task is just a
    # fancy way of saying 'a piece of code that `asyncio` is going to run for us'.
    # Think of it as assigning a mini-job to `asyncio`'s overworked event loop.
    tasks = [asyncio.create_task(stream_and_print(processor, prompt, i)) for i, prompt in enumerate(prompts)]

    # `asyncio.gather` is the conductor of our asynchronous orchestra. It takes
    # all the tasks we've lined up and makes them play (or fail) together.
    # It won't return until every last one of them has finished its solo performance,
    # or spectacularly crashed.
    await asyncio.gather(*tasks)


async def stream_and_print(processor: GeminiProcessor, prompt: str, index: int):
    """
    This helper function streams the AI's response and prints it to your console.
    It's the friendly face of the `GeminiProcessor`, making sure you see the
    text as it arrives, prompt by prompt. It also prints the prompt header and
    footer, so you know which AI rambling belongs to which of your brilliant
    (or hilariously mundane) prompts.
    """
    print(f"--- Prompt {index + 1}: {prompt} ---")
    response_stream = processor.stream_generate(prompt)
    # Here we use `async for` to iterate over the `AsyncIterator` from
    # `stream_generate`. It's like a regular `for` loop, but polite and waits
    # its turn, which is crucial when dealing with asynchronous operations like
    # receiving streamed data. It patiently waits for each chunk of text to arrive.
    async for chunk in response_stream:
        # `end=""` ensures each chunk prints right after the last, making one
        # coherent sentence (or paragraph, if you're lucky). `flush=True`?
        # That's the secret sauce that forces Python to show you the text *immediately*,
        # not hold onto it like a miser hoarding gold. Crucial for that real-time feel!
        print(f"Prompt {index + 1}: {chunk}", end="", flush=True)
    print(f"\n--- End of Prompt {index + 1} ---\n")


async def main():
    """
    This is where the whole show begins. It's the `main` function, the script's
    starting point. We'll initialize our AI buddy (`GeminiProcessor`), give it
    a list of profound (or profoundly silly) prompts, and then unleash the
    parallel processing beast (`parallel_generate`). Prepare for output!
    """
    print("Initializing Gemini Processor...")
    processor = GeminiProcessor()

    prompts = [
        "Tell me a joke about a developer who is trying to center a div.",
        "Write a short story about a rubber duck who is having an existential crisis.",
        "Explain the meaning of life in one sentence, but make it sound like a threat.",
        "Write a passive-aggressive error message for a user who forgot to save their work.",
    ]

    print("Starting parallel generation...")
    await parallel_generate(processor, prompts)
    print("All tasks are complete. Now go and do something useful with your life (or at least grab a coffee).")


if __name__ == "__main__":
    # This `if __name__ == "__main__":` block is your script's entry point.
    # Think of it as the 'main' function in other languages.
    # It ensures the code here only runs when you execute this file directly
    # (e.g., `python gemini_streaming_parallel.py`), not when it's imported elsewhere.
    # 
    # `asyncio.run(main())` is the command that kicks off the entire asynchronous operation.
    # It starts the asyncio event loop, runs your `main()` coroutine, and then cleans up.
    # Basically, it tells Python: 'Go, run the show, and don't come back until it's over!'
    asyncio.run(main())
