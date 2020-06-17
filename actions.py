# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import psycopg2
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionGreetUser(Action):
    """
    Greet user for the first time he has opened the bot windows
    """
    def name(self) -> Text:
        return "action_greet_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_greet_user")   
        return [UserUtteranceReverted()]

class ActionShowNewPO(Action):
    """
    Show more results of the restaurants
    """
    def name(self) -> Text:
        return "action_show_new_po"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        legacyPo_Entity=next(tracker.get_latest_entity_values("location"), None)
        
        try:
            conn = psycopg2.connect(host="localhost",database="kpTestDB", user="kp", password="november1@KP")
            # create a psycopg2 cursor that can execute queries
            cursor = conn.cursor()
            cursor.execute("""select new_po from legacypo where legacy_po=legacyPo_Entity""")
            conn.commit() # <--- makes sure the change is shown in the database
            rows = cursor.fetchall()
            print(rows)
            cursor.close()
            conn.close()
            dispatcher.utter_message(text=rows)
            return []
        except Exception as e:
            print("Uh oh, can't connect. Invalid dbname, user or password?")
            print(e)
