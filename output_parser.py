from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Dict, Any, List

class Summary(BaseModel):
    summary: str = Field(description="summary")
    facts: List[str] = Field(description="Interesting facts about them")
    questions: List[str] = Field(description="Quastions to start")

    def to_dict(self) -> Dict[str, Any]:
        return {"summary":self.summary, "facts":self.facts, "questions":self.questions}
summry_parser = PydanticOutputParser(pydantic_object=Summary)