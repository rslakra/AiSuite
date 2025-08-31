# AI Evaluation Dataset

---


```python
from llama_index.evaluation import FaithfulnessEvaluator

# Assuming you have retrieved some context and a response
evaluator = FaithfulnessEvaluator()
eval_result = evaluator.evaluate(
    query="What is the capital of France?",
    response="The capital of France is Paris.",
    contexts=["Paris is the capital of France."]
)

print(eval_result.score) # Output: 1.0 (if the response is fully faithful)
```

> Some examples of LlamaIndex's DatasetGenerator

The LlamaIndex DatasetGenerator is a powerful tool for generating synthetic question-answer pairs and evaluation datasets for your LlamaIndex RAG applications.

Here are some practical examples of how it's used:

1. Generating questions from documents

Imagine you have a large collection of documents (e.g., PDFs, web pages, plain text) that you've indexed using LlamaIndex.
You want to create a test set to evaluate how well your LlamaIndex application answers questions based on this data.
The DatasetGenerator.from_documents method allows you to feed your documents to the generator, which then leverages a Large Language Model (LLM) (e.g., GPT-4) to create relevant questions from the text, as shown in the example on the LlamaIndex website using Paul Graham's essay.
The generated questions can be used to test your Retrieval-Augmented Generation (RAG) pipeline's ability to find the correct information and formulate accurate responses.

2. Creating evaluation datasets 

Beyond simple question generation, the DatasetGenerator can be used to construct more elaborate evaluation datasets, like LabelledRagDataset objects.
These datasets might include not only questions but also the corresponding "ground-truth" answers or context chunks from which the answers are derived, notes LlamaIndex.
This allows for more comprehensive evaluation, measuring aspects like retrieval performance (how well the system retrieves relevant documents) and faithfulness (how well the generated answer aligns with the retrieved context).

3. Leveraging it in evaluation pipelines

The generated datasets, whether simple question lists or more complex LabelledRagDataset objects, are crucial for running evaluations with LlamaIndex's evaluation modules.
For instance, the RetrieverEvaluator can be used to evaluate retrieval performance based on the generated question-context pairs, measuring metrics like hit rate and MRR (Mean Reciprocal Rank).
The generated questions can also be used in conjunction with the RelevancyEvaluator and FaithfulnessEvaluator to assess the quality of the generated answers, as shown in the example in the LlamaIndex documentation.

4. Customizing question generation

The DatasetGenerator allows for some customization of the question generation process, including setting the num_questions_per_chunk (number of questions to generate for each text chunk) and providing custom text_question_template or question_gen_query to guide the question generation process.
This allows users to fine-tune the type and complexity of questions generated to suit their specific evaluation needs. 
In essence, the LlamaIndex DatasetGenerator empowers developers to automate the creation of evaluation data, allowing them to systematically test and improve the performance of their LlamaIndex applications. 



**Code Sample**
```python
import os
from llama_index.core import SimpleDirectoryReader
from llama_index.core.llama_dataset import DatasetGenerator
from llama_index.llms.openai import OpenAI # You'll need to install the llama-index-llms-openai package

# Set up your OpenAI API key
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"  # Replace with your actual key

# 1. Load your documents
# Create a dummy text file for this example (e.g., 'data/paul_graham_essay.txt')
# In a real scenario, you'd load your actual data from PDFs, webpages, etc.
# For example, you might create a file like 'data/my_document.txt' with some text.
documents = SimpleDirectoryReader("./data").load_data()  # Assuming your data is in a 'data' directory

# 2. Initialize the DatasetGenerator
# The DatasetGenerator will use an LLM (e.g., OpenAI's gpt-4) to generate questions
# from your documents.
dataset_generator = DatasetGenerator.from_documents(documents, llm=OpenAI(model="gpt-4"))

# 3. Generate the dataset
# This will generate question-answer pairs based on the content of your documents.
# The `num` parameter limits the total number of question-answer pairs generated.
# The `agenerate_dataset_from_nodes` method asynchronously generates questions for each node.
eval_dataset = await dataset_generator.agenerate_dataset_from_nodes(num=20)

# 4. Access the generated data
# The generated dataset (eval_dataset) contains a dictionary of queries (questions) and responses (ground-truth answers).
queries = eval_dataset.queries
responses = eval_dataset.responses

# 5. Print some examples
print("Generated Questions and Answers:")
for q_id, query in list(queries.items())[:5]:  # Print the first 5 examples
print(f"Question: {query}")
if q_id in responses:
    print(f"Answer: {responses[q_id].response}")
print("---")

# 6. Save the dataset (optional)
# You can save the generated dataset for later use or sharing.
eval_dataset.save_json("generated_rag_dataset.json")

print("\nDataset generated and saved to 'generated_rag_dataset.json'")
```



# Reference

https://docs.llamaindex.ai/en/v0.10.33/module_guides/evaluating/usage_pattern/
https://github.com/run-llama/llama_cloud_services
https://docs.llamaindex.ai/en/v0.10.33/getting_started/concepts/
https://docs.llamaindex.ai/en/v0.10.33/getting_started/starter_example/



# Author

---

* [Rohtash Lakra](https://github.com/rslakra)

