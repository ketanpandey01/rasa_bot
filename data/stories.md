## greet
* greet
  - utter_greet

## asking for legacyPO, without number
* legacyPO
  - legacypo_form
  - form{"name": "legacypo_form"}
  - form{"name": null}
 <!-- - utter_ask_legacyPO_number -->

## asking for legacyPO, with number
* legacyPO{"legacyPO_No":"123456"}
 - action_show_new_po

## asking for multiple SOH details
* SOHDetails
  - utter_request_type
* multipleRequest
  - utter_uploadAttachment
* UploadAttachment
  - action_fetch_multi_SOH_details

## asking for single SOH details
* SOHDetails
  - utter_request_type
* singleRequest
  - sohDetails_form
  - form{"name": "sohDetails_form"}
  - form{"name": null}



<!-- * inform{"SKU_No":"123456789"}
  - slot{"SKU_No":"123456789"}
  - utter_ask_store_No
* inform{"store_No":"6789"}
  - action_fetch_SOH_details -->

<!-- ## asking for SKU, without number
* SKU
  - utter_on_it
  - utter_ask_SKU_number

## asking for SKU, with number
* SKU{"SKU_No":"123456789"}
  - slot{"SKU_No":"123456789"}
  - utter_ask_store_number
* Store{"store_No":"6789"}
  - action_fetch_SOH_details -->


## thank
* thank
  - utter_noworries



<!--
## goodbye
* goodbye
  - utter_goodbye

## order form
* itemOrder
    - order_form
    - form{"name": "order_form"}
    - form{"name": null} -->


<!-- ## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot -->
