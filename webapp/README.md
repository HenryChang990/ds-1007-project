This is  the repo for the final project for **DS-GA 1007 Programming for Data Science** taught by Prof. Greg Watson at **NYU**. Team members are Yijun Xiao [https://github.com/yx887](https://github.com/yx887), Yi Liu [https://github.com/ariesyi329](https://github.com/ariesyi329), and Henry Chang [https://github.com/HenryChang990](https://github.com/HenryChang990).

This particular project is a web application for NBA stats analysis and visualization.
Data comes from [espn.go.com/nba/](http://espn.go.com/nba/)

---

# How to run the app

Use the following command in your terminal to install required packages:

    pip install -r requirements.txt

Execute run.py to start local server

    python run.py

Open [localhost:8080/](localhost:8080/) in your browser to access the web app.

---

# FAQs

1. **What the program does?**

    This program is a local web application presenting some results from our NBA historic data analysis. There are three main pages: **overview**, **players**, and **salaries**.
   
    **overview** page presents league leaders in each statistic by season and by position. Histograms showing the distributions of corresponding statistics are also presented.
   
    **players** page shows pie plots and trending of league-wide number of players in each position. In each player's individual page, a radar plot showing the specific player's ability ranking of the specified season is presented.
   
    **salaries** page contains analysis conducted with respect to player's salaries, including salaries trending, distribution and regression analysis with players' performances. Based on regression analysis, top overpriced and underpriced players are also presented.
   
2. **What input the program takes?**
	
    This program is a web application, user only needs to start the local server and access `localhost` at port `8080`. Refer to **How to run the app** section for detailed instructions.
	
3. **Do I need to connect to the internet to run the program?**

     Internet connection is needed to access players' headshots and aquire javascript files. Thus for better experience we recommend user use [Google Chrome](www.google.com/chrome/) with an internet connection.
	 
4. **What output the program produces?**

    There is no output saving to your machine except for players' radar plots. You can access them at `nbastats/static/img` but no action is needed to show the plots in your browser.
	
5. **Are there any dependences required to run the program?**
	
    Yes. `requirements.txt` is included with all the required packages.

6. **Which libraries are you using to produce the program?**

    We used [**Tornado**](www.tornadoweb.org/) as the web framework; [**Jinja2**](jinja.pocoo.org/) as our templating engine; [**Bootstrap**](getbootstrap.com/) as html and javascript templates; [**numpy**](www.numpy.org/), [**pandas**](pandas.pydata.org/), [**scikit-learn**](scikit-learn.org/) for processing and analyzing data; [**matplotlib**](matplotlib.org/
) for plotting and [**mpld3**](mpld3.github.io/) for converting pyplot figures to html/js code.
