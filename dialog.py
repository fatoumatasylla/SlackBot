
def get_dialog(callback_id):
  dialog = {

  'askcauses': {
    "title":"Partages-tu cette cause?",  
    "callback_id":callback_id,
    "submit_label":"Enregister",
    "notify_on_cancel": "true",
    "elements": [
      {
        "label": "DÉVELOPPER LE VIETNAM",
        "type": "select",
        "name":"1",
        "options": [
          {"label": "oui", "value": "1" },
          {"label": "non","value": "0"}
          ]
        },
      {
        "label": "ENCOURAGER LA MONDIALISATION POSITIVE",
        "type": "select",
        "name":"2",
        "options": [
          {"label": "oui","value": "1"},
          {"label": "non","value": "0"}]
      },
      {
        "label": "CRÉER DE LA VALEUR PARTAGÉE",
        "type": "select",
        "name":"3",
        "options": [
          {"label": "oui", "value": "1" },
          {"label": "non","value": "0"}
          ]
        },
        {
        "label": "PENSER ET AGIR DURABLE",
        "type": "select",
        "name":"4",
        "options": [
         {"label": "oui", "value": "1" },
         {"label": "non","value": "0"}
          ]
        },
        {
        "label": "PARTAGER LE SAVOIR",
        "type": "select",
        "name":"5",
        "options": [
          {"label": "oui", "value": "1" },
          {"label": "non","value": "0"}
          ]
  }]
}
  }
  return dialog