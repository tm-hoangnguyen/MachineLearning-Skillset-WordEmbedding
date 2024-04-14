# MachineLearning-Skillset-WordEmbedding

The project focuses on analyzing the key skills needed for a specific job title. Using the OpenAI API 3.5 Turbo, the code extracts the top 8 skills from a dataset of 10,000 job descriptions. These skills are then vectorized using the Google-News-300 pre-trained Word2Vec model, which contains 300-dimensional vectors for 3 million words and phrases derived from about 100 billion words of data. Following vectorization, the skills are clustered and fine-tuned using the DBSCAN algorithm to identify patterns and relationships among the skills. This process helps in understanding the essential skill sets required for the targeted job title.

Source: [https://www.kaggle.com/datasets/arshkon/linkedin-job-postings](url).
