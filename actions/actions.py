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
# import psycopg2
from rasa_sdk.events import SlotSet, UserUtteranceReverted
import cx_Oracle as cx
import numpy as np
import json
import spacy
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
        # dispatcher.utter_message(template="utter_choose_conversation_path")
        return [UserUtteranceReverted()]


class ActionFetchMultiDetails(Action):
    """
    Show more results of the restaurants
    """

    def name(self) -> Text:
        return "action_fetch_multi_details"

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
            try:
                db = cx.Connection('')
                cursor = cx.Cursor(db)
                excelData = json.loads(metadata)
                outputJson = []
                if('ITEM' in excelData[0].keys()):
                    for row in excelData:
                        print(row["ITEM"],row["LOC"])
                        sql = "select unit_cost from item_loc_soh where item = %d and loc = %d " % (int(row["ITEM"]), int(row["LOC"]))
                        cursor.execute(sql)
                        res = cursor.fetchone()
                        outputRow = {}
                        outputRow["UnitCost"] = res
                        outputJson.append(outputRow)
                elif('LEGACY_ORD_NO' in excelData[0].keys()):
                    for row in excelData:
                        print(row["LEGACY_ORD_NO"])
                        sql = "select PO_PFX_NBR||PO_DC_ID as LEGACY_ORD_NBR, egi_ord_nbr from POORX_PO_XREF_T where PO_PFX_NBR||PO_DC_ID = '%s' " % (row["LEGACY_ORD_NO"])
                        cursor.execute(sql)
                        res = cursor.fetchone()                      
                        outputRow = {}
                        outputRow["NewPO"] = res[1]
                        outputJson.append(outputRow)
                
                print(json.dumps(outputJson))
                message = {"payload": "excelData", "data": json.dumps(outputJson)}
                dispatcher.utter_message(text="Ouput Excel Generated", json_message=message)
            except Exception as e:
                print("Uh oh, can't connect. Invalid dbname, user or password?")
                print(e)
                dispatcher.utter_message(text="Cannot fulfill your request right now")


            


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

        return {"SKU_No": [self.from_text(not_intent="chitchat")], "store_No": [self.from_text(not_intent="chitchat")]}

    def validate_SKU_No(self,value: Text,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> Dict[Text, Any]:
        """Validate cuisine value."""

        print("SKU1: ",value)
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(value)
        skuNo = None
        for token in doc:
            if token.like_num:
                skuNo = token
                break
        print("SKU2: ", skuNo)
        if skuNo==None:
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            # dispatcher.utter_message(template="utter_wrong_SKU_No")
            return {"SKU_No": None}
        else:
            # validation succeeded, set the value of the "SKU_No" slot to value
            return {"SKU_No": skuNo.text}

    def validate_store_No(self,value: Text,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> Dict[Text, Any]:
        """Validate cuisine value."""

        print("store1: ",value)
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(value)
        storeNo = None
        for token in doc:
            if token.like_num:
                storeNo = token
                break
        print("store2: ",storeNo)
        if storeNo==None:
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            # dispatcher.utter_message(template="utter_wrong_store_No")
            return {"store_No": None}
        else:
            # validation succeeded, set the value of the "store_No" slot to value
            return {"store_No": storeNo.text}

    def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> List[Dict]:
        skuNo = tracker.get_slot("SKU_No")
        storeNo = tracker.get_slot("store_No")
        print("sku: ", skuNo)
        print("store: ", storeNo)
        try:
            db = cx.Connection('')
            cursor = cx.Cursor(db)
            sql = "select stock_on_hand from item_loc_soh where item = %d and loc = %d " % (int(skuNo), int(storeNo))
            print(sql)
            cursor.execute(sql)
            res = cursor.fetchone()
            # print('Matrix size ', rmatrix.shape)
            # print('Item Store SOH Details \n', rmatrix[:1, :])
            cursor.close()
            db.close()
                # if(rmatrix[:1, :]==[]):
                #     dispatcher.utter_message(text="Data corresponding to your request doesn't exist")
                #     dispatcher.utter_message(text="Please try with the correct sku/store number")
                # else:
            if res==None:    
                dispatcher.utter_message(text="No information found for your query. Please provide the correct details")
            else:
                #310691496
                resultStr = "SOH Details: "+'<br>'
                resultStr += "SKU No: " + skuNo + '<br>' + "Store No: " + storeNo + '<br>' + "Stock on hand: " + str(res[0])
                dispatcher.utter_message(text=resultStr)
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

        return {"legacyPo": [self.from_text(not_intent="chitchat")]}

    def validate_legacyPo(self,value: Text,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> Dict[Text, Any]:
        """Validate legacyPo value."""

        # print(value)
        # nlp = spacy.load("en_core_web_sm")
        # doc = nlp(value)
        legacyPo_No = value
        # for token in doc:
        #     if token.is_alpha and token.is_digit:
        #         legacyPo_No = token
        #         break
        print("legacyPO: ",legacyPo_No)
        if legacyPo_No==None:
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            # dispatcher.utter_message(template="utter_wrong_legacyPo")
            return {"legacyPo": None}
        else:
            # validation succeeded, set the value of the "legacyPo" slot to value
            return {"legacyPo": legacyPo_No}


    def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> List[Dict]:

        legacyPo = tracker.get_slot("legacyPo")
        print("legacyPO :",legacyPo)
        try:
            db = cx.Connection('')
            cursor = cx.Cursor(db)
            # sql = "select egi_ord_nbr from POORX_PO_XREF_T where PO_PFX_NBR||PO_DC_ID = %d " % legacyPo
            sql = "select PO_PFX_NBR||PO_DC_ID as LEGACY_ORD_NBR, egi_ord_nbr from POORX_PO_XREF_T where PO_PFX_NBR||PO_DC_ID = '%s' " % (legacyPo)
            print(sql)
            cursor.execute(sql)
            res = cursor.fetchone()
            cursor.close()
            db.close()
            if res==None:    
                dispatcher.utter_message(text="No information found for your query. Please provide the correct details")
            else:
                resultStr = "PO Details: "+'<br>'
                resultStr += "LegacyPo No: " + legacyPo + '<br>' + "NewPo No: " + str(res[1])
                dispatcher.utter_message(text=resultStr)
            return []
        except Exception as e:
            print("Uh oh, can't connect. Invalid dbname, user or password?")
            print(e)
            return []

class ActionDefaultAskAffirmation(Action):
   """Asks for an affirmation of the intent if NLU threshold is not met."""

   def name(self):
       return "action_default_ask_affirmation"


   def run(self, dispatcher, tracker, domain):
    #    # get the most likely intent
    #    last_intent_name = tracker.latest_message['intent']['name']

    #    # get the prompt for the intent
    #    intent_prompt = self.intent_mappings[last_intent_name]

    #    # Create the affirmation message and add two buttons to it.
    #    # Use '/<intent_name>' as payload to directly trigger '<intent_name>'
    #    # when the button is clicked.
    #    message = "Sorry, I'm not sure I've understood you correctly. I can help you with the following: "
    #    buttons = [{'title': 'Yes',
    #                'payload': '/{}'.format(last_intent_name)},
    #               {'title': 'No',
    #                'payload': '/out_of_scope'}]
    #    dispatcher.utter_button_message(message, buttons=buttons)
       dispatcher.utter_message(template="utter_choose_conversation_path")

       return []

class ActionFindGLMapping(Action):
    """
    Show more results of the restaurants
    """

    def name(self) -> Text:
        return "action_find_GL_mapping"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            db = cx.Connection('')
            cursor = cx.Cursor(db)
            outputJson = []
            glMappingSQL = "SELECT DISTINCT a.dept, a.location, a.tran_code, DECODE (a.tran_code,'23', a.gl_ref_no, -1) tran_ref_no, 'C' cost_retail_flag FROM tran_data_history a WHERE post_date BETWEEN (SELECT last_eom_date + 1 FROM system_variables ) AND (SELECT next_eom_date FROM system_variables) AND tran_code IN ( select substr(code,0,2) from code_detail where code_type='GLMT') UNION SELECT DISTINCT a.dept, a.location, a.tran_code, DECODE (a.tran_code,'23', a.gl_ref_no, -1) tran_ref_no, 'C' cost_retail_flag FROM tran_data a WHERE tran_date BETWEEN (SELECT last_eom_date + 1 FROM system_variables) AND (SELECT next_eom_date FROM system_variables) AND tran_code IN (select substr(code,0,2) from code_detail where code_type='GLMT') MINUS /*The below sql will get all available mapping in GL */ SELECT DISTINCT b.dept, b.location, b.tran_code, NVL (b.tran_ref_no, -1) tran_ref_no, b.cost_retail_flag FROM fif_gl_cross_ref b WHERE tran_code IN (select substr(code,0,2) from code_detail where code_type='GLMT') UNION SELECT DISTINCT a.dept, a.location, 51 tran_code, NULL tran_ref_no, 'C' cost_retail_flag FROM month_data a WHERE eom_date = (SELECT next_eom_date FROM system_variables) AND (nvl(stocktake_bookstk_cost,0) - nvl(stocktake_actstk_cost,0)) <> 0 MINUS /*The below sql will get all available mapping in GL */ SELECT DISTINCT b.dept, b.location, 51 tran_code, NULL tran_ref_no, b.cost_retail_flag FROM fif_gl_cross_ref b WHERE tran_code = 51 UNION SELECT DISTINCT a.dept, a.location, DECODE (a.tran_code,1,51,41,51,a.tran_code) tran_code, NULL tran_ref_no, 'C' cost_retail_flag FROM tran_data_history a WHERE post_date BETWEEN (SELECT last_eom_date FROM system_variables) AND (SELECT next_eom_date FROM system_variables) AND tran_code IN ('1','41') UNION SELECT DISTINCT a.dept, a.location, DECODE (a.tran_code, 1, 51,41,51,a.tran_code) tran_code, NULL tran_ref_no, 'C' cost_retail_flag FROM tran_data a WHERE tran_date BETWEEN (SELECT last_eom_date FROM system_variables) AND (SELECT next_eom_date FROM system_variables) AND tran_code IN ('1', '41') MINUS /*The below sql will get all available mapping in GL */ SELECT DISTINCT b.dept, b.location, b.tran_code, NULL tran_ref_no, b.cost_retail_flag FROM fif_gl_cross_ref b WHERE tran_code ='51' ORDER BY 3,2,1"
            cursor.execute(glMappingSQL)
            res = cursor.fetchall()
            if(res is not None):
                for row in res:
                    outputJson.append({'DEPT': row[0], 'LOCATION': row[1], 'TRAN_CODE': row[2], 'TRAN_REF_NO': row[3], 'COST_RETAIL_FLAG': row[4]})
                print(json.dumps(outputJson))
                
            message = {"payload": "excelData", "data": json.dumps(outputJson)}
            dispatcher.utter_message(text="GL Mapping Excel Generated", json_message=message)
        except Exception as e:
            print("Uh oh, can't connect. Invalid dbname, user or password?")
            print(e)
            dispatcher.utter_message(text="Cannot fulfill your request right now")


        

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
#             db = cx.Connection('')
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
