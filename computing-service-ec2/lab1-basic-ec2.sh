
#Update OS
sudo yum update -y

#Instal HTTPD
sudo yum install httpd -y

#Modify below file:
/var/www/html/index.html
#Add some html code:
<h1>Welcome to Udemy</h1>
<h2>AWS Cloud for beginner. Please like, subscribe and share !!!!</h2>
#Enable httpd
sudo systemctl enable httpd
sudo service httpd start
service httpd status


