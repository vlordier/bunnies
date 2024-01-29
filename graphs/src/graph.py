"""
    This module is responsible for creating the workflow graph.
"""
from dotenv import load_dotenv

load_dotenv()

from langgraph.graph import StateGraph

from .crew.crew import EmailFilterCrew
from .nodes import Nodes
from .state import EmailsState


class WorkFlow:
    """
    This class is responsible for creating the workflow graph.
    """

    def __init__(self):
        """
        Initialize the workflow graph.
        """
        nodes = Nodes()
        workflow = StateGraph(EmailsState)

        workflow.add_node("check_new_emails", nodes.check_email)
        workflow.add_node("wait_next_run", nodes.wait_next_run)
        workflow.add_node("draft_responses", EmailFilterCrew().kickoff)

        workflow.set_entry_point("check_new_emails")
        workflow.add_conditional_edges(
            "check_new_emails",
            nodes.new_emails,
            {"continue": "draft_responses", "end": "wait_next_run"},
        )
        workflow.add_edge("draft_responses", "wait_next_run")
        workflow.add_edge("wait_next_run", "check_new_emails")
        self.app = workflow.compile()
