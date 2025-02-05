from __future__ import annotations
from livekit.agents import(
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm
    )


from livekit.agents.multimodal import MultimodalAgent
from livekit.plugins import google
from dotenv import load_dotenv
from api import AssistantFnc

from prompts import WELCOME_MESSAGE,INSTRUCTIONS,LOOKUP_CANDIDATE_MESSAGE


import certifi
import os
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
load_dotenv()


async def entrypoint(ctx : JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.SUBSCRIBE_ALL)
    await ctx.wait_for_participant()
    model = google.beta.realtime.RealtimeModel(
        voice="Puck",
        temperature=0.8,
        instructions=INSTRUCTIONS,    
        modalities=["AUDIO"]

    )
    
    assistant_fnc   = AssistantFnc()
    assistant = MultimodalAgent(model=model,fnc_ctx=assistant_fnc)
    
    assistant.start(ctx.room,)
    session = model.sessions[0]
    
    print(session)
    session.conversation.item.create(
        llm.ChatMessage(
            role="assistant",
            content=WELCOME_MESSAGE,   
        )
    )

    session.response.create()
    
if __name__ == "__main__" : 
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint,agent_name="Sarah"))
    