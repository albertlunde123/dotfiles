import openai
import json
import pynvim

openai.api_key = "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"

@pynvim.plugin
class GPT4Plugin:
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.function("GPT4Complete", sync=True)
    def complete(self, args):
        prompt = args[0]
        completions = self.generate_completions(prompt)
        return completions

    def generate_completions(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=50,
            n=5,
            stop=None,
            temperature=0.9,
        )
        choices = response["choices"]
        completions = [choice["message"]["content"].strip() for choice in choices]
        return completions

    # @pynvim.function("GPT4Ask", sync=True)
    # def gpt4_ask(self, args):
    #     prompt = args[0]
    #     answers = self.generate_completions(prompt)
    #     # self.nvim.api.echo([(f"Answers: {answers}",)], True, {})  # Add this line to display the answers in Neovim
    #     # joined_answers = "\n".join(answers)
    #     self.nvim.api.echo([(f"Answers: {json.dumps(answers)}",)], True, {})  # Add this line to display the answers in Neovim

    #     # return f"{{{', '.join([f'\"{answer}\"' for answer in answers])}}}"
    #     return json.dumps([answer if answer is not None else "" for answer in answers])

        # return json.dumps(answers)
        # return joined_answers

    @pynvim.function("GPT4Ask", sync=True)
    def gpt4_ask(self, args):
        prompt = args[0]
        answers = self.generate_completions(prompt)
        # self.nvim.api.echo([(f"Answers: {answers}",)], True, {})  # Add this line to display the answers in Neovim
        json_string = json.dumps([answer if answer is not None else "" for answer in answers])
        print(f"JSON string: {json_string}")
        print("---")
        return json_string
        # print(gpt4_ask("hello", "hello"))
