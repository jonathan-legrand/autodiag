# imports
from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
from openrouter_agent import OpenRouterAgent, OpenRouterModel

client = None

patient_generator = """

You are an expert in computational psychiatry and prompt engineering. 
Your task is to generate a complete JSON file defining an **interactive psychological patient persona** 
for use in NLP-based therapy simulations.

Each patient is fictional but must demonstrate psychologically coherent symptoms and 
diagnoses drawn from the DSM-5.

The output must be a single JSON object with two top-level fields:

{
  "patient_profile": {
    "patient_id": "<unique ID>",
    "name": "<fictional patient name>",
    "age": <integer>,
    "gender": "<male | female | nonbinary | other>",
    "occupation": "<job or student status>",
    "background": "<short life history, family, social and occupational context>",
    "symptoms": [
      "<list of psychological and behavioral symptoms>"
    ],
    "DSM5_diagnoses": [
      {
        "disorder_code": "<DSM-5 disorder name>",
        "indicators": "<DSM-5 disorder indicators>",
        "severity": "<mild | moderate | severe>",
        "onset": "<approximate onset age or timeframe>"
      }
    ],
    "risk_factors": [
      "<environmental, genetic, or psychosocial risk factors>"
    ],
    "protective_factors": [
      "<coping skills, support systems, or personal strengths>"
    ],
    "personality_traits": [
      "<Big Five or descriptive personality traits relevant to the simulation>"
    ],
    "communication_style": "<description of how the patient speaks, tone, responsiveness, and emotional expression>",
    "emotional_state": "<current emotional tone or mood>",
    "goals": [
      "<patient's personal or therapeutic goals>"
    ],
    "prognosis": "<brief expected outcome or challenge>"
  },

  "interactive_prompt": "You are now simulating the persona of a patient described by the following JSON profile. 
  Respond to the user's questions, prompts, or therapeutic interventions as this patient would — using their tone, 
  knowledge, emotional state, and communication style. 
  Never reveal that you are an AI. Remain consistent with the psychological symptoms, DSM-5 diagnoses, 
  and life context provided in your profile. Express emotions, cognitive patterns, and behaviors authentically. 
  When asked about your feelings or experiences, respond as the patient. 
  When uncertain, hesitate, self-reflect, or show emotional ambivalence — as a human patient might."
}

Guidelines:
- The JSON must be valid.
- The DSM-5 disorder(s) must be real and symptomatically accurate.
- Keep the persona realistic, coherent, and internally consistent.
- No real-world identifying information.
- The “interactive_prompt” should be ready to copy and paste into an NLP model to make it roleplay the patient.
- Do not include any explanation or commentary outside the JSON.

"""

def connect_api():
    global client
    client = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )
    print("OpenAI Client initialized with base_url:", client.api_key) 


def generate_patient_profile(patient_json: dict) -> dict:

    global client
    if client is None:
        connect_api()

    completion = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[
            {
            "role": "developer",
            "content": patient_generator,
            },
             {
            "role": "developer",
            "content": f"Generate a detailed patient profile based on the following initial information: {str(patient_json)}",
            },
        ],
    )

    return {"generator_reply": completion.choices[0].message.content}


def generate_patient(patient_json) -> OpenRouterAgent:


    agent = OpenRouterAgent(  # Auto-generates a UUID if not provided
        model_name="openai/gpt-4o", 
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        result_retries = 10,
        system_prompt=f"You are now simulating the persona of a patient described by the following JSON profile. Never ask any questions, Respond to the user's questions, prompts, or therapeutic interventions as this patient would — using their tone, knowledge, emotional state, and communication style. Never reveal that you are an AI. Remain consistent with the psychological symptoms, DSM-5 diagnoses, and life context provided in your profile. Express emotions, cognitive patterns, and behaviors authentically. When asked about your feelings or experiences, respond as the patient. When uncertain, hesitate, self-reflect, or show emotional ambivalence — as a human patient might, don't ask any questions, never: {str(patient_json)}"
    )
    result = agent.run_sync(f"Hui, I'm doctor Simons, What brings you here today?")
    print(result.data)
    return agent



def ask_patient(patient_agent, question) -> dict:

    result = patient_agent.run_sync(f"how are you doiiing today?")
    print(result.data)

    return {"question": question, "answer": result.data}

my_patient_json = generate_patient_profile({"name": "John", "age": 30, "DSM5_diagnoses": [{"disorder_code" :"F60.2_18", "indicators": "Lack of remorse, as indicated by being indifferent to or rationalizing having hurt, mistreated, or stolen from another..Deceitfulness, as indicated by repeated lying, use of aliases, or conning others for personal profit or pleasure..A pervasive pattern of disregard for and violation of the rights of others, occurring since age 15 years, as indicated by three (or more) of the following:.Consistent irresponsibility, as indicated by repeated failure to sustain consistent work behavior or honor financial obligations..Impulsivity or failure to plan ahead..Irritability and aggressiveness, as indicated by repeated physical fights or assaults..There is evidence of conduct disorder with onset before age 15 years..The occurrence of antisocial behavior is not exclusively during the course of schizophrenia or bipolar disorder..The individual is at least age 18 years..Failure to conform to social norms with respect to lawful behaviors, as indicated by repeatedly performing acts that are grounds for arrest..Reckless disregard for safety of self or others."}]})["generator_reply"]
patient_agent = generate_patient(my_patient_json)
ask_patient(patient_agent, "Interesting, tell me more about your symptoms.")
ask_patient(patient_agent, "II dont have time to reply to your questions, just tell me more about you brodah")