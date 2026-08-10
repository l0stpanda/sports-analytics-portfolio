# PROJECT AUDIT

## State Log (as of 9 August 2026):

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
