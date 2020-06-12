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

# class ActionShowNewPO(Action):
#     """
#     Show more results of the restaurants
#     """
#     def name(self) -> Text:
#         return "action_show_new_po"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         restaurants = tracker.get_slot("more_restaurants")
#         if restaurants!=None:
#             if(tracker.get_latest_input_channel()=="slack"):
#                 restData = getResto_Slack(restaurants,show_more_results=False)
#                 dispatcher.utter_message(text="Here are few more restaurants",json_message=restData)
#             else:
#                 dispatcher.utter_message(text="Here are few more restaurants",json_message={"payload":"cardsCarousel","data":restaurants})
            
#             return [SlotSet("more_restaurants", None)] 
#         else:
#             dispatcher.utter_message(text="Sorry No more restaurants found")
#             return []
