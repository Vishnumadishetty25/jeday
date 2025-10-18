import tkinter as tk
from tkinter import scrolledtext, messagebox
from openai import OpenAI
from dotenv import load_dotenv
import os
from agents.coordinator_agent import CoordinatorAgent

load_dotenv()


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


def test_ollama_connection():

    models_to_try = [
        "phi3:mini"
    ]

    for model in models_to_try:
        try:
            print(f" Trying model: {model}")
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Say 'Hello'"}],
                max_tokens=10
            )
            print(f" {model} works!")
            return model
        except Exception as e:
            print(f"  {model} failed: {e}")
            continue

    messagebox.showerror(
        "No Compatible Models",
        "Please download a smaller model:\n\n"
        "Run in terminal:\n"
        "ollama pull phi3:mini\n\n"
        "Then restart this application."
    )
    return None


working_model = test_ollama_connection()
if not working_model:
    exit()

# GUI SETUP
root = tk.Tk()
root.title("Jeday the AI ")
root.geometry("900x600")
root.config(bg="#34a2eb")

# Widgets
title = tk.Label(root, text="Jeday the AI - Running Locally",
                 font=("Arial", 18, "bold"), bg="#34a2eb")
title.pack(pady=10)

brief_label = tk.Label(root, text="Enter your project brief:",
                       bg="#34a2eb", font=("Arial", 12))
brief_label.pack(anchor="w", padx=20)

brief_text = scrolledtext.ScrolledText(root, height=5, width=100, wrap=tk.WORD)
brief_text.pack(padx=20, pady=5)

output_label = tk.Label(root, text="Results:",
                        bg="#34a2eb", font=("Arial", 12))
output_label.pack(anchor="w", padx=20, pady=(10, 0))

output_text = scrolledtext.ScrolledText(
    root, height=20, width=100, wrap=tk.WORD)
output_text.pack(padx=20, pady=5)


def generate_plan():
    brief = brief_text.get("1.0", tk.END).strip()
    if not brief:
        messagebox.showwarning(
            "Missing Input", "Please enter a project brief first.")
        return

    try:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, " Starting analysis...\n")
        root.update()

        coordinator = CoordinatorAgent(client, working_model)

        output_text.insert(tk.END, " Breaking down tasks...\n")
        root.update()

        result = coordinator.process_brief(brief)

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, " Project Breakdown:\n")
        for t in result["tasks"]:
            output_text.insert(
                tk.END, f"- {t['agent'].title()}: {t['description']}\n")

        output_text.insert(tk.END, "\n Generated Code:\n")
        for r in result["outputs"]:
            output_text.insert(
                tk.END, f"\n=== {r['agent'].title()} Task: {r['task']} ===\n{r['code']}\n")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")


generate_button = tk.Button(root, text="Generate Plan", command=generate_plan,
                            bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
generate_button.pack(pady=10)

root.mainloop()
