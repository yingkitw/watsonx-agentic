from dotenv import load_dotenv
import os, json
import requests

proxy = "proxy.us.ibm.com:8080"

class WatsonxAI:
    GRANITE_3B_CODE_INSTRUCT = "ibm/granite-3b-code-instruct"
    GRANITE_8B_CODE_INSTRUCT = "ibm/granite-8b-code-instruct"
    GRANITE_20B_CODE_INSTRUCT = "ibm/granite-20b-code-instruct"
    GRANITE_34B_CODE_INSTRUCT = "ibm/granite-34b-code-instruct"
    GRANITE_13B_CHAT_V2 = "ibm/granite-13b-chat-v2"
    GRANITE_13B_INSTRUCT_V2 = "ibm/granite-13b-instruct-v2"
    GRANITE_20B_MULTILINGUAL = "ibm/granite-20b-multilingual"
    LLAMA_3_70B_INSTRUCT = "meta-llama/llama-3-70b-instruct"

    project_id = None
    api_key = None
    access_token = None 
    ibm_cloud_iam_url = None

    def connect(self):

        load_dotenv()
        self.api_key = os.getenv("API_KEY", None)
        self.project_id = os.getenv("PROJECT_ID", None)
        self.ibm_cloud_iam_url = os.getenv("IAM_IBM_CLOUD_URL", None)

        creds = {
            "url"    : "https://us-south.ml.cloud.ibm.com",
            "apikey" : self.api_key
        }

        # Prepare the payload and headers
        payload = {
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": self.api_key
        }
        headers = {
            'Content-Type': "application/x-www-form-urlencoded"
        }

        # Make a POST request while ignoring SSL certificate verification
        try:
            response = requests.post(f"https://{self.ibm_cloud_iam_url}/identity/token", data=payload, headers=headers, verify=False)
            
            # Check if the request was successful
            response.raise_for_status()

            # Parse the JSON response
            decoded_json = response.json()
            self.access_token = decoded_json["access_token"]
            return self.access_token
            # print(f"Access Token: {access_token}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def watsonx_gen(self,prompt,model_id):
        params = {
            "decoding_method":"greedy",
            "max_new_tokens":500,
            "min_new_tokens":1,
            # "temperature":0.1,
            "top_k":50,
            "top_p":1,
            "stop_sequences":["[/INST]"],
        }

        url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation_stream?version=2023-05-29"

        body = {
            "input": prompt,
            "parameters": params,
            "model_id": model_id,
            "project_id": self.project_id
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.post(
            url,
            headers=headers,
            json=body,
            stream=True
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        answer = ""
        # Stream the response
        for line in response.iter_lines():
            if line:  # Ensure the line is not empty
                decoded_line = line.decode("utf-8").strip()
                
                # Check if the line starts with "data: "
                if decoded_line.startswith("data: "):
                    json_data = decoded_line[len("data: "):]  # Remove the "data: " prefix
                    
                    try:
                        # Attempt to load the JSON data
                        data = json.loads(json_data)
                        generated_text = data.get("results", "")
                        answer += generated_text[0]["generated_text"]
                        # print(generated_text[0]["generated_text"],end="")  # Print or process the generated text as needed
                    except json.JSONDecodeError:
                        print("Failed to decode JSON:", json_data)
                    except Exception as e:
                        print("An error occurred:", e)

        return answer
