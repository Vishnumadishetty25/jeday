from openai import OpenAI
from agents.frontend_agent import FrontendAgent
from agents.backend_agent import BackendAgent
import json


class CoordinatorAgent:
    def __init__(self, client: OpenAI, model_name="phi3:mini"):
        self.client = client
        self.model_name = model_name
        self.frontend_agent = FrontendAgent(client, model_name)
        self.backend_agent = BackendAgent(client, model_name)

    def process_brief(self, brief: str):
        prompt = f"""
        You are an AI project manager. Break this project brief into specific, detailed technical tasks.
        Assign each to either a frontend or backend developer.
        Respond in JSON format:
        [
          {{ "description": "task detail", "agent": "frontend" }},
          {{ "description": "task detail", "agent": "backend" }}
        ]

        Brief: {brief}
        """

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            top_p=0.9,
        )

        try:
            tasks = json.loads(response.choices[0].message.content)
        except Exception:
            tasks = [{"description": "Implement basic UI", "agent": "frontend"}]

        results = []
        for task in tasks:
            if task["agent"].lower() == "frontend":
                results.append(
                    self.frontend_agent.handle_task(task["description"]))
            else:
                results.append(
                    self.backend_agent.handle_task(task["description"]))

        return {"brief": brief, "tasks": tasks, "outputs": results}
