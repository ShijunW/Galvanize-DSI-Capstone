# Galvanize-DSI-Capstone
Capstone Project - Yelp Restaurants Recommender

[AWS EC2 Link](http://34.220.105.213:5000/) for the Restaurants Recommender.

### Some Screenshots

Starter page:
![](/Presentation/starter_page.png)

Input page:
![](/Presentation/input_page.png)

Recommender page:
![](/Presentation/recommender_page.png)


### Dataset and Yelp API

Yelp dataset is from Yelp Open Dataset (Round 12 Chanllenge, downloaded on 8/8/2018)

https://www.yelp.com/dataset

1. Focus on restaurants in Phoenix and users with 5 or more reviews on those restaurants.

Combined sub dataset

| Tables | user_id                | business_id            | categories           |
| ------:|-----------------------:| ----------------------:|---------------------:|
| count  | 189773                 | 189773                 | 189773               |
| unique | 15237                  |   3738                 | 2337                 |
| top    | d_TBs6J3twMy9GChqUEXkg | OgJ0KxwJcJ9R5bUK0ixCbg | Restaurants, Mexican |
| freq   | 486                    | 1008                   | 4356                 |



Find the most common words in categories

categories word cloud:
![](/Presentation/words_frequency.png)

2. For a given user, input a destination city, pull live Yelp restaurants data using Yelp API and do the recommendation to the user.

### AWS EC2 setup

[Here](/aws_app/) is the instruction.
