"""
This file contains the nodes of the graph.
Nodes are the building blocks of a graph. They are the smallest unit of work that can be performed in a graph.
"""

import os
import time

from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.search import GmailSearch


class Nodes:
    def __init__(self):
        """
        Initialize the GmailToolkit.
        """
        self.gmail = GmailToolkit()

    def check_email(self, state: dict) -> dict:
        """
        Check for new emails.
        """
        print("# Checking for new emails")
        search = GmailSearch(api_resource=self.gmail.api_resource)
        emails = search.query("after:newer_than:1d")
        checked_emails = state.get("checked_emails_ids", [])
        thread = []
        new_emails = []
        for email in emails:
            if (
                (email.get("id") not in checked_emails)
                and (email.get("threadId") not in thread)
                and (os.environ.get("MY_EMAIL") not in email.get("sender"))
            ):
                thread.append(email.get("threadId"))
                new_emails.append(
                    {
                        "id": email.get("id"),
                        "threadId": email.get("threadId"),
                        "snippet": email.get("snippet"),
                        "sender": email.get("sender"),
                    }
                )
        checked_emails.extend([email.get("id") for email in emails])
        return {**state, "emails": new_emails, "checked_emails_ids": checked_emails}

    def wait_next_run(self, state: dict) -> dict:
        """
        Wait for 180 seconds before checking for new emails again.
        """
        print("## Waiting for 180 seconds")
        time.sleep(180)
        return state

    def new_emails(self, state: dict) -> str:
        """
        Check if there are new emails.
        """
        emails = state.get("emails", [])
        if len(emails) == 0:
            print("## No new emails")
            return "end"
        else:
            print("## New emails")
            return "continue"
