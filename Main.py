import gradio as gr
import openai
import os

# Preluarea cheii API din .env
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable before running the script.")
# Functie de interactiune cu cheia API a OPENAI (foloseste modelul gratuit GPT-3.5)
def ask_gpt3(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", # Setare model
            messages=[
                {"role": "system", "content": "You are a helpful assistant specialized in generating personalized diet plans in romanian language, specifying grammages and macro for each food, total macro for each day. Specify also the sources you took for creating the diet and calculate the total calories for maintenance for each day using the formula: total_calories_of_maintenance=2*15*weight. From that, add 500 calories for bulking and substract 300 calories for cutting."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=512,
            temperature=0.7,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"An error occurred: {e}"

# Functie de generare a planulului dietei
def generate_diet_plan(food_prefs, restrictions, budget, height, weight, goals, preferences):
    try:
        prompt = (
            f"Create a detailed diet plan considering the following information:\n"
            f"- Food Preferences: {food_prefs}\n"
            f"- Dietary Restrictions: {restrictions}\n"
            f"- Weekly Budget: ${budget}\n"
            f"- Height: {height} cm\n"
            f"- Weight: {weight} kg\n"
            f"- Fitness Goals: {goals}\n"
            f"- Additional Preferences: {preferences}\n\n"
            f"Provide a day-by-day breakdown including meal options, portion sizes, and estimated calorie intake."
        )
        diet_plan = ask_gpt3(prompt)  # Foloseste GPT-3.5
        return diet_plan
    except ValueError as ve:
        return f"Input error: {ve}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Interfata Gradio
iface = gr.Interface(
    fn=generate_diet_plan,
    inputs=[
        gr.Textbox(label="Preferinte (exemplu: Oua + vita la micul dejun)"),
        gr.Textbox(label="Intolerante/Restrictii (exemplu: nu am, intoleranta la lactoza, intoleranta la gluten)"),
        gr.Number(label="Buget saptamanal (in RON)"),
        gr.Number(label="Inaltime (in cm)"),
        gr.Number(label="Greutate (in kg)"),
        gr.Dropdown(label="Obiective", choices=["Slabire", "Mentinere", "Ingrasare"]),
        gr.Textbox(label="Preferinte aditionale (exemplu: High protein, Low carb)"),
    ],
    outputs="text",
    title="Diet-Planner",
    description="Genereaza o dieta personalizata, bazata pe cererile tale!",
    examples=[
        ["Vegetarian", "Nu am", 450, 170, 65, "Slabire", "High protein"],
        ["Non-vegetarian", "Intoleranta la lactoza", 70, 165, 70, "Mentinere", "Dieta Keto"],
    ],
)

# Rulare
if __name__ == "__main__":
    iface.launch()