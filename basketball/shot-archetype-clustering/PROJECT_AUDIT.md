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
![Feature Profile by Cluster](image.png)

Why the two features matter: unassisted_fga_rate adds upon pct_assisted by making it a per-attempt stat, so it doesn't get confounded by make rate. shot_diversity uses a normalized Shannon entropy - 0 = a one-zone specialist, 1 is evenly spread. Tells a story of balance vs. one-trick.

I found unassisted_fga_rate to actually push itself to the very front of the 13 features with an F-score of 240.1 to a p-score of 3e-98. Shot_diversity is not far behind as a top-4 feature with 147.4 F-score and 2e-73 p-value. Important stuff!

