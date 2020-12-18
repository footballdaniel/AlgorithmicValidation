# Algorithmic classification

<!-- https://towardsdatascience.com/inter-rater-agreement-kappas-69cd8b91ff75 -->

<!-- http://john-uebersax.com/stat/agree.htm -->

## Procedure
I used the [online validation](https://share.streamlit.io/footballdaniel/algorithmicvalidation/main/validation.py) to compare the algorithmic classification against three manual raters. The comparison consists of 1595 frames that all raters clicked through.
I analyzed the percent viewing time and the inter-rater reliability (Kappa scores).
First, I performed a preliminary analysis where I included all AOI's. It turns out the algorithm is more conservative when the gaze is outsie of the human body. The algorithm judges more frames as `Other`, which leads to a low agreement.

In a second step, I excluded the `Other` category from the analysis and reached a more consistent rater agreement between the algorithm and the manual ratings (on average the manual raters agreed in 79.5% of the frames with the algorithm).


## All AOI

In the first plot you can see the AOI classification for all AOI's (inlucding `Other`!). The classification of the algorithm (left plot) is compared to the classification of the manual raters. 
As you can see, the algorithm has classified many more frames as `Other` (about 35%) when compared to the manual raters (about 15%).

![Classification for all AOI (including Other)](plots/RaterComparison.svg)


Why is it that the algorithm classified many more frames as `Other`? It is because the algorithmic classification is really strict when it comes to gaze points that lie outside of the human body (just one pixel away from the human gist is enough). To show this, I looked at all the frames where the algorithm judged `Other` and separately also at all the frames where any human rater judged `Other`

![Comparison of subset frames classified as Other](plots/RaterOtherSubset.svg)

On the left hand, you see that whenever the algorithm judged `Other`, the manual raters did still associate most of the frames to the body. This shows that the algorithm is too conservative and labels frames as `Other` too often.

On the right hand of the plot, I examine all the frames when any of the manual raters judged `Other` and plotted the algorithms judgement against it. Whenever the manual raters classified gaze as `Other`, then the algorithm did so too.

This is a systematic error that leads to a relatively low agreement between the algorithm and the manual raters.

I calculated two dependent variables. First, I calculate the `percent agreement`. This is comparing every manual rater against the algorithm for each frame. I also calculated the `percent agreement` among the manual raters to see for how many frames all manual labels were the same.
Second, I calculated the Cohens Kappa for the comparisons. To also get an idea about the agreement between all three raters, I used Krippendorff's Kappa.


| Comparison all AOI    |   Percent agreement [%] |   Reliability [Cohens Kappa] |
|-----------------------|-------------------------|------------------------------|
| Rater 1 vs. Algorithm |                   59.76 |                         0.39 |
| Rater 2 vs. Algorithm |                   47.73 |                         0.27 |
| Rater 3 vs. Algorithm |                   54.12 |                         0.33 |
| Rater 1 vs. Rater 2   |                   77.86 |                         0.67 |
| Rater 1 vs. Rater 3   |                   80.56 |                         0.70 |
| Rater 2 vs. Rater 3   |                   75.34 |                         0.64 |
| Among manual raters   |                   68.35 |                         0.63 (Krippendorff)|

When we look at all AOI, the agreement between the algorithm and the manual ratings is somewhere between fair and moderate. The agreement among the human raters is substantial.


## When gaze is on body (excluding Other)


| Comparison                  | Percent agreement | Reliability |
| --------------------------- | ----------------- | ----------- |
| Rater 1 vs. Algorithm       | 86.4%             | 0.70 Cohens Kappa |
| Rater 2 vs. Algorithm       | 71.7%             | 0.50 Cohens Kappa |
| Rater 3 vs. Algorithm       | 80.6%             | 0.61 Cohens Kappa |
| Average Rater vs. Algorithm | 79.5% | 0.61 Cohens Kappa (Krippendorff) |



## Gaze anchor at neck

I looked deeper into the estimations of the neck anchor. Generally, we have to be very careful not to over interpret this measure, because we **estimate** the gaze anchor by a **very rough 2D** approximation. Whenever the opponents arms and head were not in a 2D plane (this happens when they are very close), this results in a measurement error.

With this said, I still looked cautiously into the frequency distributions, but this time only looked at interpersonal distances < 1 m. The results are very similar to the numbers I already mentioned in the email.



![Frequency distribution when gaze is on Neck](results/Fdist_Neck.png)

The anchor is visible clearest when we look at interpersonal distances > 1 m. (For close distances, its just more noisy). You can see some outliers (values > 100 cm below head).

![Frequency distributions](results/Fdist.png)

When we look again at interpersonal distances > 1 m but now at all AOI's, gaze is on average roughly 30 cm down from the head.

Again, there is a bunch of measurement error in here. I think there is some general evidence that the gaze is on average about 22 cm (median) or 27 - 35 cm (mean) below the head.

If you want to be conservative, the median value (22.3 cm) makes most sense to me.

