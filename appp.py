import streamlit 
import requests

api_key = "fb6031e2-7b0f-4118-8ca8-0e9c971dbef9"
headers = {"Authorization": f"Bearer {api_key}"}
url = "https://api.cricapi.com/v1/currentMatches?apikey=fb6031e2-7b0f-4118-8ca8-0e9c971dbef9&offset=0"

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print("Authentication failed!")
matches=response.json()

import requests

api_key = "fb6031e2-7b0f-4118-8ca8-0e9c971dbef9"
headers = {"Authorization": f"Bearer {api_key}"}
url = "https://api.cricapi.com/v1/match_scorecard?apikey=fb6031e2-7b0f-4118-8ca8-0e9c971dbef9&id=1f0d678c-8663-45ba-a4d9-db0d7db94a42"

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print("Authentication failed!")
scorecard=response.json()

x=matches['data']
print(x)
Live_Match=x['matchEnded'==False]
Live_Match_Names=Live_Match['name']
Not_Live_Match = [match for match in x if match.get("matchEnded")==True]
Not_Live_Match_Names=[match['name'] for match in x if match.get("matchEnded")]
print(Live_Match)
print(Live_Match_Names)
print(Not_Live_Match)
print(Not_Live_Match_Names)
sc=scorecard['data']
match_type=sc['matchType']
score=sc['score']
runs=score[0]['r']
overs=score[0]['o']
Net_run_rate=runs/overs
def projected_score(matchType,runs,overs,Net_run_rate):
  if matchType=='odi':
    over_left=50-int(overs)
    return int(runs+Net_run_rate*over_left)
  elif matchType=='T20':
    over_left=20-int(overs)
    return int(runs+Net_run_rate*over_left)
import cohere
co = cohere.Client("sRmFY97EVTJa7VaaaQha5oH7lScl1rxTZv8x6KrV")
def ask_cricket_query(query, context):
    prompt = f"""You are an expert in cricket match analysis. Given the following match data,If User ask project score you should use {projected_score(match_type,runs,overs,Net_run_rate)} to give projected score:
{context}

Answer the following query concisely:
{query}
Answer:"""
    try:
        response = co.generate(
            model="command-xlarge-nightly",  
            prompt=prompt,
            max_tokens=150,
            temperature=0.5,
            stop_sequences=["\n"]
        )
        answer = response.generations[0].text.strip()
        return answer
    except Exception as e:
        return f"Error while querying Cohere: {e}"
import streamlit as st

def main():
    st.title("Cricket Match Query")
    
    want_live = st.radio("Want Live Match Details?", ("Yes", "No"))
    
    st.write("### Matches that are Live:")
    st.write(Live_Match_Names)
    
    st.write("### Matches that are not Live:")
    for match in Not_Live_Match_Names:
        st.write(match)
    
    user_query = st.text_input("Enter your cricket query:")
    
    if user_query:
        if want_live == 'Yes':
            answer = ask_cricket_query(user_query, scorecard)
        elif want_live == 'No':
            answer = ask_cricket_query(user_query, x)
        else:
            answer = "Please enter Yes or No."
        
        st.write("### LLM Answer:")
        st.write(answer)

if __name__ == "__main__":
    main()
