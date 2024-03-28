# import sys, os
# sys.path.insert(
#     0, os.path.abspath("../")
# )  # Adds the parent directory to the system path
from fastapi import FastAPI, Request, status, HTTPException, Depends
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import uuid
import litellm
import json
import ast
import openai
from openai import AsyncOpenAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

litellm_router = litellm.Router(
    model_list=[
        {
            "model_name": "fake-openai-endpoint",  # model alias -> loadbalance between models with same `model_name`
            "litellm_params": {  # params for litellm completion/embedding call
                "model": "openai/anything",  # actual model name
                "api_key": "sk-1234",
                "api_base": "https://openai-endpoint.ishaanjaffer0324.workers.dev/",
            },
        },
        {
            "model_name": "gpt-3.5-turbo",
            "litellm_params": {'model': 'azure/chatgpt-v-2', 'api_base': 'https://openai-gpt-4-test-v-1.openai.azure.com/', 'api_version': '2023-05-15', 'api_key': 'gm'},
        },
        {
            "model_name": "gpt-3.5-turbo-large",
            "litellm_params":  {'model': 'gpt-3.5-turbo-1106', 'api_key': 'sk'},
        },
        {
            "model_name": "gpt-4",
            "litellm_params":  {'model': 'gpt-3.5-turbo-1106', 'api_key': 'sk'},

        },
        {
            "model_name": "sagemaker-completion-model",
            'litellm_params': {'model': 'sagemaker/berri-benchmarking-Llama-2-70b-chat-hf-4', 'input_cost_per_second': 0.00042}

        },
        {
            "model_name": "sagemaker-completion-model",
            'litellm_params': {'model': 'sagemaker/berri-benchmarking-Llama-2-70b-chat-hf-4', 'input_cost_per_second': 0.00042}

        },
        {
            "model_name": "sagemaker-completion-model",
            'litellm_params': {'model': 'sagemaker/berri-benchmarking-Llama-2-70b-chat-hf-4', 'input_cost_per_second': 0.00042}

        },
        {
            "model_name": "sagemaker-completion-model",
            'litellm_params': {'model': 'sagemaker/berri-benchmarking-Llama-2-70b-chat-hf-4', 'input_cost_per_second': 0.00042}

        },
        {
            "model_name": "sagemaker-completion-model",
            'litellm_params': {'model': 'sagemaker/berri-benchmarking-Llama-2-70b-chat-hf-4', 'input_cost_per_second': 0.00042}

        }

    ]
)

# for completion
@app.post("/chat/completions")
@app.post("/v1/chat/completions")
async def completion(request: Request):
    # this proxy uses the OpenAI SDK to call a fixed endpoint
    ### ROUTE THE REQUEST ###
    data = {}
    body = await request.body()
    body_str = body.decode()
    try:
        data = ast.literal_eval(body_str)
    except:
        data = json.loads(body_str)
    response = await litellm_router.acompletion(**data)
    return response


litellm_client = AsyncOpenAI(
    base_url="https://openai-endpoint.ishaanjaffer0324.workers.dev/",
    api_key="sk-1234",
)

# for completion
@app.post("/openai/chat/completions")
async def completion(request: Request):
    # this proxy uses the OpenAI SDK to call a fixed endpoint

    response = await litellm_client.chat.completions.create(
        model="anything",
        messages=[
            {
                "role": "user",
                "content": "hello who are you",
            }
        ],
    )

    return response


if __name__ == "__main__":
    import uvicorn

    # run this on 8090, 8091, 8092 and 8093
    uvicorn.run(app, host="0.0.0.0", port=8090)
