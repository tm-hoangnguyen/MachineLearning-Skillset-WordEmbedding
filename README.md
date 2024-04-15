# MachineLearning-Skillset-WordEmbedding

The project focuses on analyzing key skills needed for a specific job title. Using the OpenAI API 3.5 Turbo, the code extracts top skills from a dataset of 10,000 job descriptions. These skills are vectorized using Google-News-300 pre-trained Word2Vec model, which contains 300-dimensional vectors for 3M words and phrases derived from about 100B words of data. Following vectorization, the skills are clustered and fine-tuned using the DBSCAN to identify patterns among the skills.

Source: [https://www.kaggle.com/datasets/arshkon/linkedin-job-postings](url).

## Data Manipulation
This folder includes scripts to connect to RDS instance and utilize OpenAI API to extract key job skills from "description" column. For each job description, there will be a corresponding list of key skills.

GPT model: **GPT-3.5 Turbo**.

### Usage

1. Set up the `OPENAI_API_KEY` as a secret key or environment variable.

2. Specify a clear job description within the `"content"` field of the `messages` variable in `openai_script.py`.

3. Run the `openai_script.py` script to connect to the RDS instance and extract key job skills from the job descriptions.

For more information on how to calculate tokens and pricing for the GPT-3.5 Turbo model, refer to the [OpenAI Pricing](https://openai.com/pricing) page.

## Clustering
This folder loads Word2Vec pre-trained model and implements DBSCAN clustering with parameters to optimally reduce noise data points

In addition, it includes two graphs to identify the best epsilon and dimensions for each skill vector.

Tableau Public Visualization: [https://public.tableau.com/authoring/SkillNetwork_View_HoangN_6242/Dashboard1#1](url)
