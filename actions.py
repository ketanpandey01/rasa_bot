# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import psycopg2
from rasa_sdk.events import SlotSet, UserUtteranceReverted
import cx_Oracle as cx
import numpy as np
import json
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
        dispatcher.utter_message(template="utter_choose_conversation_path")
        return [UserUtteranceReverted()]


class ActionFetchMultiSOHDetails(Action):
    """
    Show more results of the restaurants
    """

    def name(self) -> Text:
        return "action_fetch_multi_SOH_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        events = tracker.current_state()['events']
        user_events = []
        for e in events:
            if e['event'] == 'user':
                user_events.append(e)

        metadata = user_events[-1]['metadata']

        # return user_events[-1]['metadata']
        if(metadata != {}):
            # dispatcher.utter_message(text=metadata)
            excelData = json.loads(metadata)
            outputJson = []
            for row in excelData:
                print(row["ITEM"])
                print(row["LOC"])
                outputRow = {}
                # outputRow["outputSKU"] = row["SKU"]
                # outputRow["outputStore"] = row["Store"]
                # outputJson.append(outputRow)
                try:
                    db = cx.Connection('vigarg_ts/GapInfosys1234$$@ISCRMSBE')
                    cursor = cx.Cursor(db)
                    sql = "select item, loc, stock_on_hand from item_loc_soh where item = %d and loc = %d " % (int(row["ITEM"]), int(row["LOC"]))
                    cursor.execute(sql)
                    res = cursor.fetchone()
                    outputRow["Result"] = res
                    outputJson.append(outputRow)
                except Exception as e:
                    print("Uh oh, can't connect. Invalid dbname, user or password?")
                    print(e)
            print(json.dumps(outputJson))
            message = {"payload": "excelData", "data": json.dumps(outputJson)}
            dispatcher.utter_message(text="Ouput Excel Generated", json_message=message)


# class HandleRequestType(Action):

#     def name(self) -> Text:
#         return "action_handle_request_type"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         reqType = next(tracker.get_latest_entity_values("requestType"), None)
#         print(reqType)
#         if(str(reqType).upper() == "SINGLE"):
#             # [rasa_sdk.events.FollowupAction("sohDetails_form")]
#             dispatcher.utter_message(text="please provide the SKU number?")
#         else:
#             dispatcher.utter_message(text="please upload excel data", buttons=[
#                                      {"title": "Upload Excel", "payload": ""}])
#             # dispatcher.utter_message(text="please upload excel data")

#         return []


class SOHDetailsForm(FormAction):
    """Collects sales information and adds it to the spreadsheet"""

    def name(self):
        return "sohDetails_form"

    @staticmethod
    def required_slots(tracker): return ["SKU_No","store_No"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
        - an extracted entity
        - intent: value pairs
        - a whole message
        or a list of them, where a first match will be picked"""

        return {"SKU_No": [self.from_text(intent="inform")], "store_No": [self.from_text(intent="inform")]}

    # def validate_SKU_No(self,value: Text,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> Dict[Text, Any]:
    #     """Validate cuisine value."""

    #     print(value)

    #     if value.lower() in self.cuisine_db():
    #         # validation succeeded, set the value of the "cuisine" slot to value
    #         return {"cuisine": value}
    #     else:
    #         dispatcher.utter_message(template="utter_wrong_cuisine")
    #         # validation failed, set this slot to None, meaning the
    #         # user will be asked for the slot again
    #         return {"cuisine": None}

    # def validate_store_No(self,value: Text,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> Dict[Text, Any]:
    #     """Validate cuisine value."""

    #     print(value)

    #     # if value.lower() in self.cuisine_db():
    #     #     # validation succeeded, set the value of the "cuisine" slot to value
    #     #     return {"cuisine": value}
    #     # else:
    #     #     dispatcher.utter_message(template="utter_wrong_cuisine")
    #     #     # validation failed, set this slot to None, meaning the
    #     #     # user will be asked for the slot again
    #     #     return {"cuisine": None}

    def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> List[Dict]:
        skuNo = tracker.get_slot("SKU_No")
        storeNo = tracker.get_slot("store_No")
        print("sku: ", skuNo)
        print("store: ", storeNo)
        try:
            db = cx.Connection('vigarg_ts/GapInfosys1234$$@ISCRMSBE')
            cursor = cx.Cursor(db)
            sql = "select stock_on_hand from item_loc_soh where item = %d and loc = %d " % (int(skuNo), int(storeNo))
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
            dispatcher.utter_message("Thanks for getting in touch, we’ll contact you soon")
            return []

class LegacyPoForm(FormAction):
    """Collects sales information and adds it to the spreadsheet"""

    def name(self):
        return "legacypo_form"

    @staticmethod
    def required_slots(tracker): return ["legacyPo"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
        - an extracted entity
        - intent: value pairs
        - a whole message
        or a list of them, where a first match will be picked"""

        return {"legacyPo": [self.from_text(intent="inform")]}


    def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> List[Dict]:

        legacyPo = tracker.get_slot("legacyPo")
        print("legacyPO :",legacyPo)
        try:
            db = cx.Connection('vigarg_ts/GapInfosys1234$$@ISCRMSBE')
            cursor = cx.Cursor(db)
            sql = "select egi_ord_nbr from POORX_PO_XREF_T where PO_PFX_NBR||PO_DC_ID = %d " % int(legacyPo)
            print(sql)
            cursor.execute(sql)
            rmatrix = np.matrix(cursor.fetchmany())
            print('Matrix size ', rmatrix.shape)
            print('LegacyPo \n', rmatrix[:1, :])
            cursor.close()
            db.close()
            dispatcher.utter_message(text=rmatrix)
            return []
        except Exception as e:
            print("Uh oh, can't connect. Invalid dbname, user or password?")
            print(e)
            return []

        

# class ActionShowNewPO(Action):
#     """
#     Show more results of the restaurants
#     """
#     def name(self) -> Text:
#         return "action_show_new_po"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         legacyPo=next(tracker.get_latest_entity_values("legacyPO_No"), None)
#         print(legacyPo)
#         try:
#             db = cx.Connection('vigarg_ts/GapInfosys1234$$@ISCRMSBE')
#             cursor = cx.Cursor(db)
#             sql = "select egi_ord_nbr from POORX_PO_XREF_T where PO_PFX_NBR||PO_DC_ID = %d " % (legacyPo)
#             print(sql)
#             cursor.execute(sql)
#             rmatrix = np.matrix(cursor.fetchmany())
#             print('Matrix size ', rmatrix.shape)
#             print('LegacyPo \n', rmatrix[:1, :])
#             cursor.close()
#             db.close()
#             dispatcher.utter_message(text="Thanks for your query. We are working on this feature.")
#             return []
#         except Exception as e:
#             print("Uh oh, can't connect. Invalid dbname, user or password?")
#             print(e)
