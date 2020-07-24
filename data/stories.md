## story_0
* chitchat
  - respond_chitchat


## asking for single SOH details(without chitchat)
* SOHDetails
  - utter_request_type
* singleRequest
  - sohDetails_form
  - form{"name": "sohDetails_form"}
  - form{"name": null}

## asking for single SOH details(with chitchat)
* SOHDetails
  - utter_request_type
* chitchat
  - respond_chitchat
  - utter_request_type
* singleRequest
  - sohDetails_form
  - form{"name": "sohDetails_form"}
* chitchat
  - respond_chitchat
  - sohDetails_form
  - form{"name": null}

## asking for multiple SOH details(without chitchat)
* SOHDetails
  - utter_request_type
* multipleRequest
  - utter_uploadAttachment
* UploadAttachment
  - action_fetch_multi_details

## asking for multiple SOH details(with chitchat)
* SOHDetails
  - utter_request_type
* chitchat
  - respond_chitchat
  - utter_request_type
* multipleRequest
  - utter_uploadAttachment
* UploadAttachment
  - action_fetch_multi_details

## asking for single legacy details(without chitchat)
* legacyPO
  - utter_request_type
* singleRequest
  - legacypo_form
  - form{"name": "legacypo_form"}
  - form{"name": null}

## asking for single legacy details(with chitchat)
* legacyPO
  - utter_request_type
* chitchat
  - respond_chitchat
  - utter_request_type
* singleRequest
  - legacypo_form
  - form{"name": "legacypo_form"}
* chitchat
  - respond_chitchat
  - legacypo_form
  - form{"name": null}

## asking for multiple legacy details(without chitchat)
* legacyPO
  - utter_request_type
* multipleRequest
  - utter_uploadAttachment
* UploadAttachment
  - action_fetch_multi_details

## asking for multiple legacy details(with chitchat)
* legacyPO
  - utter_request_type
* chitchat
  - respond_chitchat
  - utter_request_type
* multipleRequest
  - utter_uploadAttachment
* UploadAttachment
  - action_fetch_multi_details




## thank
* thank
  - utter_noworries



