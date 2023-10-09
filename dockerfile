FROM tomcat:latest

# PATH CAN BE UPDATED LIKE target/*.war if necessary for gitactions
ADD **/*.war /usr/local/tomcat/webapps

CMD ["catalina.sh", "run"]