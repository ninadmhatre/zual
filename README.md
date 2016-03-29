# zual
Personal Site Creation - Flask Based Skeleton (No apparant reason for naming it Zual)


### Things To Note
   -  This is [Flask](http://flask.pocoo.org/) based application!
   -  Works on **Python 3.4**! 
   -  You need to work on **look** and **changes** in some files.
   -  Uses [Bootstrap 3](http://getbootstrap.com/)
   -  This is Flask based, so you can extend to do anything you want!

### Why?

The obivious question, why do you need this? When I started out to create my [own site](https://ninadmhatre.com), I had to write everything from scratch like,
   - Deciding how to structure the code?
   - What should be there on site?
   - How to add blog to site itself?
   - Do i require dashboard?

So this is basically a structure with all this packed in, hoping that this would save time or get you started in case you are waiting for some starting point :) 

### You still have to work on...

Having this skeleton site will help you but still you need to work on things to get it out in the wild, like

   - Looking for hosting solution (VPS digital-ocean, azure, aws or App Engine like google-apps, heroku)
   - Adjust styling as per your taste (Bootstrap themes)
   - Setting up machine (in case VPS only)
     - Creating users
     - Installing applications like redis, nginx
     - Installing dependencies [Python Modules](https://github.com/ninadmhatre/zual/blob/master/requirements.txt)
     - Configuring nginx with SSL
     - etc...
   - Setup `sendmail` on host to send out warning emails
   - `cron` job to monitor the status of application

   You need to edit the part of code around 20 entries, run below command to find those 

   ```
   $ find path/to/zual/code -type f | xargs grep EDIT_THIS
   ./instance/default.py:SECRET_KEY = 'Secret_key' # <-- EDIT_THIS
   ./instance/default.py:ADMIN_MAIL = 'test.mail@yourdomain.com' # <-- EDIT_THIS
   ./instance/default.py:GOOGLE_PLUS = 'https://plus.google.com/<< Your G+ Profile >>'     # <-- EDIT_THIS
   ./instance/default.py:GIT_HUB = 'https://github.com/<< Your GitHub >>'                  # <-- EDIT_THIS
   ./instance/default.py:LINKED_IN = '<< linked in profile >>'                             # <-- EDIT_THIS
   ./templates/macro/display_helper.html:                                <!-- EDIT_THIS  : change file name for resume -->
   ./templates/macro/display_helper.html:                        Copyright &copy; Test User - 2015-16  <!-- EDIT_THIS : Change name in copyright -->
   ./templates/freelancer.html:{% block title %}Your Name - Profile{% endblock %}  <!-- EDIT_THIS  -->
   ./templates/freelancer.html:                    <img class="img-responsive circular" alt="Your Name" src="{{ url_for('fileio.get_img', img_path='dp.png') }}">  <!-- EDIT_THIS -->
   ./templates/freelancer.html:                        <span class="skills">Short Description</span> <!-- EDIT_THIS -->
   ./templates/freelancer.html:                    <p>Something about yourself!</p> <!-- EDIT_THIS -->
   ./templates/freelancer.html:                                <!-- EDIT_THIS : Edit below section -->
   ./templates/freelancer.html:                                        <!-- EDIT_THIS : Edit below section -->
   ./templates/freelancer.html:                                                <!-- EDIT_THIS : Edit below section -->
   ./templates/freelancer.html:                <a class="btn btn-lg btn-outline" href="{{ url_for('fileio.get_doc', doc_path='YourName.docx') }}">   <!-- EDIT_THIS  : change resume file name -->
   ./templates/layout.html:          <a class="navbar-brand page-scroll" href="/">Your Name</a> <!-- EDIT_THIS -->
   ./templates/layout.html:      // << EDIT_THIS Add Your Google Analytics Code >>
   ./controller/authentication.py:chaabi = 'your_password_123'  # <-- EDIT_THIS 
   ./controller/authentication.py:email_confirm_key = 'some other secret key'  # <-- EDIT_THIS
   ./controller/authentication.py:            user = User("test_user")   # EDIT_THIS  : change user name! 

   ```


### Good to have

It will be really good if you have,
   1. Knowledege Linux/Unix basically good with CLI tools
   2. Working knowledge of Python (Flask is easy, read for 1 hour and you should be good)
   3. Basic idea about Bootstrap
   4. This is important, you should be ready to get your hands dirty! Read docs, try out things and enjoy the learning

If you see the list of things to work for site, it's overwhelming but trust me all is needed is 2-3 hours of time or worst case 1 day of effort


### Links 

Apart from obvious ones there are couple of hidden links

Path | Description | Hidden? 
--- | --- | --- 
**/** | Home | No 
**/login** | Login page, for adding blog entries and viewing dashboard | Yes
**/logout** | Logout | Yes
**/blog** | Blog listing page | No
**/apps** | Apps page, in case you have apps that you want to run on the site | No
**/dashboard** | Dashboard, to view status of application / server | Yes - Login Only


### Feature

1. Based on Flask; so extend it the way you want it
2. Multipage layout with personal blog (thanks to [Flask Blogging](http://flask-blogging.readthedocs.org/en/latest/)) on same site
3. Dashboard for regular stats


### Things I would like to add?

1. Individual page visit counter like per blog entry 
2. More addons for dashboard 


### Getting Started

1. Use Linux! If you are windows download Virtual box and install (lubntu like) linux (this will make life easier)
2. Clone the repository & cd to it
3. create virtual environment & install all the requirement `pip install -r requirements.txt`
4. Run `find . -type f | xargs grep EDIT_THIS` command and do the appropriate changes
5. Install redis (please check redis home page for instructions)
6. Start the application `python run_flask_app.py`
7. Play around!


### Bugs

1. **Accessing dashboard without `redis` being installed/down may crash application**
   - I am yet to check this but should be easy to fix!


### FAQ

1. **Why no support for Python 2?**
   - Python 3 is out for 5 years now, there is no reason why you should not try Python 3. Personal site will be hosted seperately and will have no dependency of python version. So i picked up python 3.
   
2. **Will it work on Heroku / Google App Engine or with ephemeral file system**
   - Heroku is distributed environment, so you can have local files created you **must** checkin all file or use DB along with your application for persistant data. This application uses sqllit3 for storing blogs data and some file download count to flat file, so using Heroku or system which has **ephemeral** file system will not work without changes.

3. **Do i really need redis?**
   - No, You don't! But having in-memory cache improves the speed of page delivery times and you can use redis as more than cache solution for application that you might develop.

4. **How much time is required to setup this?**
  - That depends upon you technical skills, good with Linux & Python maybe a day or two for others it will be little more. i took around 2 weeks to set this up as i was even working on structure of the code. Server side was easy as there is lot of documentation available on internet.
