---
title : Metrics for Search System (Information retrieval)
notetype : feed
date : 23-04-2024
---

## Why we should measure these search metrics?
Evaluation these metrics helps us to assess how well the search results satisfied the user's query intent, some metrics will be a clue about issue on the search systems and which optimize technique are effective in our application.

## Example metric of the search systems
### Online Metrics
#### 1. Session abandonment rate
Session abandonment rate is a ratio of search sessions which do not result in a click.
```
non-click / Number of search
```

#### 2. Click-through rate
The ratio of users who click on a specific link to the number of total users who view a page
```
click / Number of search
```

#### 3. Session success rate
Session success rate measures the ratio of user sessions that lead to a success. Defining "success" is often dependent on context, but for search a successful result is often measured using dwell time as a primary factor along with secondary user interaction, for instance, the user copying the result URL is considered a successful result, as is copy/pasting from the snippet.
```
Dwell time = The duration time between click result and return/left the result

User has the interaction after click the result (Search → Click → Play with the same CMS_ID for VOD)
```

##### 3.1 Dwell time
Dwell time is the duration between when a user clicks on a search engine result, and when the user returns from that result, or is otherwise seen to have left the result. It is a relevance indicator of the search result correctly satisfying the intent of the user. Short dwell times indicate the user's query intent was not satisfied by viewing the result. Long dwell times indicate the user's query intent was satisfied. Google has used dwell time in page ranking.

#### 4. Zero result rate
Zero result rate (ZRR) is the ratio of Search Engine Results Pages (SERPs) which returned with zero results. The metric either indicates a recall issue, or that the information being searched for is not in the index.


#### 5.Queries per time / Average queries latency
Measuring how many queries are performed on the search system per (month/day/hour/minute/sec) tracks the utilization of the search system. It can be used for diagnostics to indicate an unexpected spike in queries, or simply as a baseline when comparing with other metrics, like query latency. For example, a spike in query traffic, may be used to explain a spike in query latency.

#### 5.Top queries list
Top queries is noting the most common queries over a fixed amount of time. The top queries list assists in knowing the style of queries entered by users.

----

### Offline Metrics (Binary Relevance [Order-Unaware Metrics])
#### 1. Precision@k
This metric quantifies how many items in the top-K results were relevant.

![Precision](/assets/img/Metrix/precision.png)

#### 2. Recall@k
This metric gives how many actual relevant results were shown out of all actual relevant results for the query.

![Recall](/assets/img/Metrix/recall.png)

#### 3. F1@K
This is a combined metric that incorporates both Precision@k and Recall@k by taking their harmonic mean.

![F1](/assets/img/Metrix/f1.png)

---

### Offline Metrics (Binary Relevance [Order Aware Metrics])

#### 1. [[Mean Reciprocal Rank (MRR)]]
This metric is useful when we want our system to return the best relevant item and want that item to be at a higher position.

![MRR](/assets/img/Metrix/MRR.png)


#### 2. Average Precision(AP)
Average Precision is a metric that evaluates whether all of the ground-truth relevant items selected by the model are ranked higher or not. Unlike MRR, it considers all the relevant items.
- rel(k)rel(k) is an indicator function which is 1 when the item at rank K is relevant.
- P(k)P(k) is the Precision@k metric
![AP](/assets/img/Metrix/AP.png)


#### 3. Mean Average Precision(MAP)
If we want to evaluate average precision across multiple queries, we can use the MAP. It is simply the mean of the average precision for all queries.

![MAP](/assets/img/Metrix/MAP.png)

---

### Graded Relevance
We have a ranking model that gives us back 5-most relevant results for a certain query. The first item had a relevance score of 3 as per our ground-truth annotation, the second item has a relevance score of 2 and so on.

![Graded Relevance](/assets/img/Metrix/grade_relevance.png)

#### 1. Cumulative Gain (CG@k)
This metric uses a simple idea to just sum up the relevance scores for top-K items. The total score is called cumulative gain.

![CG](/assets/img/Metrix/CG.png)

`Problem: CG doesn’t take into account the order of the relevant items. So, even if we swap a less-relevant item to the first position, the CG@2 will be the same.`

![CG](/assets/img/Metrix/CG2.png)


#### 2. Discounted Cumulative Gain (DCG@k)
The simple cumulative gain doesn’t take into account the position. But, we would normally want items with a high relevance score to be present at a better rank.

![DCG](/assets/img/Metrix/DCG.png)

Using this penalty, we can now calculate the discounted cumulative gain simply by taking the sum of the relevance score normalized by the penalty.

![DCG](/assets/img/Metrix/DCG2.png)

##### Example

![Example DCG](/assets/img/Metrix/DCG3.png)

There is also an alternative formulation for DCG@K that gives more penalty if relevant items are ranked lower. `This formulation is preferred more in industry.`

![DCG Formula](/assets/img/Metrix/DCG4.png)

While DCG solves the issues with cumulative gain, it has a limitation. Suppose we a query Q1 with 3 results and query Q2 with 5 results. Then the query with 5 results Q2 will have a larger overall DCG score. But we can’t say that query 2 was better than query 1.

![Example DCG](/assets/img/Metrix/DCG5.png)

#### 3. Normalized Discounted Cumulative Gain (NDCG@k)
To allow a comparison of DCG across queries, we can use NDCG that normalizes the DCG values using the ideal order of the relevant items.

![NDCG](/assets/img/Metrix/NDCG.png)

##### Example

###### Actual Relevance
![NDCG Actual Relevance](/assets/img/Metrix/NDCG2.png)

###### Ideally Relevance
we would have wanted the items to be sorted in descending order of relevance scores.

![NDCG Ideally Relevance](/assets/img/Metrix/NDCG3.png)

###### Result
![NDCG Ideally Relevance](/assets/img/Metrix/NDCG4.png)

---

## Summary of metrics

Type|Metrics|Description
:---:|---|---
Online|Session abandonment rate| Session abandonment rate is a ratio of search sessions which do not result in a click. `Number of Non-click / Number of search`
Online|Click-through rate| The ratio of users who click on a specific link to the number of total users who view a page `Number of Click / Number of search`
Online|Session success rate| The ratio of user sessions that lead to a success. Success = More Dwell time `Dwell time = The duration time between click result and return/left the result`, user interaction `User has the interaction after click the result`
Online|Zero result rate| The ratio of Search Engine Results Pages (SERPs) which returned with zero results. It’s recall issue or information is not index. `Number of empty result / Number of search`
Online|Queries per time| The utilization of the search system. It can be used for diagnostics to indicate an unexpected spike in queries, or simply as a baseline when comparing with other metrics, like query latency. `Number of query / Time (month/day/hour/minute/sec)`
Online|Average queries latency| The utilization of the search system. It can be used for diagnostics to indicate an unexpected spike in queries, or simply as a baseline when comparing with other metrics, like query latency. `Sum of queries latency / Number of query`
Online|Top queries list (trending)| Top queries is the most common queries over a fixed amount of time. `Top k queries order by number of search in period of time`
Offline Binary Relevance|[Order-Unaware Metrics] Precision@k| This metric quantifies how many items in the top-K results were relevant.
Offline Binary Relevance|[Order-Unaware Metrics] Recall@k| This metric gives how many actual relevant results were shown out of all actual relevant results for the query.
Offline Binary Relevance|[Order-Unaware Metrics] F1@k| This is a combined metric that incorporates both Precision@k and Recall@k by taking their harmonic mean.
Offline Binary Relevance|[Order Aware Metrics] Mean Reciprocal Rank(MRR)| This metric is useful when we want our system to return the best relevant item and want that item to be at a higher position.
Offline Binary Relevance|[Order Aware Metrics] Average Precision(AP)| Average Precision is a metric that evaluates whether all of the ground-truth relevant items selected by the model are ranked higher or not. Unlike MRR, it considers all the relevant items.
Offline Binary Relevance|[Order Aware Metrics] Mean Average Precision(MAP)| If we want to evaluate average precision across multiple queries, we can use the MAP. It is simply the mean of the average precision for all queries.
Offline Graded Relevance|Cumulative Gain (CG@k)| This metric uses a simple idea to just sum up the relevance scores for top-K items. The total score is called cumulative gain.
Offline Graded Relevance|Discounted Cumulative Gain (DCG@k)| The simple cumulative gain doesn’t take into account the position. But, we would normally want items with a high relevance score to be present at a better rank. There is also an alternative formulation for DCG@K that gives more penalty if relevant items are ranked lower. This formulation is preferred more in industry.
Offline Graded Relevance|Normalized Discounted Cumulative Gain (NDCG@k)| NDCG that normalizes the DCG values using the ideal order of the relevant items.


--- 

Resource
- https://en.wikipedia.org/wiki/Evaluation_measures_(information_retrieval)
- https://en.wikipedia.org/wiki/Dwell_time_(information_retrieval)
- https://nlp.stanford.edu/IR-book/pdf/08eval.pdf
- https://amitness.com/2020/08/information-retrieval-evaluation/
- https://seranking.com/blog/pagerank
- https://truedmp.atlassian.net/wiki/spaces/AI/pages/5002790082/Explore+Metrics+about+Search+System+Information+retrieval
