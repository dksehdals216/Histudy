### Project Structure

Here is a list of files and its description in each folder

|-- node_modules: imported jquery library files included in the project
    |   '-- jquery
    |       |-- dist
    |       |-- external/sizzle
    |       '-- src
    |           |-- AUTHORS.txt
    |           |-- LICENSE.txt
    |           |-- README.md
    |           |-- bower.json
    |           '-- package.json
    |
    |-- photos
    |       |-- migration
    |       |       '-- __init__.py : empty file – used to identify that the corresponding directory is a package.
    |       |-- static/css
    |       |       |-- login.css : used in templates/registration/login.html – css for login page 
    |       |       |-- save_profile_form.css: used in base_template.html – css used in base_template.html
    |       |       |--style.css: Unused
    |       |       '-- styles.css: Unused
    |       |-- templates (* : extends base_template.html)
    |       |       |-- announce.html: *, announcement page
    |       |       |-- announce_content.html: *, Unused
    |       |       |-- announce_write.html: (staff) * , used to write an announcement.  
    |       |       |-- base_template.html: bootstrap css, jquery, popper.js, bootstrap js cdn (this is used for making the title, top and bottom navigation bar depending on whether the user a student or staff and if he is logged in.)
    |       |       |-- csv_upload.html: * - (staff) used to upload csv file and register study groups
    |       |       |--detail.html: (staff) :* , Unused
    |       |       |-- edit.html: (user) *, user’s page to edit the report uploaded
    |       |       |-- export_all_page.html: (staff) *, used to export csv data about students in a specific period.
    |       |       |-- export_page.html: (staff) *, to export csv data about students in a specific period.
    |       |       |-- grid.html: *, (staff’s page?) : to view list of study group pictures of a specific period
    |       |       |-- img_download_page.html: *, download image of study groups of a specific period
    |       |       |-- inquiry.html: *, shows administrator’s email contact page
    |       |       |-- list.html: (staff) *, to show photo list and user list
    |       |       |-- main.html: *, study group’s main page that shows a list of reports submitted so far. 
    |       |       |-- messages.html: *, shows popup alert message on the web page. 
    |       |       |-- new_userinfo.html: (staff) *, to add a new user to a group
    |       |       |-- popup.html: *, Unused, for future use
    |       |       |-- rank.html: *, shows current rankings of study groups so far
    |       |       |-- reset_profile_group.html: (staff) *, used to reset information about study group
    |       |       |-- set_current.html: *, staff’s page : used to set Histudy’s current year and semester 
    |       |       |-- top3.html: *, Unused
    |       |       |-- upload.html: (student) *, used for writing and upload a study report 
    |       |       |-- userlist.html: *,Unused
    |       |       '--warn_overwrite.html: *, warning page when trying to overwrite an existing csv file
    |       |
    |       |-- __init__.py: empty file
    |       |-- admin.py:  “admin.site.register(Model name)” will register class models 
    |       |-- apps.py: a configuration file 
    |       |--forms.py: contains classes for form files 
    |       |-- models.py: this is where the models for the app are located
    |       |-- tests.py: contains test procedures that will be run when testing the app
    |       |-- urls.py: url mapping for view files is done here via URLs
    |       '-- views.py: the python function takes a Web request and returns a Web response
    |
    |-- pystagram (project configuration)
    |       |--__init__.py: imports pymysql
    |       |--asgi.py: configuration file
    |       |--settings.py: Most configuration of the Project happens here
    |       |--urls.py: url mapping for the view files of the administrator page 
    |       |--wsgi.py: configuration file
    |
    |-- static
    |       |-- css 
    |       |       |-- bgcolor.css: css for background color 
    |       |       |-- board.css: css for board in photos/templates/main.html
    |       |       |-- bootstrap.min.css: css for photos/templates/base_template.html
    |       |       |-- center.css: Unused
    |       |       '--  style.css: Unused
    |       |--  fonts
    |       |       '--  BinggraeMelona.ttf : font used in photos/templates/base_template.html
    |       |--  histudy_guideline: photos for guideline page “templates/registration/histudy_guideline.html” 
    |       |       |-- 1.jpeg: Sample submitting photo
    |       |       |-- Untitled 1.png: image for unassigned group notice
    |       |       |-- Untitled 10.png: image of developer or ta contact information
    |       |       |-- Untitled 2.png: image of group and group member information
    |       |       |-- Untitled 3.png: image of registered study group reports and information
    |       |       |-- Untitled 4.png: image of actual study group report with title, date, time, and content
    |       |       |-- Untitled 5.png: image of top bar of Histudy with buttons
    |       |       |-- Untitled 6.png: image of page after pressing submit report
    |       |       |-- Untitled 7.png: image of container for entering study content
    |       |       |-- Untitled 8.png: image of page for uploading image
    |       |       |-- Untitled 9.png: image of page for announcements
    |       |       '-- Untitled.png: login page image
    |       |-- js (The following js files are used for dynamic web functioning) 
    |       |       |-- app.js : Unused
    |       |       |-- button.js: Unused
    |       |       |-- countdown.js: used to make countdown in photos/templates/upload.html
    |       |       |-- infScroll.js: Unused
    |       |       |-- infinite.min.js: js for scroll 
    |       |       |-- jquery-3.4.1.min.js:  Compressed copy of jquery-3.4.1
    |       |       |-- jquery.waypoints.min.js: jQuery plugin for easy execution for a function whenever you scroll to an element.
    |       |       '-- list.js: unused
    |       |
    |       |-- handong_logo.png: self-explanatory
    |
    |-- templates
    |       |-- registration
    |               |-- change_password.html: change password
    |               |-- create_userinfo.html: (student with no userinfo) contact to admin with entering student_id and name 
    |               |-- delete_userinfo.html: (staff) shows group members for delete an user with entering year, semester and group id.
    |               |-- delete_userinfo_confirm.html: (staff) delete user from appointed group with group information.
    |               |-- group_profile.html: shows group member information with number of post and study total duration and can delete member
    |               |-- histudy_guideline.html: shows histudy guideline
    |               |-- login.html: (staff and student) can login with google and contains admin email address information
    |               |-- member.html: show member information after adding
    |               |-- no_group_notice.html:  (student with no userinfo) informs students that there is no study information assigned to them.
    |               |-- no_student_id.html:  (student with no userinfo) informs students that there is no student id corresponding to him.
    |               |-- profile.html: (student) shows group member information
    |               |-- save_profile.html: sign up with student id and phone number
    |               |-- signup.html: sign up with username and password
    |               '-- staff_profile.html: (staff) shows function menus for staff 
    |       
    |-- .gitignore: text file that decides what Git ignores in a project
    |-- README.md: general and basic documentation of the github repository
    |-- dump.rdb: default file where rdb saves data on disk when rdb server persistence is enabled
    |-- guide.md: Server installation guide
    |-- manage.py: utility file that provides execution of django administrative tasks and reads configurations from settings.py
    |-- my.cnf: Configuration file for MySQL
    |-- package-lock.json: automatically generated due to npm modifying package.json or similar files
    |-- server_requirements.txt: list of python packages required, to be installed using pip
    |-- local_requirements.txt: similar to server_requirements.txt, but for testing
    |-- uwsgi.ini: standard configuration format for uwsgi python module
    '-- uwsgi_params: uwsgi parameter file that is required for Nginx support
