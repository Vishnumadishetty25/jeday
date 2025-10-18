from openai import OpenAI


class FrontendAgent:
    def __init__(self, client: OpenAI, model_name="phi3:mini"):
        self.client = client
        self.model_name = model_name

    def handle_task(self, description: str):
        prompt = f"You are a frontend engineer. Generate HTML/CSS/React code for this task: {description}"

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return {
            "agent": "frontend",
            "task": description,
            "code": response.choices[0].message.content
        }
