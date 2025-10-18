from openai import OpenAI


class BackendAgent:
    def __init__(self, client: OpenAI, model_name="phi3:mini"):
        self.client = client
        self.model_name = model_name

    def handle_task(self, description: str):
        prompt = f"You are a backend engineer. Generate Python Flask or Node.js code for this task: {description}"

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        return {
            "agent": "backend",
            "task": description,
            "code": response.choices[0].message.content
        }
