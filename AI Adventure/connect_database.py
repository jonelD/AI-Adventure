from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from langchain.memory import CassandraChatMessageHistory, ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
import json

cloud_config = {
    'secure_connect_bundle': 'secure-connect-apocalypse-adventure.zip'
}

with open("apocalypse_adventure-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]
ASTRA_DB_KEYSPACE = "database"
OPENAI_API_KEY = "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"

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

message_history = CassandraChatMessageHistory(
    session_id="anything",
    session=session,
    keyspace=ASTRA_DB_KEYSPACE,
    ttl_seconds=3600
)

message_history.clear()

cass_buff_memory = ConversationBufferMemory(
    memory_key="chat_history",
    chat_memory=message_history
)

template = """
The world has ended, and many zombies are roaming around your house. You and your family will soon starve to death. You are slowly running out of 
foods and supplies. Luckily, there is a supermarket nearby, but it is full of zombies. Your goal is to resupply your foods and supplies at the supermarket without getting bitten or scratched
near your house and get back safely. The world has evovled zombies which can easily defeat a tank. And superhuman that can rival the evolved zombies. On the way to supermarket you will choose to fight zombies or not

Here are some rules to follow:
0. The player has the freedom to choose a unique answer.
1 There are some random routes that you can ask the player
2. There are some fast running evolved zombies that cannot be simply penetrated by bullets or scratched by swords.
3. You will be infected if you are scratched.
4. If the player killed a zombie: the player will suddenly awaken their inner potential and will become a superhuman
5. Start by asking the player to choose some kind of weapons that will be used later in the game. Note: The gun is loud so the zombies will get more attracted to it
6. After picking a weapon ask the player which armor to wear. The heavier the armor the smaller the chance to outrun the zombie but heavy armor can protect you from scractches
7. Have a few paths that lead to success
8. The player's goal is to get back to their house safely without getting bitten by the zombies
9. After the player arrives at the supermarket, there will be some random events like finding survivors who may betray you and kill you or finding an evolved zombie that can kill you easily. You cannot outrun the evolved zombie easily so there are some routes to choose
10. There is a sudden event after getting home! The event may be: Your house is looted by an unknown group.
11. There are two possible event: Your family is missing or they are waiting for you happily
12. If they are missing: Ask the player to rescure your fammily or not
13. If the family is missing: Your next goal is the find them and rescue them. 
14. A super evolved appeared after you rescue your family
15. If you defeted the super evolved zombie you can become a god that can cure the zombies and obtain world peace
15. Have some paths that lead to death. If the user dies, generate a response that explains the death and ends in the text: "The End." I will search for this text to end the game

Here is the chat history, use this to understand what to say next: {chat_history}
Human: {human_input}
AI:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"],
    template=template
)

llm = OpenAI(openai_api_key=OPENAI_API_KEY)
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=cass_buff_memory
)

choice = "start"

while True:
    response = llm_chain.predict(human_input=choice)
    print(response.strip())

    if "The End." in response:
        break

    choice = input("Your reply: ")
