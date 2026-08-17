# PROJECT AUDIT

## VERSION 0: State Log (as of 9 August 2026):

### Features I'm Using
I'm currently using **15 standardized features**, split into four groups:
- Shot-location frequency: rim, paint, midrange, corner 3, above-the-break 3
- Zone efficiency: FG% in each of those five zones
- Shot-selection aggregates: three-point rate, rim-plus-three rate, midrange rate
- Shot creation: assisted-FG%, unassisted-FG%

There are a couple issues I've taken note of:

- Midrange frequency and midrange attempt rate are the same thing. One can be deleted for redundancy.
- The three-point attempt rate is mathematically derived from corner 3 and above-the-break 3 frequency numbers.
- In that same avenue, rim-plus-three rate can be mathematically derived from other numbers.
- Not sure if this is a major issue, but you can derive assisted-FG% from unassisted-FG% and vice-versa. I could eliminate one of these features to reduce redundancy.
- Zone-level FG% can be noisy even after filtering the players down to 200 total shot attempts.

### How I'm currently clustering:
The primary model is K-means with k=5, using the aforementioned features and random_state=42. The dataset contains 350 players after filtering out all players who took under 200 shot attempts for the season.

The notebook also fits two other models (Gaussian Mixture and Agglomeritave Clustering), but this is mainly for future work regarding robustness comparison.

The intended archetypes are:

- Balanced Wing
- Midrange Scorer
- 3-and-D
- Rim Runner
- Shot Creator

I started with five clusters just as a baseline, but domain intuition won't be enough. The next step is stability and validation across k.

### Validation
I currently have two quantitative metrics:

- Silhouette: 0.135
- Davies-Bouldin: 1.770

I also have PCA visualization and cluster-profile analysis through a feature heatmap. It's recommended to manually check players against their clusters and see if they fit the proper description (spoiler: couple mismatches, most notably Curry listed as a balanced wing).

Perhaps the most major issue with a project like this is that there is no ground-truth dataset for me to validate with. A lot of this validation ends up being subjective.

It is thus important for me to not only improve the clustering but also the validation and archetype-labeling. Players like Alex Caruso get labeled as a "rim-runner" despite very clearly being not that. There might be value in weighting more heavily towards the attempt heatmap. Caruso's weak 3FG% this past season could be a source of his given label.

### Exporting
The notebook exports a JSON that contains all of the features, as well as the names, IDs, and archetypes for each player in the cleaned dataset. My website (https://ibisboard.vercel.app/sports/offensive-profiles) then reads this and prints out the data in a readable, searchable manner.

### Pipeline
The pipeline is thus: 
1. NBA API
2. Python/Notebook
3. CSV Cache
4. Feature Engineering
5. Clustering
6. JSON
7. Website

## 3 Week Plan

### Feature Engineering

- Remove redundant features
- Reevaluate the 200 FGA bar.
- Investigate the treatment of low-efficiency zones.
- Add more context (investigate NBA API documentation for this) such as dribbling, touch time, etc.
- Document why for each of the final features.

### Validation

- Evaluate more values of k.
- In doing so, compare the metrics being used to evaluate the model.
- Use different random_state seeds.
- Compare K-Means versus GMM and hierarchical clustering.
- Manually create a new, smaller dataset of players with set-in-stone archetypes to compare against.
- IMPORTANT: cluster quality vs. basketball usefulness.

### Documentation

- Document the entire data pipeline.
- Record the final features as well as their rationale.
- Record the parameters and evaluation metrics with each export.

### Further Plans

I want to move this from just a notebook to a more repeatable pipeline, especially modular if possible in order to get more years and better outputs. Below are some of my thoughts:

- Extending this work to years past (and the can of worms that opens)
- Storing the model's metadata alongside the player output.
- Handling players changing teams
- Ensuring the output schema stays the same for frontend stability throughout modeling process changes
- Scaling to career-level archetypes

### Metrics
Silhouette score: 0.130
Davies-Bouldin index: 1.834

Important graphs can be found in the version folders (v0, v1, etc.). The ones I'm honing in on are elbow, silhouette, feature value heatmap, and PCA. 

## VERSION 1: Feature Engineering

### Are these features linearly separable?

No, since that isn't a requirement for an unsupervised clustering model. I need to focus on whether the features form meaningful regions in feature space. I also need to figure out whether transformations or redundant features are distoring Euclidean distance.

### Changelog and Analysis

Removed redundant features:

- three_point_rate
- rim_plus_three_rate
- midrange_rate
- pct_unassisted

Added three new features:

- shot_diversity: calculated with Shannon Entropy. Does this player specialize heavily in one type of shot, or do they distribute their offense across many areas?
- efg_pct: effective field goal percentage. Think of it as an overall fg% across all the zones.
- unassisted_fga_rate: manually calculated now.

### Metrics

ALL THREE NEW FEATURES
Silhouette score: 0.121 
Davies-Bouldin index: 1.986

SHOT DIVERSITY ONLY
Silhouette score: 0.124
Davies-Bouldin index: 1.850

EFG PCT ONLY
Silhouette score: 0.124
Davies-Bouldin index: 1.785

UNASSISTED FGA RATE ONLY
Silhouette score: 0.129
Davies-Bouldin index: 1.802

SHOT DIVERSITY + EFG PCT
Silhouette score: 0.119
Davies-Bouldin index: 1.947

SHOT DIVERSITY + UNASSISTED FGA RATE
Silhouette score: 0.126
Davies-Bouldin index: 1.781

EFG PCT + UNASSISTED FGA RATE
Silhouette score: 0.116
Davies-Bouldin index: 1.814

After analyzing these metrics and the graphs given by analyzing the new features, I decided to delete efg.
New feature metrics:
![Feature Correlation Matrix](v1/v1-feature-corr-matrix.png)
![Feature Distributions](v1/v1-feature-distributions.png)
![Feature Boxplot](v1/v1-feature-boxplot.png)
![Feature Profile by Cluster](v1/v1-feature-profiles.png)

Why the two features matter: unassisted_fga_rate adds upon pct_assisted by making it a per-attempt stat, so it doesn't get confounded by make rate. shot_diversity uses a normalized Shannon entropy - 0 = a one-zone specialist, 1 is evenly spread. Tells a story of balance vs. one-trick.

I found unassisted_fga_rate to actually push itself to the very front of the 13 features with an F-score of 240.1 to a p-score of 3e-98. Shot_diversity is not far behind as a top-4 feature with 147.4 F-score and 2e-73 p-value. Important stuff!

Silhouette score: 0.126
Davies-Bouldin index: 1.781

## VERSION 2: Clustering Tweaks

### What I'm Doing

Tweaking my cluster count both due to domain knowledge and the 2nd cluster having a large imbalance of players (109 to an average about 60 players for the other four clusters). I think I might cap out at 8 or 9 to avoid overfitting. Lowering it is probably not helpful, but I am curious.

### Analysis

I got pretty much what I expected out of the testing by testing k = 2-8, with a noticeable boost in the third cluster (can be ignored) and a big red sign screaming "LOOK AT SIX AND SEVEN!"

I graphed their differences in both silhouette and Davies-Bouldin, can be found in the notebook, probably, and saved in the v2 folder.

Next, I looked a bit closer at the metrics for k=6 and k=7.

**K = 6:**

=== K=6 Inspection ===
Cluster sizes:
cluster_k6
0      5
1     83
2     52
3     55
4    118
5     37
Name: count, dtype: int64

Cluster profiles:
            pct_fga_rim  pct_fga_paint_non_ra  pct_fga_midrange  \
cluster_k6                                                        
0                 0.656                 0.240             0.072   
1                 0.247                 0.254             0.159   
2                 0.374                 0.136             0.036   
3                 0.170                 0.098             0.058   
4                 0.246                 0.198             0.094   
5                 0.637                 0.251             0.035   

            pct_fga_corner3  pct_fga_above_break3  fgpct_rim  \
cluster_k6                                                     
0                     0.003                 0.029      0.691   
1                     0.057                 0.283      0.657   
2                     0.202                 0.251      0.657   
3                     0.211                 0.463      0.653   
4                     0.115                 0.347      0.643   
5                     0.024                 0.052      0.719   

            fgpct_paint_non_ra  fgpct_midrange  fgpct_corner3  \
cluster_k6                                                      
0                        0.431           0.310          1.000   
1                        0.456           0.414          0.383   
2                        0.344           0.272          0.346   
3                        0.417           0.422          0.412   
4                        0.437           0.406          0.400   
5                        0.478           0.380          0.253   

            fgpct_above_break3  pct_assisted  shot_diversity  \
cluster_k6                                                     
0                        0.188         0.601           0.527   
1                        0.336         0.451           0.888   
2                        0.316         0.736           0.849   
3                        0.363         0.848           0.817   
4                        0.346         0.680           0.893   
5                        0.274         0.680           0.552   

            unassisted_fga_rate  
cluster_k6                       
0                         0.240  
1                         0.256  
2                         0.120  
3                         0.066  
4                         0.143  
5                         0.193  

Sample players per cluster:
  Cluster 0 (n=5): ['Clint Capela', 'Giannis Antetokounmpo', 'Jonas Valanciunas', 'Mark Williams']
  Cluster 1 (n=83): ['Ajay Mitchell', 'Alperen Sengun', 'Andrew Nembhard', 'Anfernee Simons']
  Cluster 2 (n=52): ['Andre Drummond', 'Ben Saraf', 'Bilal Coulibaly', 'Bruce Brown']
  Cluster 3 (n=55): ['AJ Green', 'Aaron Nesmith', 'Al Horford', 'Alex Caruso']
  Cluster 4 (n=118): ['Aaron Gordon', 'Aaron Holiday', 'Aaron Wiggins', 'Ace Bailey']
  Cluster 5 (n=37): ['Adem Bona', 'Amen Thompson', 'Anthony Gill', 'Ausar Thompson']

**K = 7:**

=== K=7 Inspection ===
Cluster sizes:
cluster_k7
0    67
1    71
2    45
3    17
4    69
5    17
6    64
Name: count, dtype: int64

Cluster profiles:
            pct_fga_rim  pct_fga_paint_non_ra  pct_fga_midrange  \
cluster_k7                                                        
0                 0.187                 0.109             0.057   
1                 0.250                 0.257             0.161   
2                 0.391                 0.135             0.035   
3                 0.707                 0.229             0.039   
4                 0.199                 0.177             0.114   
5                 0.637                 0.269             0.035   
6                 0.324                 0.237             0.078   

            pct_fga_corner3  pct_fga_above_break3  fgpct_rim  \
cluster_k7                                                     
0                     0.204                 0.443      0.655   
1                     0.052                 0.279      0.661   
2                     0.200                 0.239      0.662   
3                     0.008                 0.017      0.717   
4                     0.110                 0.400      0.598   
5                     0.021                 0.038      0.710   
6                     0.107                 0.254      0.694   

            fgpct_paint_non_ra  fgpct_midrange  fgpct_corner3  \
cluster_k7                                                      
0                        0.418           0.409          0.418   
1                        0.463           0.416          0.380   
2                        0.339           0.268          0.336   
3                        0.496           0.401          0.565   
4                        0.401           0.431          0.406   
5                        0.456           0.307          0.158   
6                        0.469           0.382          0.368   

            fgpct_above_break3  pct_assisted  shot_diversity  \
cluster_k7                                                     
0                        0.363         0.839           0.829   
1                        0.337         0.439           0.884   
2                        0.314         0.729           0.841   
3                        0.370         0.659           0.447   
4                        0.347         0.616           0.890   
5                        0.122         0.667           0.558   
6                        0.335         0.710           0.884   

            unassisted_fga_rate  
cluster_k7                       
0                         0.071  
1                         0.264  
2                         0.123  
3                         0.216  
4                         0.162  
5                         0.197  
6                         0.143  

Sample players per cluster:
  Cluster 0 (n=67): ['AJ Green', 'Aaron Holiday', 'Aaron Nesmith', 'Al Horford']
  Cluster 1 (n=71): ['Ajay Mitchell', 'Alperen Sengun', 'Andrew Nembhard', 'Anfernee Simons']
  Cluster 2 (n=45): ['Andre Drummond', 'Ben Saraf', 'Bilal Coulibaly', 'Bruce Brown']
  Cluster 3 (n=17): ['Adem Bona', 'Clint Capela', 'Daniel Gafford', 'Deandre Ayton']
  Cluster 4 (n=69): ['Aaron Wiggins', 'Andrew Wiggins', 'Ayo Dosunmu', 'Bennedict Mathurin']
  Cluster 5 (n=17): ['Amen Thompson', 'Ausar Thompson', "Day'Ron Sharpe", 'Domantas Sabonis']
  Cluster 6 (n=64): ['Aaron Gordon', 'Ace Bailey', 'Alex Sarr', 'Anthony Black']

The biggest backbreaker here, alongside its obviously worse metrics, is K=6's cluster with 5 players. So I've settled on 7. It performs slightly worse than K=5, but we will have to make that sacrifice for wider breadth.

### Archetype Naming
K=7 identifies seven distinct, basketball-meaningful archetypes:

1. **Three-Point Role Players (n=67):** Low-volume perimeter specialists, high assists
   - Example: AJ Green, Aaron Nesmith, Al Horford
   - Profile: 64.7% from 3pt range, 83.9% assisted makes

2. **Two-Level Scorers (n=71):** Balanced scorers with high shot diversity
   - Example: Alperen Sengun, Anfernee Simons
   - Profile: Shot diversity 0.884, mid-range on most dimensions

3. **Corner Specialists (n=45):** Role players, corner-oriented, mid-post
   - Example: Andre Drummond, Bruce Brown
   - Profile: 39.1% rim, 20% corner-3, 72.9% assisted

4. **Elite Post Scorers (n=17):** High-volume finishers, efficient from restricted area
   - Example: Clint Capela, Domantas Sabonis, DeAaron Ayton
   - Profile: 70.7% rim, nearly 0% 3pt volume, efficient (72% rim FG%)

5. **Playmaking Wings (n=69):** Primary creators, balanced outside game
   - Example: Aaron Wiggins, Andrew Wiggins
   - Profile: 40% above-break 3s, 0.890 shot diversity, mid assists

6. **Rim Runners (n=17):** Finishers with limited outside game
   - Example: Amen Thompson, Ausar Thompson, Day'Ron Sharpe
   - Profile: 63.7% rim, <6% 3pt, limited ball-handling

7. **Three-Level Scorers (n=64):** Mid-range oriented, mixed scoring
   - Example: Aaron Gordon, Anthony Black
   - Profile: 32.4% rim, 23.7% paint, 25.4% above-break 3s



