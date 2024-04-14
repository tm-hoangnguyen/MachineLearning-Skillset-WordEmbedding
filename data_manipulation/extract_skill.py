import pymysql
import os
import pandas as pd
import ast
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Access environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI()

def jd_skillset_extraction(job_description):
    if not job_description:
        return ValueError("Job description is empty.")

    response = client.chat.completions.create(
        # temperature is used to control the randomness of the output
        temperature=0.5,
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": '''
                        Your task is to identify and extract technical skillsets from provided job description.
                        Please list all the skillset you find, ensuring accuracy and completeness.
                        Focus solely on extracting technical skillset without providing additional analysis or commentary.
                        Return exactly top 8 skillset if more than 8 are found.
                        Return format: [tag1, tag2]
                        '''
            },
            {
                "role": "user",
                "content": job_description
            }
        ]
    )
    output = response.choices[0].message.content # this is currently list representation of string
    
    # convert output to list type
    output = output.strip('[').strip(']').split(',')
    output = [keyword.strip().strip("'") for keyword in output]
    # print(type(output))
    return output


    ### Test ###
    # jd1 = '''
    # About The Team

    # Workvivo is a digital experience platform that brings workplace culture to life and empowers employees to be heard and feel included, no matter where they work. We are committed to our customers, obsessed with improving employees’ working lives, and driven by results. From automotive, technology, manufacturing, logistics, finance, and everything in between, we roll out the Workvivo platform to diverse organizations across the globe to enhance their employee experience.

    # What We’re Looking For

    # Have 0 to 12 months experience with SaaS sales space in Business Development
    # Be able to manage a large number of accounts and work cohesively with AE's
    # Experience communicating with C-Level by phone and email
    # Be empathic and have positive energy
    # Be comfortable with process and ambiguity. We are still growing and learning as a company.
    # Experience in picking up and explaining ideas and processes to business decision-makers and champions
    # Be knowledgable in tools of the trade i.e. Hubspot, Zoominfo, LinkedIn, and Outreach
    # Immigration sponsorship is not available for this position. You must be legally authorized to work in the United States**
    # '''

    # print(jd_skillset_extraction(jd1))

def extract_skills_from_jd(df):
    # Extract skills from job description using the function jd_skillset_extraction
    df['skill'] = df['description'].apply(lambda x: jd_skillset_extraction(x))
    df = df[['job_id', 'skill']]
    # Convert the skills column to a list
    df['skill'] = df['skill'].apply(lambda x: x if isinstance(x, list) else ast.literal_eval(x))

    # Split each skill within skills list into a separate row
    result = df.explode('skill').reset_index(drop=True)
    
    return result

def main():
    # Set environment variable to enable cleartext plugin if needed
    os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

    # Access environment variables for database connection
    endpoint = os.environ.get('DB_ENDPOINT')
    port = os.environ.get('DB_PORT')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    database = os.environ.get('DB_DATABASE')

    try:
        # Establish connection to the database
        conn = pymysql.connect(host=endpoint, port=int(port), user=user, passwd=password, db=database)
        # Create a cursor object
        cursor = conn.cursor()
        # Query
        query = '''
            select
                job_id
                , description
            from job_postings
            limit 10000;
            '''
        # Execute the query
        cursor.execute(query)
        # Fetch and print the result
        result = cursor.fetchall()

        # Convert the result to a pandas DataFrame
        df = pd.DataFrame(result, columns=['job_id', 'description'])
        # Close cursor and connection
        cursor.close()
        conn.close()

        # Extract skills from job descriptions
        df = extract_skills_from_jd(df)

        # Print result
        # print(df)

        # Write DataFrame to CSV file
        # df.to_csv('job_postings_skills_output_9002_10000.csv', index=False)

    except Exception as e:
        print("Database connection failed due to:", e)

if __name__ == "__main__":
    main()
