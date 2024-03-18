from mailjet_rest import Client#pip install mailjet-rest
import os

def send_mail(massage:str,recipiants:list[str]):
   """_summary_

   :param massage: _description_
   :type massage: str
   :param recipiants: _description_
   :type recipiants: list[str]
   """
   #print(get_keys())
   #keys=get_keys()
   try:
      api_key=os.getenv("api_key")

      api_secret=os.getenv("api_secret")
      mailjet = Client(auth=(api_key, api_secret), version='v3.1')
      data = {
      'Messages': [
         {
         "From": {
            "Email": "yuvalproject305@gmail.com",
            "Name": "yuval"
         },
         "To": [ 
            {
            "Email": recipiant,
            } for recipiant in recipiants ],
         "Subject": "Greetings from Mailjet.",
         "TextPart": "My first Mailjet email",
         "HTMLPart": "<h3>"+massage+"</h3>",
         "CustomID": "AppGettingStartedTest"
         }
      ]
      }
      result = mailjet.send.create(data=data)
      print(result.status_code)
      print(result.json())
   except:
        print("mail error")


def get_keys():
    file_path="mail_key.txt"
    with open(file_path,"r") as file:
         lines=[line.strip() for line in file.readlines()]
    return lines
if __name__ == "__main__":
	send_mail("hey",[])