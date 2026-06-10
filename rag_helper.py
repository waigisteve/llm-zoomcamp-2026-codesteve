INSTRUCTIONS = """
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."
"""

PROMPT_TEMPLATE = """
QUESTION: {question}

CONTEXT:
{context}
""".strip()


class RAGBase:
    def __init__(
        self,
        index,
        llm_client,
        instructions: str = INSTRUCTIONS,
        prompt_template: str = PROMPT_TEMPLATE,
        course: str = "llm-zoomcamp",
        model: str = "gpt-5.4-mini",
    ) -> None:
        self.index = index
        self.llm_client = llm_client
        self.instructions = instructions
        self.course = course
        self.prompt_template = prompt_template
        self.model = model

    def search(self, query: str, num_results: int = 5) -> list[dict]:
        return self.index.search(
            query=query,
            filter_dict={"course": self.course},
            boost_dict={"question": 3.0, "section": 0.5},
            num_results=num_results,
        )

    def build_context(self, search_results: list[dict]) -> str:
        context_parts = []

        for result in search_results:
            context_parts.append(
                f"section: {result['section']}\n"
                f"question: {result['question']}\n"
                f"answer: {result['answer']}"
            )

        return "\n\n".join(context_parts)

    def build_prompt(self, question: str, context: str) -> str:
        return self.prompt_template.format(question=question, context=context)

    def llm(self, prompt: str) -> str:
        response = self.llm_client.responses.create(
            model=self.model,
            instructions=self.instructions,
            input=prompt,
        )
        return response.output_text

    def rag(self, question: str) -> str:
        search_results = self.search(question)
        context = self.build_context(search_results)
        prompt = self.build_prompt(question, context)
        return self.llm(prompt)
