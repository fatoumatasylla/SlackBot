attachements = {
        'firstmessage':[
        {	
            "fallback": "Saviez-vous que l’espace d’Offycare est fondé autour de cinq causes ?",
            "title":"Saviez-vous que l’espace d’Offycare est fondé autour de cinq causes ?",
            "callback_id": "fristquestion",
            "color": "warning",
            "attachment_type": "default",
            "response_type": "in_channel",
            "text":"Utilises\"/offyvalues\" pour enter tes causes \nTu pourras par la suite utiliser \"/meet\" pour être mis en relation avec un Offy friend qui à une ou des causes en commun avec toi." ,
            "actions": [
                {
                    "name": "Enregister",
                    "text": "Enter mes causes",
                    "type": "button",
                    "value": "Enregister",
					"style":"primary",
                    
                }
            ]
    
        }
    ],
    "/addoffyvalues":[
        {	
            "fallback": "Saviez-vous que l’espace d’Offycare est fondé autour de cinq causes ?",
            "title":"Saviez-vous que l’espace d’Offycare est fondé autour de cinq causes ?",
            "callback_id": "fristquestion",
            "color": "primary",
            "actions": [
                {
                    "name": "fromcaues",
                    "text": "Enter mes causes",
                    "type": "button",
                    "value": "formcause",
					"style":"primary",
                    "confirm": {
                    "title": "Are you sure?",
                    "text": "Enregister ses causes ?",
                    "ok_text": "Yes",
                    "dismiss_text": "No"
                    }
                }
            ]
        }
    ],

    'presoffyvalues':[
            {	
                "text": "Les causes d'Officience <https://officience.com/fr/| (En savoir plus)> :\nDÉVELOPPER LE VIETNAM\nENCOURAGER LA MONDIALISATION POSITIVE\nCRÉER DE LA VALEUR PARTAGÉE\nPENSER ET AGIR DURABLE\nPARTAGER LE SAVOIR\nTu est desormais un offy à 50 %",
                "image_url":"https://drive.google.com/file/d/1scNFKH-iuwlsnJaj9Y6KU7FhfdHwTAiN/view?usp=sharing",
                "fallback": "Quel sont tes causes ?",
                "color": "warning"
            }		
        ],

    'enregister':[
        {	"title":"Quelles causes partages-tu ?",
            "fallback": "matching ",
            "callback_id": "formcauses",
            "attachment_type": "default",
            "color":"danger",
            "text":"Utilises\"/updatevalue\" pour mettre à jours tes caues\nTu pourras par la suite utiliser \"/meet\" pour être mis en relation avec un Offy friend qui à une ou des causes en commun avec toi." ,

            "actions": [
                {
                    "name": "Enregister",
                    "text": "Enter mes causes",
                    "type": "button",
                    "value": "Enregister",
					"style":"primary",
                    
                }
            ]
        }
    ],
    'update'  :[
        {	"title":"Update cause(s)",
            "fallback": "matching ",
            "callback_id": "update",
            "attachment_type": "default",
            "color":"danger",
            "text":"Utilises \"/updatevalue\" pour mettre à jours tes caues\nTu pourras par la suite utiliser \"/match\" pour être mis en relation avec un Offy friend qui à une ou des causes en commun avec toi." ,

            "actions": [
                {
                    "name": "update",
                    "text": "Enter mes causes",
                    "type": "button",
                    "value": "update",
					"style":"primary",
            
                }
            ]
        }
    ],

    'match':[
        {	 
            "fallback": "matching ",
            "callback_id": "match",
            "attachment_type": "default",
            "color":"danger",
            "text":"",
            "actions":[{
                    "name": "match",
                    "text": "Matcher",
                    "type": "button",
                    "value": "match",
					"style":"danger"
                }
            ]
        }
    ]   
}
 
offyvalues = { 
    "1": "DÉVELOPPER LE VIETNAM",
    "2": "ENCOURAGER LA MONDIALISATION POSITIVE",
    "3": "CRÉER DE LA VALEUR PARTAGÉE",
    "4": "PENSER ET AGIR DURABLE",
    "5": "PARTAGER LE SAVOIR"
}


cause_id = { 
    "DÉVELOPPER LE VIETNAM":"1",
    "ENCOURAGER LA MONDIALISATION POSITIVE":"1",
    "CRÉER DE LA VALEUR PARTAGÉE":"3",
    "PENSER ET AGIR DURABLE": "4",
    "PARTAGER LE SAVOIR":"5" 
}
