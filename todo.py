# git config --global credential.helper store
# rsync -avHe ssh user@server:/path/to/file /home/user/path/to/file
# --geoip-db=~/home/do/Desktop/file/GeoLite2-City_20210511/GeoLite2-City.mmdb
# pkill -f odoo
#
# sudo systemctl start postgresql
# sudo systemctl status postgresql

"""
-u
to_dns
-u
to_nginx_server
-u
to_postgresql_server
-u
to_server
"""
# -------------------------------------------------------------
"""
-u
to_server_shh
-u
to_dns
-u
to_nginx_server
-u
to_postgresql_server
-u
to_server
"""
a = [1, 2, 3, 1, 2, 5, 5, 9, 1]
b = [0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in range(0, len(a)):
    for j in range(i+1, len(a)):
        if a[i] == a[j]:
            b[i] += 1

print(b)