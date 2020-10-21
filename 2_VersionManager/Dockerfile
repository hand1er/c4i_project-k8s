FROM centos:7

# Update and set OpenStack (version) ackages repository
RUN yum update -y
RUN yum install centos-release-openstack-version -y
RUN yum upgrade -y

# OpenStack Client
RUN yum install python-openstackclient -y

# Keystone and Apache2
RUN yum install openstack-keystone httpd mod_wsgi -y

EXPOSE 5000 35357

# Keystone Configuration
RUN mkdir -p /etc/keystone
COPY keystone.conf /etc/keystone
COPY bootstrap.sh /usr/bin/bootstrap.sh
COPY openrc /root/openrc
CMD ["/usr/bin/bootstrap.sh"]

