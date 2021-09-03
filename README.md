# Predicting Youth Risk Behaviors: Modeling the YRBSS <br>
Becky Peters, Data Scientist<br>
github.com/beckyepeters<br>
linkedin.com/beckyepeters<br>
becky.e.peters@gmail.com<br>

### Background and Motivation 
I will use the analogy of jellyfish in the ocean to describe risky behaviors in one's youth. Part of my job as a mom (or a doctor's job with their pediatric patients, or a teacher's / counselor's job with their students) is to partner with youth to help them make choices as they develop throughout their lives. Youth deserve accurate information about the consequences of their behaviors, as well as about the possibility of these choices arising in their lives. Of course, there are so many things to navigate as you develop into adulthood; we can't throw all the jellyfish at them at once and expect them to make good decisions. We have to help them navigate the water by talking about risk and helping them make informed and appropriate decisions about their lives and discuss with them how it may impact their future. 

The [Centers for Disease Control and Prevention](https://www.cdc.gov/) (CDC) supports us with this information through their Youth Risk Behavior Survey, a biannual survey conducted across the nation since 1999. The YRBS (conducted by the CDC, state, territorial, and local education and health agencies and tribal governments) surveys youth from across the country about health-related behaviors that contribute to leading causes of death and disability among youth and adults, including (listed from [the YRBSS website](https://www.cdc.gov/healthyyouth/data/yrbs/index.htm)): 
* Behaviors that contribute to unintentional injuries and violence
* Sexual behaviors related to unintended pregnancy and sexually transmitted diseases 
* Alcohol and other drug use
* Tobacco use
* Unhealthy dietary behaviors
* Inadequate physical activity

Purpose of the Project / Model: 
* To provide individually-based predictions of probability to professional end-users (health care providers, schools, counselors, etc) that will support them with: 
    * engaging in individual discussions with the youth in their care, and
    * making programming decisions to maximize outreach efforts.
* To improve upon the baseline accuracy of 'x% of people your age or gender or race engaged in this activity' as available now through the comprehensive [YRBSS online dashboard](https://yrbs-explorer.services.cdc.gov/#/)
* To better understand the world in which my kids are growing up. 

Ethical and Moral Considerations: 
1. Insights over Answers: 
    * Certainly a high probability of a person engaging in an activity does not mean that person has.
2. Discussions over Discipline:  
    * The hope is that adult knowledge of the prevalence of these risk behaviors will lead to more appropriate, relevant conversations with young pepole about their own health. 
3. Reality over Determinism: 
    * Even if the model were 100% accurate, actual choices are impossible to predict for individual people.  

### Data Sources and Primary Resources for Project
* Data Resources: 
    * [YRBSS Publicly Available Datasets](https://www.cdc.gov/healthyyouth/data/yrbs/data.htm) 
    * This project used the 'National YRBS Datasets and Documentation' (grey section), then accessed the 2019 Data (downloaded the [Access Database file](https://www.cdc.gov/healthyyouth/data/yrbs/files/2019/XXH2019_YRBS_Data.zip) and exported tables to python using [mdbtools](https://github.com/mdbtools/mdbtools))
    * [User's Guide for the 2019 YRBS National, State, and District Combined Datasets](https://www.cdc.gov/healthyyouth/data/yrbs/pdf/2019/2019_YRBS_SADC_Documentation.pdf)
* Coding Resources: 
    * [MDB Tools on GitHub](https://github.com/mdbtools/mdbtools)



### Other Citations and References 
* [Let's Talk About Sex, Maybe](https://www.coloradohealthinstitute.org/research/lets-talk-about-sex-maybe); Colorado Health Institute, accessed Aug 2021