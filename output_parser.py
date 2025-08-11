from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class Summary(BaseModel):
    profile_pic: Optional[str] = Field(default=None, description="profile picture URL")
    summary: str = Field(description="Brief professional summary")
    facts: List[str] = Field(description="2 interesting facts")
    ice_breakers: List[str] = Field(description="3 ice-breaking questions")
    topics_of_interest: List[str] = Field(description="Topics of interest") 

    def to_dict(self) -> Dict[str, Any]:
        return {
            "profile_pic":self.profile_pic,
            "summary":self.summary, 
            "facts":self.facts, 
            "ice_breakers":self.ice_breakers, 
            "topics_of_interest":self.topics_of_interest
            }
summry_parser = PydanticOutputParser(pydantic_object=Summary)