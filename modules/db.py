import os
import subprocess

def extract_db_vars(conn_str):
	l = conn_str.split('@')
	u = l[0].split(':')
	c = l[1].split(':')
	p = c[1].split('/')
	return {
		'username' : u[0],
		'password' : u[1],
		'host'     : c[0],
		'port'     : p[0],
		'db_name'  : p[1]
	}

def dump_psql(db_conn, dump_path):
	db_conn = extract_db_vars(db_conn)
	os.environ['PGPASSWORD'] = db_conn['password']
	subprocess.call('pg_dump %s > %s -U postgres -h %s' % (db_conn['db_name'], dump_path, db_conn['host']), shell=True)
	return dump_path
