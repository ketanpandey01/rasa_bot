# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import psycopg2
from rasa_sdk.events import SlotSet, UserUtteranceReverted
import cx_Oracle as cx
import numpy as np
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


class ActionFetchSOHDetails(Action):
    """
    Show more results of the restaurants
    """

    def name(self) -> Text:
        return "action_fetch_SOH_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        skuNo = tracker.get_slot("SKU_No")
        storeNo = next(tracker.get_latest_entity_values("store_No"), None)

        print(skuNo)
        print(storeNo)
        try:
            db = cx.Connection('vigarg_ts/GapInfosys1234$$@ISCRMSBE')
            cursor = cx.Cursor(db)
            sql = "select stock_on_hand from item_loc_soh where item = %d and loc = %d " % (
                int(skuNo), int(storeNo))
            print(sql)
            cursor.execute(sql)
            rmatrix = np.matrix(cursor.fetchmany())
            print('Matrix size ', rmatrix.shape)
            print('Item Store SOH Details \n', rmatrix[:1, :])
            cursor.close()
            db.close()
            # if(rmatrix[:1, :]==[]):
            #     dispatcher.utter_message(text="Data corresponding to your request doesn't exist")
            #     dispatcher.utter_message(text="Please try with the correct sku/store number")
            # else:
            dispatcher.utter_message(text="Found these results")
            dispatcher.utter_message(text=str(rmatrix[:1, :]))
            return []
        except Exception as e:
            print("Uh oh, can't connect. Invalid dbname, user or password?")
            print(e)
            dispatcher.utter_message("I am not able to connect at the moment")


# class ActionShowNewPO(Action):
#     """
#     Show more results of the restaurants
#     """
#     def name(self) -> Text:
#         return "action_show_new_po"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         legacyPo_Entity=next(tracker.get_latest_entity_values("legacyPO_No"), None)
#         print(legacyPo_Entity)
#         try:
#             # item = int(input('Enter the SKU#: '))
#             # print (item)
#             # store = int(input('Enter the Store# where you would like to query SOH for item '))
#             # print (store)
#             item = 301834468
#             store = 1406
#             db = cx.Connection('vigarg_ts/GapInfosys1234$$@ISCRMSBE')
#             cursor = cx.Cursor(db)
#             sql = "select stock_on_hand from item_loc_soh where item = %d and loc = %d " % (item, store)
#             print(sql)
#             cursor.execute(sql)
#             rmatrix=np.matrix(cursor.fetchmany())
#             print('Matrix size ', rmatrix.shape)
#             print('Item Store SOH Details \n', rmatrix[:1,:])
#             cursor.close()
#             db.close()
#             dispatcher.utter_message(text=rmatrix[:1,:])
#             return []
#         except Exception as e:
#             print("Uh oh, can't connect. Invalid dbname, user or password?")
#             print(e)
