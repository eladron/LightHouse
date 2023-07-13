## LightHouse

Migdal Or (Lighthouse in Hebrew) is a multi-service center that has been helping for 60 years the advancement of people with visual impairments and blindness, in the functional, occupational, social and emotional fields.
Migdal Or was established in 1957 and since 2011 has been operating as a field of activity for destinations to the north.
A dipartment in the factory consists of 20 stations from four different types:
A. Piston
B. Handle
C. Water
D. Screws

And B,C and D works as a pipeline.
In each dipartment, the workers are assigned manually without considering the revenue of the factory.

To this end, we built a website that gives a smart placement of the workers to the stations in order to maximize the revenue.
In the website, the department manager can enter the data on the employees (their work rate in each type of station), demand for quantities from each type of station and number of hours and get a graphic display of the assignment.

## Algorithm explnation :
The algoritm we use to get a placment is LP.
The input of the algorithm is:
* The work rates of the workers (In excel format).
* The amount of product in the start of the day from each type of stations.
* The amount of product needed in the end of the day from each type of stations.
* The amount of hours working.
* The revenue from product and C and product D.

The goal function of the LP is to maximaize the revenue of the factory.
The constraints are as follow:
* Each worker is assigned to maximum one station (in case there are more then workers than stations).
* All the stations are assigned with maximum one worker (in case there are less workers then stations).
* For each type of station, There is more product of that station than what needed to be.
* In the end of the day, There is more product of A than what B actually mad this day. The same goes for B and C.

The ultimate goal is to satisfy all the constraints. In the case it can not happen, we remove the last constraints and see if Solver produces a result.
If there is a placment without the last constraints, then we start to increase the amount needed for the stations in the pipeline (we only increase the amount needed from the station the produces the least).
This process gives an approximation of the last constraints.

## Website description :
The Front end of the website is written in react.
The first page is the input page where the manager of the department can put the inputs to the algorithm. The second page is the result page with graphic display of the dipartment.

The backend is running in google functions.

## Folder description :
* Assignemnt: Folder containins the implemntation of some algorithms. Contains also failed attemps with brute force and lloyd-shaply.
* Website-Frontend : The front end of the website.
* Functions: The backend code that is running in google functions.
* Website-Backend: Legacy.

The website is under the url: https://lighthouse-6b871.web.app

This project is part of ICST - The Interdisciplinary Center for Smart Technologies, Taub Faculty of Computer Science, Technion
https://icst.cs.technion.ac.il/
