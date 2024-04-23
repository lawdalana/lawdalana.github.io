---
title : Loss vs Cost vs Objective function
notetype : feed
date : 22-04-2024
---

```
A loss function is a part of a cost function which is a type of an objective function.

All that being said, thse terms are far from strict, and depending on context, research group, background, can shift and be used in a different meaning. With the main (only?) common thing being "loss" and "cost" functions being something that want wants to minimise, and objective function being something one wants to optimise (which can be both maximisation or minimisation).

Cr.lejlot
```

- Loss function is usually a function defined on a data point, prediction and label, and measures the penalty

- Cost function is usually more general. It might be a sum of loss functions over your training set plus some model complexity penalty (regularization)

- Objective function is the most general term for any function that you optimize during training. For example, a probability of generating training set in maximum likelihood approach is a well defined objective function, but it is not a loss function nor cost function (however you could define an equivalent cost function)

Resource
https://stats.stackexchange.com/questions/179026/objective-function-cost-function-loss-function-are-they-the-same-thing