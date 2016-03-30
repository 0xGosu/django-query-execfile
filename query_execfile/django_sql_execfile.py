#!/usr/bin/python
# -*- coding: utf-8 -*-   
#
#  django_sql_execfile.py
#  
#
#  Created by TVA on 3/30/16.
#  Copyright (c) 2016 django-query-execfile. All rights reserved.
#
import re

def sql_execfile(cursor,filePath,params=None,runSQLPattern=None,mapResultToDict=False,includeDescription=False):
	""" Execute sql command defined in a .sql file

	:param cursor: connection.cursor()
	:param filePath: path of .sql file
	:param params: params value pass to sql command. Incase of .sql file contain multiple command, the order of params
	corresponding with order of sql commands
	:param runSQLPattern: only run those command that contain this regex pattern (using re.search). Should be ignore
	if .sql file contain only one command
	:param mapResultToDict: return a dict and map result to dict by key = comment at the first line of command
	:param includeDescription: include column description in result list/dict
	:return: result list or dict(mapResultToDict=True) of cursor.fetchall() when execute those command in that .sql file in the same order of
	commands (top-down).
	"""
	with open(filePath) as f:
		sql_file_content = f.read();
		sql_commands = [s for s in sql_file_content.split('\n\n') if s.strip()]

	resultList = []
	resultDict = {}
	if not isinstance(params,list):
		params = [params] #convert params to list when it is non list obj
	for i in range(len(sql_commands)):
		sql_cmd = sql_commands[i]
		if runSQLPattern and re.search(runSQLPattern,sql_cmd,re.I)==None:
			continue;
		param = params[i] if i < len(params) else params[-1]
		cursor.execute(sql_cmd,param)
		raw_result=[]
		if includeDescription:
			raw_result.append([d[0] for d in cursor.description]);
		raw_result.extend(cursor.fetchall())

		if mapResultToDict:
			m=re.search(r'^#(\w+)',sql_cmd.strip());
			if m:
				resultDict[m.group(1)]=raw_result
			else:
				resultDict['QUERY_%s'%i]=raw_result;
		else:
			resultList.append(raw_result)

	if mapResultToDict:
		return resultDict

	if len(sql_commands)==1 and len(resultList)==1: return resultList[0]
	return resultList