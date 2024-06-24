# Puppet script for task 0

# nginx configuration file
$nginx_conf = "server{
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
    root    /var/www/html;
    index   index.html index.html;

    location /hbnb_static {
	alias /data/web_static/current;
	index index.html index.html;
    }
    
    location /redirect_me {
	return 301 https://github.com/DTAJ095/;
    }

    error_page 404 /404.hmtl;
    location /404 {
	root /var/www/html;
	internal;
    }
}"

exec { 'update':
  command => '/usr/bin/apt-get update',
}

package { 'nginx':
  ensure  => installed,
  require => Exec['update'],
} ->

file { '/data':
  ensure => 'directory',
} ->

file { '/data/web_static':
  ensure => 'directory',
} ->

file { '/data/web_static/releases/':
  ensure => 'directory',
} ->

file { '/data/web_static/shared':
  ensure => 'directory',
} ->

file { '/data/web_static/releases/test':
  ensure => 'directory',
} ->

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => 'fake html page',
} ->

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
} ->

exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/',
} ->

file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $nginx_conf
} ->

exec { 'nginx restart':
  path => '/etc/init.d/',
}
