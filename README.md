Silver's Game Recommendation Engine

Project Lifecycle

Part A: Letter of Transmittal	2
Part B: Project Proposal Plan	4
Project Summary	4
Timeline	6
Evaluation Plan	9
Part C: Application	10
Part D: Post-implementation Report	11
Solution Summary	11
Data Summary	11
Machine Learning	11
Validation	12
Visualizations	13
User Guide	15
Reference Page	16


 
Part A: Letter of Transmittal 
August 26th, 2026
Mr. Jeremy Holt
Envirotech Studios
8793 Gray Clips Ln, New York City, NY, 43723
RE: Proposal For AI-Game Recommendation To Disrupt The Market
Dear Mr. Holt, 
I am writing today to present a proposal for a game recommendation platform that uses machine learning to serve customers.
Right now, the largest platform for discovering and buying games is Steam. Despite this, Steam has a barebones recommendation feature. The platform hosts over 100,000 games, and they can be difficult to parse beyond the few that bubble to the top. Consumers are always seeking fresh content, and Steam’s offerings run dry quickly, leaving them unsatisfied.
This is where our product comes in. It’s a machine-learning-powered game recommendation engine that lets consumers endlessly browse games like those they already play. This AI-powered personalized offering addresses the endless consumer need for fresh content, allowing them to easily navigate thousands of games based on their preferences.
By satisfying the consumer need for new content through a personalized, high-quality data product, our organization stands to gain cultural capital and a loyal customer base, which can be leveraged to increase sales of our other products. By becoming a high-trust brand, we gain resilience in the face of controversy and the flexibility to take risks and launch new offerings.
I have been working in brand management for various gaming-adjacent tech companies for 5 years. My experience gives me insight into this consumer base and makes me the perfect candidate to head a project like this. As the project develops, my experience will guide the team to remain on course towards gaming’s best recommendation engine.
This project also has minimal ethical risk, as it focuses on entertainment, and the data handled is never stored permanently. This policy and a content filter for younger consumers before the final release eliminates most of the ethical risk.
As for the scope of the project, we would start with two months of development on a prototype, with the only high cost being the developer's time away from other projects.
I hope we can meet to discuss this further.
Sincerely,
 Ahmer Syed
Ahmer Syed, Developer Branding Lead

 
Part B: Project Proposal Plan
Project Summary
Currently, consumers face limited options for finding new games. Steam, the industry leader, hosts hundreds of thousands of games, but its recommendation system leaves many things to be desired. It buries lesser-known games behind pages and pages of more popular games in a genre. This makes it hard for indie developers to be discovered and makes some games impossible to find for curious consumers. Beyond this, Steam uses a primarily one-size-fits-all approach, where everyone has the same genres to browse and the same top lists for the week.
More than anything, clients want something new. They want to find hidden gems. To each consumer, this hidden gem is something different. Steam’s lack of serious engagement with consumer preferences leaves this need unmet.
The app will use non-traditional search methods, such as similarity search and clustering, to enable consumers to engage with games they would otherwise never see on Steam's top pages. It will be an AI-powered game recommendation website that interfaces with the Steam API to determine customer preferences and tailor its output.
Our solution will include a clean, functional web app, the entire source code required to build it, a step-by-step user guide for running it, a dashboard with three distinct visualizations, and a final report documenting how development went. 
Addressing the content access problem through personalized, non-popularity-based means allows consumers to discover fresh content as they dig through thousands of games.
Data Summary
The primary source for our data is the FronkonGames Steam Games Dataset, which has 111,000 Steam games in JSON format. This includes various fields for each game. The one we will use for our search is the weighted tags field.

We will also collect data via the Steam API, including game banners and links to Steam Store pages. We will also use the Steam User Library API to get user account information for personalization.

The Steam Games database will be run through a Python script that creates a SQLite database from the JSON entries. An SQLite database will enable fast data retrieval as we handle customer queries.

This SQLite database will serve as input for the first layer of our machine learning methods. On this layer, we will turn each entry into a vector, ID pair. The vectors will be 300-dimensional coordinates that show the thematic ‘location’ of each game based on its tags.

These vectors will serve as input to our two ML methodologies. The vectors will be placed in a vector space using FAISS, and their distances will then be compared using the same technology. For our other method, we will use the same vectors to cluster them using scikit-learn’s k-means Clustering module.

This data cleaning pipeline will consist of a series of scripts that can be run sequentially to prepare the data for use by the application. If the data changes significantly or the implementation of any ML methodology changes, the scripts can be rerun in sequence.

The data goes from hard-to-quantify descriptors to a concrete coordinate of its thematic footprint. These coordinates can be easily scanned for anomalies (such as 37000 games in the dataset having empty tags) and further cleaned. When the empty-tagged games were discovered, they were excluded from the clustering process to maintain thematically rich clusters. Beyond that, in this numerical form, similarity search and clustering become possible, allowing for completely personalized recommendations.

The original dataset is CC-BY-4.0-licensed for public use, and the game data retrieved via Steam APIs is publicly available and not sensitive. User data from Steam is only retrieved after Authentication, and as a further precaution, no personal data is ever stored permanently.

Implementation
The industry-standard methodology we chose is CRISP-DM. Its steps of Business Understanding, Data Understanding, Data Preparation, Modeling, Evaluation, and Deployment fit our project perfectly.
The Business Understanding step was satisfied when we identified and articulated the problem of stale content recommendations and the industry's inability to solve it.
Data Understanding was gained by parsing the Steam Games Database, examining the anatomy of each game, and identifying which fields could be used for our purpose. The most useful one we identified was the tags field.
The Data Preparation involved converting the raw JSON entries into thematic vector coordinates in a high-dimensional vector space. It was now in a form usable by the ML methodologies. We used multiple vectorization methods until we could perfect the coordinates.
The Modeling occurred as we applied similarity search and clustering to the vector coordinates.
The Evaluation was done by displaying similarity scores for game recommendations, silhouette scores for different k values, and by plotting the shapes of the different clusters in the dataset. This allowed us to evaluate the performance of our algorithms both qualitatively and quantitatively. This step unveiled the data quality issue with the 37,000 untagged games. At this point, we refined Data Preparation and Modeling until the Evaluation results met our standards.
The Deployment occurred when we launched the fully functional app for hosting on the internet at silverrecs.com and delivered the local user guide for running the app on a personal machine.
Timeline

Milestone or deliverable	Project Dependencies	Resources	Start and End Date	Duration
Business Understanding- explore problem, define product, determine success parameters	NA	Developer/Project Lead	06/01/2026-06/05/2026	5 days
Data Understanding- determine primary dataset, explore data structure, identify key fields	Business Understanding Finished	Developer/Project Lead, FronkonGames Steam Games Dataset	06/06/2026-06/10/2026	5 days
Data Preparation-
Convert raw JSON to a SQLite database, use fastText model to vectorize the tags field with weights, store weighted vectors	Data Understanding Finished	Developer/Project Lead, Python/fastText, SQLite, numpy, and other libraries	06/11/2026-06/18/2026	8 days
Modeling-
Make FAISS vector space, populate the vector space with weighted tag vectors, using k-means; cluster weighted tag vectors	Data Preparation Finished	Developer/Project Lead	06/19/2026-06/25/2026	7 days
Evaluation-
Inspect cluster location and shape, perform silhouette scoring on k values, and inspect similarity scores for FAISS recommendations	Modeling Finished	Developer/Project Lead	06/26/2026-06/29/2026	4 days
Data Preparation/Modeling revision-
Improve data quality based on evaluation results, refine modeling methodologies	Evaluation Finished	Developer/Project Lead	06/30/2026-07/02/2026	3 days
API and frontend development	Revised Modeling Finished	Developer/Project Lead, FastAPI, Vue	07/03/2026-07/17/2026	15 days
Visualization Dashboard (3 chart types)	API and Frontend Finished	Developer/Project Lead	07/18/2026-07/21/2026	4 days
Deployment-
hosting, maintaining, and network debugging  	Dashboard Finished	Developer/Project Lead	07/22/2026-07/26/2026	5 days
Documentation-
make a user guide, make an end-of-project report	Deployment Complete	Developer/Project Lead	07/27/2026-07/31/2026	5 days

Evaluation Plan
Throughout development, a variety of verification methods were used. One was the use of test scripts to verify data integrity and correct data shaping throughout the pipeline. A script was used, for example, with sample data to verify the random entry point for clusters was operational. Another method was visual verification by running the app locally and identifying discrepancies in the dashboard or served results. A health check was added to the backend Dockerfile to verify that models had loaded successfully.
The validation method, upon completion of the project, was an evaluation using a combination of metrics, such as silhouette and similarity scores in the visuals, and a user test of the application's end-to-end usability as a recommendation engine.
Costs 
The itemized hardware and software cost is free. No special hardware beyond a personal computer is required to build the software. The free tier of any code editor can be used for the software.
The itemized estimated labor is 2 months of development. Assuming 40 hours a week, this is 320 hours of labor. The cost of an experienced developer's time can be estimated as $50 an hour. The labor cost comes to $16,000.
The application can be hosted on Cloudflare's free tier using a Pages application. A domain can be acquired for $10 for a 1-year license. A Digital Ocean droplet that can run the backend costs $6 per month for the required storage. The total environment cost is $16 upfront with recurring annual and monthly fees.
 
Part C: Application
Source code submitted in capstone_submission.zip
Application can be accessed via silverrecs.com or by following the user guide
 
Part D: Post-implementation Report
Solution Summary
Consumers of games were always looking for something new to play, but the industry lacked good, personalized recommendation solutions, leaving consumers dissatisfied. The solution was a personalized game recommendation platform that was endlessly explorable.
Our application solved this problem by using machine learning to personalize recommendations. The ML Methodologies we used also provided extensive exposure to obscure games.
Data Summary
The primary source of data was the FronKonGames Steam Games Dataset:
https://www.kaggle.com/datasets/fronkongames/steam-games-dataset
It was downloaded from Kaggle, then filtered through our data layers to become project usable.
Other data sources included the Steam Library and the User API. This data was collected via parametrized API queries.
Machine Learning
A pretrained machine learning model was used. It was a language model from the fastText family that converts sentences into high-dimensional vectors. It was ‘cc.en.300.bin’, a 300-dimensional English vector model.
The model: https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.bin.gz
This model’s output was used to train a k-means clustering model, which organized games into clusters. As an example, one cluster grouped Counter-Strike, Half-Life, Team Fortress Classic, and Day of Defeat, correctly identifying a shared theme of classic shooter games. The same pre-trained model was also used to build a vector coordinate grid for similarity searches. The library that performed the searches and built the grid was FAISS. The FAISS recommendations output games using a similarity-based nearest-neighbor algorithm. An example output from the FAISS similarity search was the recommendation of ‘BattleBit Remastered’ with a similarity score of 0.97 compared to the game in the query.
The models were built over several data preparation steps. First, the tags, along with their weights, were extracted from each game and fed to the fastText vectorization model. The vectorization accounted for the relative weight of each tag, then smoothed the weight magnitudes by taking the logarithm of each weight before averaging the vectors for each tag. This generated a single vector representing the weighted tags of the game. These vectors were placed into the FAISS vector index, which served as a space in which they could live in relation to each other. The vector space enabled similarity searches. The weighted tags were also used as input to the k-means model, though it further sanitized the data by excluding vectors that were all zeros, indicating no tags. This allowed clearer clusters to appear in the k-means analysis. The zero vectors weren’t excluded from the FAISS search to maintain discoverability of all games, even untagged ones.
This combination of similarity search and clustering was used because it aligned with the application's two purposes. First was personalization, which started with a similarity search for the user’s most-played games. The second was finding niche games, accomplished using a randomized entry point within a cluster.

Validation 
The k-means method was unsupervised, as there was no ground truth to supervise against.

This model was validated via two metrics. One was the Silhouette score, which measured the thematic cohesion of the clusters produced by the model. This score was measured across various k values and heavily influenced the data cleaning process. Originally, the validation revealed a peak Silhouette score of 0.34 at k=3, followed by a steep decline as k was increased. The early peak, the subpar score, and the steep decay motivated the team to reexamine data quality. This examination led to the inclusion of weights in the tag vectorization process; prior to this, tags were vectorized without accounting for their weights. After the data was refined, the silhouette scores were rerun, and this time they were much more promising. A peak of  0.51 at k=2 and a much flatter decay curve. There were also secondary peaks near the high 0.4 range, at k=4 and k=6, respectively. The data appeared validated by this metric, so it was passed to the second, more abstract metric. The second metric visualized the clusters' locations and shapes generated by the model. It accomplished this by using PCA flattening on the 300-dimensional vectors. It flattened them down to two-dimensional coordinates, which could be plotted on a scatter plot. Each cluster was plotted on its respective scatter plot and highlighted in a unique color to clarify its shape and location compared to the other clusters. This is where the second data quality issue was noted. Cluster 1, despite having 37,000 games, was almost entirely absent from the scatter plots. This validation method exposed the 37,000 zero vectors, which represented untagged games, that were skewing the silhouette scores from the start. After a second round of data sanitization, the silhouette scores were run again, and the scatter plots were regenerated. The silhouette scores had plummeted to a peak of 0.18 at k=6, but the decay curve was much flatter. Beyond this, the scatter plot showed strongly distinct clusters. A combination of flatter silhouette decay, promising scatter plots, and positive experience when manually testing the app earned this iteration of the dataset a passing grade. More data refinement opportunities were identified, but this was sufficient for the prototype.

The FAISS similarity search method was also unsupervised, as the meaning of similarity was not grounded in anything concrete beyond fastText model weights.

This model was validated via two metrics as well. The first was manual testing of the recommendation feature. Multiple iterations of this feature had nonsensical results. For example, an English first-person shooter would list a Japanese kids' game as its most similar game. In fact, all games would list the same five nonsensical games as their most similar games. In this iteration, the model was experiencing vector collapse, and the manual testing validation method revealed it. A combination of reworking how the ‘appids’ field is applied to the vector calculation and switching to a different vector comparison method (Cosine Similarity via Inner Product matching) fixed the vector collapse. The second validation metric stemmed from the new similarity calculation. Now that the vector distances were calculated using Cosine Inner Products, they ranged from 0.00 to 1.00. This range acted as a perfect measure of percent similarity. Tracking these similarity scores ensured that the recommendation implementation correctly applied nearest-neighbor to the vector space. This metric was used to generate the third, dynamic, visualization, the similarity score chart. Ultimately, when tags became weighted, the ‘appid’ field was dropped from the vector calculation entirely, since weighted tags meant no collisions and a unique identifier was no longer necessary for salting the vectors.
Visualizations
This chart can be found by clicking the ‘See Cluster Graphs’ button in the application.
 
This chart can also be found by clicking the ‘See Cluster Graphs’ button in the application.
 
The final chart is dynamically generated when a FAISS recommendation query is made. Navigate to the ‘recs’ page via the ‘Sign in through Steam’ or ‘Use Sample Account’ buttons. Then press ‘Get Recommendations’ on any of the gamecards. The Similarity Score Chart will appear at the top of the page.
 
User Guide
Include an enumerated (steps 1, 2, 3, etc.) guide to execute and use your application.  
	Include instructions for downloading and installing any necessary software or libraries. 
	Give an example of how the client should use the application. 
Prerequisites:
1.	Must have Docker installed and running on the machine. This can be accomplished by visiting docker.com. That installation process is outside the scope of this guide.
Steps for running the application locally:
1.	Unzip capstone_submission.zip into a folder on your machine
2.	Open PowerShell and navigate to that folder
3.	Run this command:
‘docker compose -f docker-compose.yml -f docker-compose.override.yml up --build -d’
(The containers may take some time to build)
4.	Once the containers are up and running, run this command:

‘docker compose exec backend python /app/data_scripts/write_vector_index.py’

(This may take a long time for the first run, but the console shows progression)
5.	Once that command finishes running, run this command:

‘docker compose exec backend python /app/data_scripts/write_faiss_index.py’

(This may take a long time for the first run, but the console shows progression)
Steps for Navigating to the User Interface:
1.	Open any browser (preferably Chrome)
2.	Navigate to the search bar and type ‘localhost’, then press Enter
(You should now be on the login page)
Options on the Login page:
1.	Use the “See Cluster Graphs” button to navigate to static visualizations
2.	Use the “Sign in through Steam” button to authenticate your personal Steam account and get personalized recommendations.
3.	Use the ‘Use Sample Account” button to get sample recommendations for testing.
Options on the Recommendations page:
1.	Use the “See Cluster Graphs” button to navigate to static visualizations
2.	Use the “Get Recommendations” button on any gamecard to get the FAISS recommendations. This will also generate the dynamic Similarity Search Chart
3.	Use the “View on Steam” button on any gamecard to be redirected to the Steam store page for that game.
4.	Use the “Explore More Games In This Cluster” button on any gamecard to be randomly served games from the matching cluster.
Options on the Cluster Graphs pages:
1.	Use the “Back To Recommendations” button to return to the previous page 
Example Run Through:
1.	Use the “Use Sample Account” button. This transports you to the recommendations page.
2.	Use the “Get Recommendations” button on the “Tom Clancy’s Rainbow Six Siege” gamecard. This will generate 5 recommendations for similar games, as well as a similarity score bar chart.
3.	Use the “View on Steam” button in the “MortarMen” gamecard. This will open a new tab showcasing the Steam Store page for that game.
4.	Close the Steam tab and use the “Explore More Games In This Cluster” button on the “MortarMen” gamecard. You will be served 5 random games from the same cluster as “MortarMen”.
Reference Page
	FronkonGames. (2025).Steam games dataset [Data set].Kaggle. https://www.kaggle.com/datasets/fronkongames/steam-games-dataset
	Facebook AI Research. (n.d.). Word vectors for 157 languages. fastText. Retrieved August 31, 2026, from https://dl.fbaipublicfiles.com/fasttext/vectors-crawl.html
