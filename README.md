# bet-helper-lite

## Database system
- PostgreSQL
- Hibernate to integrate with Java and see some shit
- Mybatis to better understand how to write SQL

## Data saved to DB
- Each change in score: game name (basketball, football etc), team a, team b, score a, score b, quarter, coefficient, datetime
- possible tables:
1. game - saves finish result: game id, game name, start time, team a, team b, end time, result score
2. coefficient_state - saves data about coefficient after each change in score: coeff state id, game id, score state id, team, datetime, coeff1, coeff2...
3. score_state - saves data about each change in score: score state id, game id, datetime, team a, team b, score a, score b

## Data saved as logs
- Each change in state
- log file name contains datetime start, game name, teams
- first row defines which team is home and away
- each row contains time, home-coeff-1, away-b-coeff-1..., score

## Application 1 - scraper + calculator
- scraper written in Python
- data from three bet websites is being sent to application for analyze
- before calculation data is displayed as table: coefficients as columns and bet websites as rows
- when data changes show visually - cell with coeff number changes color to green when increases, red when decreases
- count average according to coefficient steps and display it later

- !according to some situations employee must close trading - sound and notification should be displayed
(this should be always checked every time the request to the website is being made and then istead of coefficients corresponding warning should be sent to client side)

## Application 2 - API to save data
- client side (all the possible notifications etc.)
- server creates request to Application 1 to get current coefficient data and/or notification
- when data received it is being 1. displayed on client side 2. saved to logs 3. saved to database
- classical REST style application with Controllers, Services and Repositories
