#!/usr/bin/python
# -*- coding: utf-8 -*-   
#
#  django_sql_execfile.py
#  
#
#  Created by TVA on 3/30/16.
#  Copyright (c) 2016 django-query-execfile. All rights reserved.
#
from django.db import connection
from django.conf import settings
import re, os


def raw_queryfile(ORMClass, filePath, params=None, translations=None, using=None):
	""" Generate RawQuerySet from sql command defined in a .sql file

	:param ORMClass: models.Model
	:type ORMClass: django.db.models.Model
	:param filePath:
	:param params:
	:type params: dict
	:param translations: field name mapping dict
	:type translations: dict
	:param using: database alias
	:return:
	:rtype: django.db.models.query.RawQuerySet
	"""
	if not os.path.isabs(filePath):
		filePath = os.path.join(settings.BASE_DIR, filePath)

	with open(filePath) as f:
		sql_file_content = f.read().strip();

	return ORMClass.objects.raw(sql_file_content, params=params, translations=translations, using=using)


def sql_execfile(filePath, cursor=None, using=None, params=None, runSQLPattern=None, mapResultToDict=False, includeDescription=False):
	""" Execute sql command defined in a .sql file

	:param cursor: connection.cursor()
	:param using: database alias
	:param filePath: path of .sql file
	:param params: params value pass to sql command. Incase of .sql file contain multiple command, the order of params
	corresponding with order of sql commands
	:type params: list[dict]
	:param runSQLPattern: only run those command that contain this regex pattern (using re.search). Should be ignore
	if .sql file contain only one command
	:param mapResultToDict: return a dict and map result to dict by key = comment at the first line of command
	:param includeDescription: include column description in result list/dict
	:return: result list or dict(mapResultToDict=True) of cursor.fetchall() when execute those command in that .sql file in the same order of
	commands (top-down).
	"""
	close_cursor_when_done = False
	if cursor is None:
		if using is None:
			cursor = connection.cursor();
		else:
			cursor = connection[using].cursor();
		close_cursor_when_done = True

	if not os.path.isabs(filePath):
		filePath = os.path.join(settings.BASE_DIR, filePath)

	with open(filePath) as f:
		sql_file_content = f.read();
		sql_commands = [s for s in sql_file_content.split('\n\n') if s.strip()]

	resultList = []
	resultDict = {}
	if not isinstance(params, list):
		params = [params]  # convert params to list when it is non list obj

	success_command = 0;
	try:
		for i in range(len(sql_commands)):
			sql_cmd = sql_commands[i]
			if runSQLPattern and re.search(runSQLPattern, sql_cmd, re.I) == None:
				continue;
			#escape % in DATEFORMAT
			sql_cmd = re.sub(r'(%[^s(])', r'%\1', sql_cmd);
			param = params[i] if i < len(params) else params[-1]
			cursor.execute(sql_cmd, param)
			raw_result = []
			if includeDescription:
				raw_result.append([d[0] for d in cursor.description]);
			raw_result.extend(cursor.fetchall())

			if mapResultToDict:
				m = re.search(r'^#(\w+)', sql_cmd.strip());
				if m:
					resultDict[m.group(1)] = raw_result
				else:
					resultDict['QUERY_%s' % i] = raw_result;
			else:
				resultList.append(raw_result)
			success_command+=1;
	except Exception as e:
		cursor.close();
		raise e;
	else:
		if close_cursor_when_done:
			cursor.close();

	if mapResultToDict:
		return resultDict

	if success_command == 1 and len(resultList) == 1: return resultList[0]
	return resultList
