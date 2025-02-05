# from livekit.agents import llm
# import enum 
# from typing import Annotated
# import logging
# from db_driver import DatabaseDriver

# logger = logging.getLogger("user-data")
# logger.setLevel(logging.INFO)

# DB = DatabaseDriver()

# class CandidateDetails(enum.Enum):
#     id="id"
#     job_profile="job_profile"
#     name="name"
#     email="email"
#     phone="phone"
    


# class AssistantFnc(llm.FunctionContext):
#     def __init__(self):
#         super().__init__()
        
#         self._candidate_details = {
#              CandidateDetails.ID = "",
#              CandidateDetails.JOB_PROFILE = "",
#              CandidateDetails.NAME = "",
#              CandidateDetails.Email = "",
#              CandidateDetails.PHONE = ""
#             }   
        
    
    
from livekit.agents import llm
import enum
from typing import Annotated
import logging
from db_driver import DatabaseDriver

logger = logging.getLogger("user-data")
logger.setLevel(logging.INFO)

DB = DatabaseDriver()

class CandidateDetails(enum.Enum):
    ID="id"
    JOB_PROFILE="job_profile"
    NAME="name"
    EMAIL="email"
    PHONE="phone"
    

class AssistantFnc(llm.FunctionContext):
    def __init__(self):
        super().__init__()
        
        self._candidate_details = {
            CandidateDetails.ID: "",
            CandidateDetails.JOB_PROFILE: "",
            CandidateDetails.NAME: "",
            CandidateDetails.EMAIL: "",
            CandidateDetails.PHONE: ""
        }
    
    def get_candidate_str(self):
        candidate_str = ""
        for key, value in self._candidate_details.items():
            candidate_str += f"{key}: {value}\n"
            
        return candidate_str
    
    @llm.ai_callable(description="lookup a candidate by its id")
    def lookup_candidate(self, id: Annotated[str, llm.TypeInfo(description="The id of the candidate to lookup")]):
        logger.info("lookup candidate - id: %s", id)
        
        result = DB.get_candidate_by_id(id)
        if result is None:
            return "Candidate not found"
        
        self._candidate_details = {
            CandidateDetails.ID: result.id,
            CandidateDetails.JOB_PROFILE: result.job_profile,
            CandidateDetails.NAME: result.name,
            CandidateDetails.EMAIL: result.email,
            CandidateDetails.PHONE: result.phone
        }
        
        return f"The candidate details are: {self.get_candidate_str()}"
    
    @llm.ai_callable(description="get the details of the current candidate")
    def get_candidate_details(self):
        logger.info("get candidate  details")
        return f"The candidate details are: {self.get_candidate_str()}"
    
    @llm.ai_callable(description="create a new candidate")
    def create_candidate(
        self, 
        job_profile: Annotated[str, llm.TypeInfo(description="The job_profile of the candidate")],
        name: Annotated[str, llm.TypeInfo(description="The model of the candidate")],
        email: Annotated[int, llm.TypeInfo(description="The year of the candidate")],
        phone: Annotated[int, llm.TypeInfo(description="The year of the candidate")]
    ):
        logger.info("create candidate -  job_profile: %s, name: %s, email: %s, phone: %s", job_profile, name, email,phone)
        result = DB.create_candidate(job_profile,name,email,phone)
        if result is None:
            return "Failed to create candidate"
        
        self._candidate_details = {
            CandidateDetails.ID: result.id,
            CandidateDetails.JOB_PROFILE: result.job_profile,
            CandidateDetails.NAME: result.name,
            CandidateDetails.EMAIL: result.email,
            CandidateDetails.PHONE: result.phone
        }
        
        return "candidate created!"
    
    def has_candidate(self):
        return self._candidate_details[CandidateDetails.ID] != ""