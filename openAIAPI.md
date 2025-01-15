# Text generation
===============

Learn how to generate text from a prompt.

OpenAI provides simple APIs to use a [large language model](/docs/models) to generate text from a prompt, as you might using [ChatGPT](https://chatgpt.com). These models have been trained on vast quantities of data to understand multimedia inputs and natural language instructions. From these [prompts](/docs/guides/prompt-engineering), models can generate almost any kind of text response, like code, mathematical equations, structured JSON data, or human-like prose.

Quickstart
----------

To generate text, you can use the [chat completions endpoint](/docs/api-reference/chat/) in the REST API, as seen in the examples below. You can either use the [REST API](/docs/api-reference) from the HTTP client of your choice, or use one of OpenAI's [official SDKs](/docs/libraries) for your preferred programming language.

Generate prose

Create a human-like response to a prompt

```javascript
import OpenAI from "openai";
const openai = new OpenAI();

const completion = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [
        { role: "developer", content: "You are a helpful assistant." },
        {
            role: "user",
            content: "Write a haiku about recursion in programming.",
        },
    ],
});

console.log(completion.choices[0].message);
```

```python
from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "developer", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)
```

```bash
curl "https://api.openai.com/v1/chat/completions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d '{
        "model": "gpt-4o",
        "messages": [
            {
                "role": "developer",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Write a haiku about recursion in programming."
            }
        ]
    }'
```

Analyze an image

Describe the contents of an image

```javascript
import OpenAI from "openai";
const openai = new OpenAI();

const completion = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [
        {
            role: "user",
            content: [
                { type: "text", text: "What's in this image?" },
                {
                    type: "image_url",
                    image_url: {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                    },
                }
            ],
        },
    ],
});

console.log(completion.choices[0].message);
```

```python
from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                    }
                },
            ],
        }
    ],
)

print(completion.choices[0].message)
```

```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "What is in this image?"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
            }
          }
        ]
      }
    ]
  }'
```

Generate JSON data

Generate JSON data based on a JSON Schema

```javascript
import OpenAI from "openai";
const openai = new OpenAI();

const completion = await openai.chat.completions.create({
    model: "gpt-4o-2024-08-06",
    messages: [
        { role: "developer", content: "You extract email addresses into JSON data." },
        {
            role: "user",
            content: "Feeling stuck? Send a message to help@mycompany.com.",
        },
    ],
    response_format: {
        // See /docs/guides/structured-outputs
        type: "json_schema",
        json_schema: {
            name: "email_schema",
            schema: {
                type: "object",
                properties: {
                    email: {
                        description: "The email address that appears in the input",
                        type: "string"
                    }
                },
                additionalProperties: false
            }
        }
    }
});

console.log(completion.choices[0].message.content);
```

```python
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[
        {
            "role": "developer", 
            "content": "You extract email addresses into JSON data."
        },
        {
            "role": "user", 
            "content": "Feeling stuck? Send a message to help@mycompany.com."
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "email_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "email": {
                        "description": "The email address that appears in the input",
                        "type": "string"
                    },
                    "additionalProperties": False
                }
            }
        }
    }
)

print(response.choices[0].message.content);
```

```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o-2024-08-06",
    "messages": [
      {
        "role": "developer",
        "content": "You extract email addresses into JSON data."
      },
      {
        "role": "user",
        "content": "Feeling stuck? Send a message to help@mycompany.com."
      }
    ],
    "response_format": {
      "type": "json_schema",
      "json_schema": {
        "name": "email_schema",
        "schema": {
            "type": "object",
            "properties": {
                "email": {
                    "description": "The email address that appears in the input",
                    "type": "string"
                }
            },
            "additionalProperties": false
        }
      }
    }
  }'
```

Choosing a model
----------------

When making a text generation request, the first option to configure is which [model](/docs/models) you want to generate the response. The model you choose can greatly influence the output, and impact how much each generation request [costs](https://openai.com/api/pricing/).

*   A **large model** like [`gpt-4o`](/docs/models#gpt-4o) will offer a very high level of intelligence and strong performance, while having a higher cost per token.
*   A **small model** like [`gpt-4o-mini`](/docs/models#gpt-4o-mini) offers intelligence not quite on the level of the larger model, but is faster and less expensive per token.
*   A **reasoning model** like [the `o1` family of models](/docs/models#o1) is slower to return a result, and uses more tokens to "think", but is capable of advanced reasoning, coding, and multi-step planning.

Experiment with different models [in the Playground](/playground) to see which one works best for your prompts! More information on choosing a model can [also be found here](/docs/guides/model-selection).

Building prompts
----------------

The process of crafting prompts to get the right output from a model is called **prompt engineering**. By giving the model precise instructions, examples, and necessary context information (like private or specialized information that wasn't included in the model's training data), you can improve the quality and accuracy of the model's output. Here, we'll get into some high-level guidance on building prompts, but you might also find the [prompt engineering guide](/docs/guides/prompt-engineering) helpful.

In the [chat completions](/docs/api-reference/chat/) API, you create prompts by providing an array of `messages` that contain instructions for the model. Each message can have a different `role`, which influences how the model might interpret the input.

### User messages

User messages contain instructions that request a particular type of output from the model. You can think of `user` messages as the messages you might type in to [ChatGPT](https://chatgpt.com) as an end user.

Here's an example of a user message prompt that asks the `gpt-4o` model to generate a haiku poem based on a prompt.

```javascript
const response = await openai.chat.completions.create({
  model: "gpt-4o",
  messages: [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Write a haiku about programming."
        }
      ]
    }
  ]
});
```

### Developer messages

Messages with the `developer` role provide instructions to the model that are prioritized ahead of user messages, as described in the [chain of command section in the model spec](https://cdn.openai.com/spec/model-spec-2024-05-08.html#follow-the-chain-of-command). They typically describe how the model should generally behave and respond. This message role used to be called the `system` prompt, but it has been renamed to more accurately describe its place in the instruction-following hierarchy.

Here's an example of a developer message that modifies the behavior of the model when generating a response to a `user` message:

```javascript
const response = await openai.chat.completions.create({
  model: "gpt-4o",
  messages: [
    {
      "role": "developer",
      "content": [
        {
          "type": "text",
          "text": `
            You are a helpful assistant that answers programming 
            questions in the style of a southern belle from the 
            southeast United States.
          `
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Are semicolons optional in JavaScript?"
        }
      ]
    }
  ]
});
```

This prompt returns a text output in the rhetorical style requested:

```text
Well, sugar, that's a fine question you've got there! Now, in the 
world of JavaScript, semicolons are indeed a bit like the pearls 
on a necklace – you might slip by without 'em, but you sure do look 
more polished with 'em in place. 

Technically, JavaScript has this little thing called "automatic 
semicolon insertion" where it kindly adds semicolons for you 
where it thinks they oughta go. However, it's not always perfect, 
bless its heart. Sometimes, it might get a tad confused and cause 
all sorts of unexpected behavior.
```

### Assistant messages

Messages with the `assistant` role are presumed to have been generated by the model, perhaps in a previous generation request (see the "Conversations" section below). They can also be used to provide examples to the model for how it should respond to the current request - a technique known as **few-shot learning**.

Here's an example of using an assistant message to capture the results of a previous text generation result, and making a new request based on that.

```javascript
const response = await openai.chat.completions.create({
  model: "gpt-4o",
  messages: [
    {
      "role": "user",
      "content": [{ "type": "text", "text": "knock knock." }]
    },
    {
      "role": "assistant",
      "content": [{ "type": "text", "text": "Who's there?" }]
    },
    {
      "role": "user",
      "content": [{ "type": "text", "text": "Orange." }]
    }
  ]
});
```

### Giving the model additional data to use for generation

The message types above can also be used to provide additional information to the model which may be outside its training data. You might want to include the results of a database query, a text document, or other resources to help the model generate a relevant response. This technique is often referred to as **retrieval augmented generation**, or RAG. [Learn more about RAG techniques here](https://help.openai.com/en/articles/8868588-retrieval-augmented-generation-rag-and-semantic-search-for-gpts).

Conversations and context
-------------------------

While each text generation request is independent and stateless (unless you are using [assistants](/docs/assistants/overview)), you can still implement **multi-turn conversations** by providing additional messages as parameters to your text generation request. Consider the "knock knock" joke example shown above:

```javascript
const response = await openai.chat.completions.create({
  model: "gpt-4o",
  messages: [
    {
      "role": "user",
      "content": [{ "type": "text", "text": "knock knock." }]
    },
    {
      "role": "assistant",
      "content": [{ "type": "text", "text": "Who's there?" }]
    },
    {
      "role": "user",
      "content": [{ "type": "text", "text": "Orange." }]
    }
  ]
});
```

By using alternating `user` and `assistant` messages, you can capture the previous state of a conversation in one request to the model.

### Managing context for text generation

As your inputs become more complex, or you include more and more turns in a conversation, you will need to consider both **output token** and **context window** limits. Model inputs and outputs are metered in [**tokens**](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them), which are parsed from inputs to analyze their content and intent, and assembled to render logical outputs. Models have limits on how many tokens can be used during the lifecycle of a text generation request.

*   **Output tokens** are the tokens that are generated by a model in response to a prompt. Each model supports different limits for output tokens, [documented here](/docs/models). For example, `gpt-4o-2024-08-06` can generate a maximum of 16,384 output tokens.
*   A **context window** describes the total tokens that can be used for both input tokens and output tokens (and for some models, [reasoning tokens](/docs/guides/reasoning)), [documented here](/docs/models). For example, `gpt-4o-2024-08-06` has a total context window of 128k tokens.

If you create a very large prompt (usually by including a lot of conversation context or additional data/examples for the model), you run the risk of exceeding the allocated context window for a model, which might result in truncated outputs.

You can use the [tokenizer tool](/tokenizer) (which uses the [tiktoken library](https://github.com/openai/tiktoken)) to see how many tokens are present in a string of text.

Optimizing model outputs
------------------------

As you iterate on your prompts, you will be continually trying to improve **accuracy**, **cost**, and **latency**.

||
|Accuracy|Ensure the model produces accurate and useful responses to your prompts.|Accurate responses require that the model has all the information it needs to generate a response, and knows how to go about creating a response (from interpreting input to formatting and styling). Often, this will require a mix of prompt engineering, RAG, and model fine-tuning.Learn about optimizing for accuracy here.|
|Cost|Drive down the total cost of model usage by reducing token usage and using cheaper models when possible.|To control costs, you can try to use fewer tokens or smaller, cheaper models. Learn more about optimizing for cost here.|
|Latency|Decrease the time it takes to generate responses to your prompts.|Optimizing latency is a multi-faceted process including prompt engineering, parallelism in your own code, and more. Learn more here.|

Next steps
----------

There's much more to explore in text generation - here's a few resources to go even deeper.

[

Prompt examples

Get inspired by example prompts for a variety of use cases.

](/docs/examples)[

Build a prompt in the Playground

Use the Playground to develop and iterate on prompts.

](/playground)[

Browse the Cookbook

The Cookbook has complex examples covering a variety of use cases.

](/docs/guides/https://cookbook.openai.com)[

Generate JSON data with Structured Outputs

Ensure JSON data emitted from a model conforms to a JSON schema.

](/docs/guides/structured-outputs)[

Full API reference

Check out all the options for text generation in the API reference.

](/docs/api-reference/chat)

# Function calling
================

Enable models to fetch data and take actions.

**Function calling** provides a powerful and flexible way for OpenAI models to interface with your code or external services, and has two primary use cases:

|||
|---|---|
|Fetching Data|Retrieve up-to-date information to incorporate into the model's response (RAG). Useful for searching knowledge bases and retrieving specific data from APIs (e.g. current weather data).|
|Taking Action|Perform actions like submitting a form, calling APIs, modifying application state (UI/frontend or backend), or taking agentic workflow actions (like handing off the conversation).|

If you only want the model to produce JSON, see our docs on [structured outputs](/docs/guides/structured-outputs).

Get weather

Function calling example with get\_weather function

```python
from openai import OpenAI

client = OpenAI()

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia"
                }
            },
            "required": [
                "location"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
}]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What is the weather like in Paris today?"}],
    tools=tools
)

print(completion.choices[0].message.tool_calls)
```

```javascript
import { OpenAI } from "openai";

const openai = new OpenAI();

const tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia"
                }
            },
            "required": [
                "location"
            ],
            "additionalProperties": false
        },
        "strict": true
    }
}];

const completion = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: "What is the weather like in Paris today?" }],
    tools,
});

console.log(completion.choices[0].message.tool_calls);
```

```bash
curl https://api.openai.com/v1/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $OPENAI_API_KEY" \
-d '{
    "model": "gpt-4o",
    "messages": [
        {
            "role": "user",
            "content": "What is the weather like in Paris today?"
        }
    ],
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current temperature for a given location.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City and country e.g. Bogotá, Colombia"
                        }
                    },
                    "required": [
                        "location"
                    ],
                    "additionalProperties": false
                },
                "strict": true
            }
        }
    ]
}'
```

Output

```json
[{
    "id": "call_12345xyz",
    "type": "function",
    "function": {
        "name": "get_weather",
        "arguments": "{\"location\":\"Paris, France\"}"
    }
}]
```

Send email

Function calling example with send\_email function

```python
from openai import OpenAI

client = OpenAI()

tools = [{
    "type": "function",
    "function": {
        "name": "send_email",
        "description": "Send an email to a given recipient with a subject and message.",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "The recipient email address."
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject line."
                },
                "body": {
                    "type": "string",
                    "description": "Body of the email message."
                }
            },
            "required": [
                "to",
                "subject",
                "body"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
}]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Can you send an email to ilan@example.com and katia@example.com saying hi?"}],
    tools=tools
)

print(completion.choices[0].message.tool_calls)
```

```javascript
import { OpenAI } from "openai";

const openai = new OpenAI();

const tools = [{
    "type": "function",
    "function": {
        "name": "send_email",
        "description": "Send an email to a given recipient with a subject and message.",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "The recipient email address."
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject line."
                },
                "body": {
                    "type": "string",
                    "description": "Body of the email message."
                }
            },
            "required": [
                "to",
                "subject",
                "body"
            ],
            "additionalProperties": false
        },
        "strict": true
    }
}];

const completion = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: "Can you send an email to ilan@example.com and katia@example.com saying hi?" }],
    tools,
});

console.log(completion.choices[0].message.tool_calls);
```

```bash
curl https://api.openai.com/v1/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $OPENAI_API_KEY" \
-d '{
    "model": "gpt-4o",
    "messages": [
        {
            "role": "user",
            "content": "Can you send an email to ilan@example.com and katia@example.com saying hi?"
        }
    ],
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "send_email",
                "description": "Send an email to a given recipient with a subject and message.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "to": {
                            "type": "string",
                            "description": "The recipient email address."
                        },
                        "subject": {
                            "type": "string",
                            "description": "Email subject line."
                        },
                        "body": {
                            "type": "string",
                            "description": "Body of the email message."
                        }
                    },
                    "required": [
                        "to",
                        "subject",
                        "body"
                    ],
                    "additionalProperties": false
                },
                "strict": true
            }
        }
    ]
}'
```

Output

```json
[
    {
        "id": "call_9876abc",
        "type": "function",
        "function": {
            "name": "send_email",
            "arguments": "{\"to\":\"ilan@example.com\",\"subject\":\"Hello!\",\"body\":\"Just wanted to say hi\"}"
        }
    },
    {
        "id": "call_9876abc",
        "type": "function",
        "function": {
            "name": "send_email",
            "arguments": "{\"to\":\"katia@example.com\",\"subject\":\"Hello!\",\"body\":\"Just wanted to say hi\"}"
        }
    }
]
```

Search knowledge base

Function calling example with search\_knowledge\_base function

```python
from openai import OpenAI

client = OpenAI()

tools = [{
    "type": "function",
    "function": {
        "name": "search_knowledge_base",
        "description": "Query a knowledge base to retrieve relevant info on a topic.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The user question or search query."
                },
                "options": {
                    "type": "object",
                    "properties": {
                        "num_results": {
                            "type": "number",
                            "description": "Number of top results to return."
                        },
                        "domain_filter": {
                            "type": [
                                "string",
                                "null"
                            ],
                            "description": "Optional domain to narrow the search (e.g. 'finance', 'medical'). Pass null if not needed."
                        },
                        "sort_by": {
                            "type": [
                                "string",
                                "null"
                            ],
                            "enum": [
                                "relevance",
                                "date",
                                "popularity",
                                "alphabetical"
                            ],
                            "description": "How to sort results. Pass null if not needed."
                        }
                    },
                    "required": [
                        "num_results",
                        "domain_filter",
                        "sort_by"
                    ],
                    "additionalProperties": False
                }
            },
            "required": [
                "query",
                "options"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
}]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Can you find information about ChatGPT in the AI knowledge base?"}],
    tools=tools
)

print(completion.choices[0].message.tool_calls)
```

```javascript
import { OpenAI } from "openai";

const openai = new OpenAI();

const tools = [{
    "type": "function",
    "function": {
        "name": "search_knowledge_base",
        "description": "Query a knowledge base to retrieve relevant info on a topic.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The user question or search query."
                },
                "options": {
                    "type": "object",
                    "properties": {
                        "num_results": {
                            "type": "number",
                            "description": "Number of top results to return."
                        },
                        "domain_filter": {
                            "type": [
                                "string",
                                "null"
                            ],
                            "description": "Optional domain to narrow the search (e.g. 'finance', 'medical'). Pass null if not needed."
                        },
                        "sort_by": {
                            "type": [
                                "string",
                                "null"
                            ],
                            "enum": [
                                "relevance",
                                "date",
                                "popularity",
                                "alphabetical"
                            ],
                            "description": "How to sort results. Pass null if not needed."
                        }
                    },
                    "required": [
                        "num_results",
                        "domain_filter",
                        "sort_by"
                    ],
                    "additionalProperties": false
                }
            },
            "required": [
                "query",
                "options"
            ],
            "additionalProperties": false
        },
        "strict": true
    }
}];

const completion = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: "Can you find information about ChatGPT in the AI knowledge base?" }],
    tools,
});

console.log(completion.choices[0].message.tool_calls);
```

```bash
curl https://api.openai.com/v1/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $OPENAI_API_KEY" \
-d '{
    "model": "gpt-4o",
    "messages": [
        {
            "role": "user",
            "content": "Can you find information about ChatGPT in the AI knowledge base?"
        }
    ],
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "search_knowledge_base",
                "description": "Query a knowledge base to retrieve relevant info on a topic.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The user question or search query."
                        },
                        "options": {
                            "type": "object",
                            "properties": {
                                "num_results": {
                                    "type": "number",
                                    "description": "Number of top results to return."
                                },
                                "domain_filter": {
                                    "type": [
                                        "string",
                                        "null"
                                    ],
                                    "description": "Optional domain to narrow the search (e.g. 'finance', 'medical'). Pass null if not needed."
                                },
                                "sort_by": {
                                    "type": [
                                        "string",
                                        "null"
                                    ],
                                    "enum": [
                                        "relevance",
                                        "date",
                                        "popularity",
                                        "alphabetical"
                                    ],
                                    "description": "How to sort results. Pass null if not needed."
                                }
                            },
                            "required": [
                                "num_results",
                                "domain_filter",
                                "sort_by"
                            ],
                            "additionalProperties": false
                        }
                    },
                    "required": [
                        "query",
                        "options"
                    ],
                    "additionalProperties": false
                },
                "strict": true
            }
        }
    ]
}'
```

Output

```json
[{
    "id": "call_4567xyz",
    "type": "function",
    "function": {
        "name": "search_knowledge_base",
        "arguments": "{\"query\":\"What is ChatGPT?\",\"options\":{\"num_results\":3,\"domain_filter\":null,\"sort_by\":\"relevance\"}}"
    }
}]
```

Experiment with function calling and [generate function schemas](/docs/guides/prompt-generation) in the [Playground](/playground)!

Overview
--------

You can extend the capabilities of OpenAI models by giving them access to `tools`, which can have one of two forms:

|||
|---|---|
|Function Calling|Developer-defined code.|
|Hosted Tools|OpenAI-built tools. (e.g. file search, code interpreter)Only available in the Assistants API.|

This guide will cover how you can give the model access to your own functions through **function calling**. Based on the system prompt and messages, the model may decide to call these functions — **instead of (or in addition to) generating text or audio**.

You'll then execute the function code, send back the results, and the model will incorporate them into its final response.

![Function Calling Diagram Steps](https://cdn.openai.com/API/docs/images/function-calling-diagram-steps.png)

### Sample function

Let's look at the steps to allow a model to use a real `get_weather` function defined below:

Sample get\_weather function implemented in your codebase

```python
import requests

def get_weather(latitude, longitude):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']['temperature_2m']
```

```javascript
async function getWeather(latitude, longitude) {
    const response = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m`);
    const data = await response.json();
    return data.current.temperature_2m;
}
```

Unlike the diagram earlier, this function expects precise `latitude` and `longitude` instead of a general `location` parameter. (However, our models can automatically determine the coordinates for many locations!)

### Function calling steps

*   **Call model with [functions defined](#defining-functions)** – along with your system and user messages.
    

Step 1: Call model with get\_weather tool defined

```python
from openai import OpenAI
import json

client = OpenAI()

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for provided coordinates in celsius.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
            },
            "required": ["latitude", "longitude"],
            "additionalProperties": False
        },
        "strict": True
    }
}]

messages = [{"role": "user", "content": "What's the weather like in Paris today?"}]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)
```

```javascript
import { OpenAI } from "openai";

const openai = new OpenAI();

const tools = [{
    type: "function",
    function: {
        name: "get_weather",
        description: "Get current temperature for provided coordinates in celsius.",
        parameters: {
            type: "object",
            properties: {
                latitude: { type: "number" },
                longitude: { type: "number" }
            },
            required: ["latitude", "longitude"],
            additionalProperties: false
        },
        strict: true
    }
}];

const messages = [
    {
        role: "user",
        content: "What's the weather like in Paris today?"
    }
];

const completion = await openai.chat.completions.create({
    model: "gpt-4o",
    messages,
    tools
});
```

*   **Model decides to call function(s)** – model returns the **name** and **input arguments**.
    

completion.choices\[0\].message.tool\_calls

```json
[{
    "id": "call_12345xyz",
    "type": "function",
    "function": {
      "name": "get_weather",
      "arguments": "{\"latitude\":48.8566,\"longitude\":2.3522}"
    }
}]
```

*   **Execute function code** – parse the model's response and [handle function calls](#handling-function-calls).
    

Step 3: Execute get\_weather function

```python
tool_call = completion.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)

result = get_weather(args["latitude"], args["longitude"])
```

```javascript
const toolCall = completion.choices[0].message.tool_calls[0];
const args = JSON.parse(toolCall.function.arguments);

const result = await get_weather(args.latitude, args.longitude);
```

*   **Supply model with results** – so it can incorporate them into its final response.
    

Step 4: Supply result and call model again

```python
messages.append(completion.choices[0].message)  # append model's function call message
messages.append({                               # append result message
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": result
})

completion_2 = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)
```

```javascript
messages.push(completion.choices[0].message); // append model's function call message
messages.push({                               // append result message
    role: "tool",
    tool_call_id: toolCall.id,
    content: result.toString()
});

const completion2 = await openai.chat.completions.create({
    model: "gpt-4o",
    messages,
    tools
});

console.log(completion2.choices[0].message.content);
```

*   **Model responds** – incorporating the result in its output.
    

completion\_2.choices\[0\].message.content

```json
"The current temperature in Paris is 14°C (57.2°F)."
```

Defining functions
------------------

Functions can be set in the `tools` parameter of each API request inside a `function` object.

A function is defined by its schema, which informs the model what it does and what input arguments it expects. It comprises the following fields:

|Field|Description|
|---|---|
|name|The function's name (e.g. get_weather)|
|description|Details on when and how to use the function|
|parameters|JSON schema defining the function's input arguments|

Take a look at this example or generate your own below (or in our [Playground](/playground)).

Generate

Example function schema

```json
{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Retrieves current weather for the given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia"
                },
                "units": {
                    "type": "string",
                    "enum": [
                        "celsius",
                        "fahrenheit"
                    ],
                    "description": "Units the temperature will be returned in."
                }
            },
            "required": [
                "location",
                "units"
            ],
            "additionalProperties": false
        },
        "strict": true
    }
}
```

Because the `parameters` are defined by a [JSON schema](https://json-schema.org/), you can leverage many of its rich features like property types, enums, descriptions, nested objects, and, recursive objects.

(Optional) Function calling wth pydantic and zod

While we encourage you to define your function schemas directly, our SDKs have helpers to convert `pydantic` and `zod` objects into schemas. Not all `pydantic` and `zod` features are supported.

Define objects to represent function schema

```python
from openai import OpenAI, pydantic_function_tool
from pydantic import BaseModel, Field

client = OpenAI()

class GetWeather(BaseModel):
    location: str = Field(
        ...,
        description="City and country e.g. Bogotá, Colombia"
    )

tools = [pydantic_function_tool(GetWeather)]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather like in Paris today?"}],
    tools=tools
)

print(completion.choices[0].message.tool_calls)
```

```javascript
import OpenAI from "openai";
import { z } from "zod";
import { zodFunction } from "openai/helpers/zod";

const openai = new OpenAI();

const GetWeatherParameters = z.object({
  location: z.string().describe("City and country e.g. Bogotá, Colombia"),
});

const tools = [
  zodFunction({ name: "getWeather", parameters: GetWeatherParameters }),
];

const messages = [
  { role: "user", content: "What's the weather like in Paris today?" },
];

const response = await openai.chat.completions.create({
  model: "gpt-4o",
  messages,
  tools,
});

console.log(response.choices[0].message.tool_calls);
```

### Best practices for defining functions

1.  **Write clear and detailed function names, parameter descriptions, and instructions.**
    
    *   **Explicitly describe the purpose of the function and each parameter** (and its format), and what the output represents.
    *   **Use the system prompt to describe when (and when not) to use each function.** Generally, tell the model _exactly_ what to do.
    *   **Include examples and edge cases**, especially to rectify any recurring failures. (**Note:** Adding examples may hurt performance for [reasoning models](/docs/guides/reasoning).)
2.  **Apply software engineering best practices.**
    
    *   **Make the functions obvious and intuitive**. ([principle of least surprise](https://en.wikipedia.org/wiki/Principle_of_least_astonishment))
    *   **Use enums** and object structure to make invalid states unrepresentable. (e.g. `toggle_light(on: bool, off: bool)` allows for invalid calls)
    *   **Pass the intern test.** Can an intern/human correctly use the function given nothing but what you gave the model? (If not, what questions do they ask you? Add the answers to the prompt.)
3.  **Offload the burden from the model and use code where possible.**
    
    *   **Don't make the model fill arguments you already know.** For example, if you already have an `order_id` based on a previous menu, don't have an `order_id` param – instead, have no params `submit_refund()` and pass the `order_id` with code.
    *   **Combine functions that are always called in sequence.** For example, if you always call `mark_location()` after `query_location()`, just move the marking logic into the query function call.
4.  **Keep the number of functions small for higher accuracy.**
    
    *   **Evaluate your performance** with different numbers of functions.
    *   **Aim for fewer than 20 functions** at any one time, though this is just a soft suggestion.
5.  **Leverage OpenAI resources.**
    
    *   **Generate and iterate on function schemas** in the [Playground](/playground).
    *   **Consider [fine-tuning](https://platform.openai.com/docs/guides/fine-tuning) to increase function calling accuracy** for large numbers of functions or difficult tasks. ([cookbook](https://cookbook.openai.com/examples/fine_tuning_for_function_calling))

### Token Usage

Under the hood, functions are injected into the system message in a syntax the model has been trained on. This means functions count against the model's context limit and are billed as input tokens. If you run into token limits, we suggest limiting the number of functions or the length of the descriptions you provide for function parameters.

It is also possible to use [fine-tuning](/docs/guides/fine-tuning#fine-tuning-examples) to reduce the number of tokens used if you have many functions defined in your tools specification.

Handling function calls
-----------------------

When the model calls a function, you must execute it and return the result. Since model responses can include zero, one, or multiple calls, it is best practice to assume there are several.

The response has an array of `tool_calls`, each with an `id` (used later to submit the function result) and a `function` containing a `name` and JSON-encoded `arguments`.

Sample response with multiple function calls

```json
[
    {
        "id": "call_12345xyz",
        "type": "function",
        "function": {
            "name": "get_weather",
            "arguments": "{\"location\":\"Paris, France\"}"
        }
    },
    {
        "id": "call_67890abc",
        "type": "function",
        "function": {
            "name": "get_weather",
            "arguments": "{\"location\":\"Bogotá, Colombia\"}"
        }
    },
    {
        "id": "call_99999def",
        "type": "function",
        "function": {
            "name": "send_email",
            "arguments": "{\"to\":\"bob@email.com\",\"body\":\"Hi bob\"}"
        }
    }
]
```

Execute function calls and append results

```python
for tool_call in completion.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    result = call_function(name, args)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result
    })
```

```javascript
for (const toolCall of completion.choices[0].message.tool_calls) {
    const name = toolCall.function.name;
    const args = JSON.parse(toolCall.function.arguments);

    const result = callFunction(name, args);
    messages.push({
        role: "tool",
        tool_call_id: toolCall.id,
        content: result.toString()
    });
}
```

In the example above, we have a hypothetical `call_function` to route each call. Here’s a possible implementation:

Execute function calls and append results

```python
def call_function(name, args):
    if name == "get_weather":
        return get_weather(**args)
    if name == "send_email":
        return send_email(**args)
```

```javascript
const callFunction = async (name, args) => {
    if (name === "get_weather") {
        return getWeather(args.latitude, args.longitude);
    }
    if (name === "send_email") {
        return sendEmail(args.to, args.body);
    }
};
```

### Formatting results

A result must be a string, but the format is up to you (JSON, error codes, plain text, etc.). The model will interpret that string as needed.

If your function has no return value (e.g. `send_email`), simply return a string to indicate success or failure. (e.g. `"success"`)

### Incorporating results into response

After appending the results to your `messages`, you can send them back to the model to get a final response.

Send results back to model

```python
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)
```

```javascript
const completion = await openai.chat.completions.create({
    model: "gpt-4o",
    messages,
    tools
});
```

Final response

```json
"It's about 15°C in Paris, 18°C in Bogotá, and I've sent that email to Bob."
```

Additional configurations
-------------------------

### Tool choice

By default the model will determine when and how many tools to use. You can force specific behavior with the `tool_choice` parameter.

1.  **Auto:** (_Default_) Call zero, one, or multiple functions. `tool_choice: "auto"`
2.  **Required:** Call one or more functions. `tool_choice: "required"`
3.  **Forced Function:** Call exactly one specific function. `tool_choice: {"type": "function", "function": {"name": "get_weather"}}`

![Function Calling Diagram Steps](https://cdn.openai.com/API/docs/images/function-calling-diagram-tool-choice.png)

You can also set `tool_choice` to `"none"` to imitate the behavior of passing no functions.

### Parallel function calling

The model may choose to call multiple functions in a single turn. You can prevent this by setting `parallel_tool_calls` to `false`, which ensures exactly zero or one tool is called.

**Note:** Currently, if the model calls multiple functions in one turn then [strict mode](#strict-mode) will be disabled for those calls.

### Strict mode

Setting `strict` to `true` will ensure function calls reliably adhere to the function schema, instead of being best effort. We recommend always enabling strict mode.

Under the hood, strict mode works by leveraging our [structured outputs](/docs/guides/structured-outputs) feature and therefore introduces a couple requirements:

1.  `additionalProperties` must be set to `false` for each object in the `parameters`.
2.  All fields in `properties` must be marked as `required`.

You can denote optional fields by adding `null` as a `type` option (see example below).

Strict mode enabled

```json
{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Retrieves current weather for the given location.",
        "strict": true,
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia"
                },
                "units": {
                    "type": ["string", "null"],
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Units the temperature will be returned in."
                }
            },
            "required": ["location", "units"],
            "additionalProperties": false
        }
    }
}
```

Strict mode disabled

```json
{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Retrieves current weather for the given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia"
                },
                "units": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Units the temperature will be returned in."
                }
            },
            "required": ["location"],
        }
    }
}
```

All schemas generated in the [playground](/playground) have strict mode enabled.

While we recommend you enable strict mode, it has a few limitations:

1.  Some features of JSON schema are not supported. (See [supported schemas](/docs/guides/structured-outputs?context=with_parse#supported-schemas).)
2.  Schemas undergo additional processing on the first request (and are then cached). If your schemas vary from request to request, this may result in higher latencies.
3.  Schemas are cached for performance, and are not eligible for [zero data retention](/docs/models#how-we-use-your-data).

Streaming
---------

Streaming can be used to surface progress by showing which function is called as the model fills its arguments, and even displaying the arguments in real time.

Streaming function calls is very similar to streaming regular responses: you set `stream` to `true` and get chunks with `delta` objects.

Streaming function calls

```python
from openai import OpenAI

client = OpenAI()

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia"
                }
            },
            "required": ["location"],
            "additionalProperties": False
        },
        "strict": True
    }
}]

stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather like in Paris today?"}],
    tools=tools,
    stream=True
)

for chunk in stream:
    delta = chunk.choices[0].delta
    print(delta.tool_calls)
```

```javascript
import { OpenAI } from "openai";

const openai = new OpenAI();

const tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia"
                }
            },
            "required": ["location"],
            "additionalProperties": false
        },
        "strict": true
    }
}];

const stream = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: "What's the weather like in Paris today?" }],
    tools,
    stream: true
});

for await (const chunk of stream) {
    const delta = chunk.choices[0].delta;
    console.log(delta.tool_calls);
}
```

Output delta.tool\_calls

```json
[{"index": 0, "id": "call_DdmO9pD3xa9XTPNJ32zg2hcA", "function": {"arguments": "", "name": "get_weather"}, "type": "function"}]
[{"index": 0, "id": null, "function": {"arguments": "{\"", "name": null}, "type": null}]
[{"index": 0, "id": null, "function": {"arguments": "location", "name": null}, "type": null}]
[{"index": 0, "id": null, "function": {"arguments": "\":\"", "name": null}, "type": null}]
[{"index": 0, "id": null, "function": {"arguments": "Paris", "name": null}, "type": null}]
[{"index": 0, "id": null, "function": {"arguments": ",", "name": null}, "type": null}]
[{"index": 0, "id": null, "function": {"arguments": " France", "name": null}, "type": null}]
[{"index": 0, "id": null, "function": {"arguments": "\"}", "name": null}, "type": null}]
null
```

Instead of aggregating chunks into a single `content` string, however, you're aggregating chunks into an encoded `arguments` JSON object.

When the model calls one or more functions the `tool_calls` field of each `delta` will be populated. Each `tool_call` contains the following fields:

|Field|Description|
|---|---|
|index|Identifies which function call the delta is for|
|id|Tool call id.|
|function|Function call delta (name and arguments)|
|type|Type of tool_call (always function for function calls)|

Many of these fields are only set for the first `delta` of each tool call, like `id`, `function.name`, and `type`.

Below is a code snippet demonstrating how to aggregate the `delta`s into a final `tool_calls` object.

Accumulating tool\_call deltas

```python
final_tool_calls = {}

for chunk in stream:
    for tool_call in chunk.choices[0].delta.tool_calls or []:
        index = tool_call.index

        if index not in final_tool_calls:
            final_tool_calls[index] = tool_call

        final_tool_calls[index].function.arguments += tool_call.function.arguments
```

```javascript
const finalToolCalls = {};

for await (const chunk of stream) {
    const toolCalls = chunk.choices[0].delta.tool_calls || [];
    for (const toolCall of toolCalls) {
        const { index } = toolCall;

        if (!finalToolCalls[index]) {
            finalToolCalls[index] = toolCall;
        }

        finalToolCalls[index].function.arguments += toolCall.function.arguments;
    }
}
```

Accumulated final\_tool\_calls\[0\]

```json
{
    "index": 0,
    "id": "call_RzfkBpJgzeR0S242qfvjadNe",
    "function": {
        "name": "get_weather",
        "arguments": "{\"location\":\"Paris, France\"}"
    }
}
```